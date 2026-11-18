#!/usr/bin/env python3
"""Versioned local UI-component collection. Python standard library only."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
import re
import shutil
import sys
import tempfile
from urllib.parse import parse_qs, unquote, urlsplit
from urllib.request import urlopen
import webbrowser


def stamp():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=path.parent, delete=False) as out:
        json.dump(value, out, ensure_ascii=False, indent=2)
        out.write('\n')
        temporary = Path(out.name)
    temporary.replace(path)


def init(root):
    root.mkdir(parents=True, exist_ok=True)
    (root / 'components').mkdir(exist_ok=True)
    if not (root / 'library.json').exists():
        atomic_json(root / 'library.json', {'schema': 1, 'updatedAt': stamp(), 'components': []})


def load(root):
    return json.loads((root / 'library.json').read_text())


@contextmanager
def lock(root):
    init(root)
    with (root / '.library.lock').open('a') as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def document(source, root, title, inline_icons=False):
    if re.search(r'<!doctype|<html\b', source, re.I):
        return source
    icons = root / 'assets/lucide.js'
    if inline_icons and icons.exists():
        icon_script = '<script>' + icons.read_text().replace('</script', '<\\/script') + '</script>'
    else:
        icon_script = '<script src="/assets/lucide.js"></script>'
    return '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>''' + html.escape(title) + '''</title>
<style>
:root{color-scheme:light dark}html,body{margin:0;min-height:100%;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:light-dark(#fafaf9,#0a0a0a);color:light-dark(#17181a,#f5f5f3)}
.cursor-interaction{cursor:pointer}[hidden]{display:none!important}
.viz-dotted-background{background-image:radial-gradient(light-dark(#17181a13,#ffffff10) .8px,transparent .8px);background-size:16px 16px}
</style><script>const theme=new URLSearchParams(location.search).get('theme');if(theme==='light'||theme==='dark')document.documentElement.style.colorScheme=theme;</script>
</head><body>''' + icon_script + source + '''
<script>if(window.lucide)lucide.createIcons({attrs:{width:18,height:18}});</script>
</body></html>'''


def add(root, args):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', args.id):
        raise ValueError('Component id must use lowercase words separated by hyphens.')
    source = Path(args.html).expanduser().resolve().read_text()
    attachments = [Path(value).expanduser().resolve() for value in args.source]
    if len({p.name for p in attachments}) != len(attachments):
        raise ValueError('Source attachments must have unique file names.')
    digest = hashlib.sha256(source.encode())
    for file in attachments:
        digest.update(file.name.encode())
        digest.update(file.read_bytes())
    fingerprint = digest.hexdigest()
    with lock(root):
        library = load(root)
        component = next((c for c in library['components'] if c['id'] == args.id), None)
        if component and component['versions'][-1]['fingerprint'] == fingerprint:
            return {'status': 'unchanged', 'id': args.id, 'version': component['versions'][-1]['id'], 'url': f'http://127.0.0.1:{args.port}/?component={args.id}'}
        now = stamp()
        if component is None:
            component = {'id': args.id, 'name': args.name or args.id.replace('-', ' ').title(), 'description': args.description or '', 'category': args.category or 'Components', 'createdAt': now, 'versions': []}
            library['components'].append(component)
        else:
            for field in ['name', 'description', 'category']:
                if getattr(args, field) is not None:
                    component[field] = getattr(args, field)
        parent = root / 'components' / args.id
        existing_numbers = [int(p.name[1:]) for p in parent.glob('v[0-9]*') if p.is_dir() and p.name[1:].isdigit()]
        number = max(existing_numbers, default=0) + 1
        revision_id = f'v{number:03d}'
        folder = parent / revision_id
        folder.mkdir(parents=True)
        (folder / 'source.html').write_text(source)
        (folder / 'preview.html').write_text(document(source, root, component['name']))
        files = [{'name': 'source.html', 'path': str((folder / 'source.html').relative_to(root))}]
        for file in attachments:
            target = folder / 'sources' / file.name
            target.parent.mkdir(exist_ok=True)
            shutil.copy2(file, target)
            files.append({'name': file.name, 'path': str(target.relative_to(root))})
        revision = {'id': revision_id, 'number': number, 'label': args.label or ('Original' if not component['versions'] else 'Refinement'), 'createdAt': now, 'preview': str((folder / 'preview.html').relative_to(root)), 'files': files, 'prompt': args.prompt or '', 'fingerprint': fingerprint}
        component['versions'].append(revision)
        component['updatedAt'] = now
        library['updatedAt'] = now
        atomic_json(root / 'library.json', library)
    return {'status': 'saved', 'id': args.id, 'version': revision_id, 'preview': str(folder / 'preview.html'), 'url': f'http://127.0.0.1:{args.port}/?component={args.id}'}


def select_version(root, query):
    component = next((c for c in load(root)['components'] if c['id'] == query.get('component', [''])[0]), None)
    if component is None:
        raise ValueError('Component not found.')
    requested = query.get('version', [''])[0]
    version = next((v for v in component['versions'] if v['id'] == requested), None) if requested else component['versions'][-1]
    if version is None:
        raise ValueError('Version not found.')
    return component, version


def check(root):
    library = load(root)
    errors = []
    ids = set()
    for component in library['components']:
        if component['id'] in ids:
            errors.append('Duplicate id: ' + component['id'])
        ids.add(component['id'])
        for revision in component['versions']:
            for item in [{'path': revision['preview']}, *revision['files']]:
                path = (root / item['path']).resolve()
                if not path.is_relative_to(root) or not path.is_file():
                    errors.append('Missing or invalid file: ' + item['path'])
    return {'ok': not errors, 'components': len(ids), 'versions': sum(len(c['versions']) for c in library['components']), 'errors': errors}


def serve(root, port, open_browser):
    init(root)
    address = f'http://127.0.0.1:{port}/'
    try:
        with urlopen(address + 'api/health', timeout=.5) as response:
            running = json.load(response)
        if running.get('service') == 'component-studio' and running.get('root') == str(root):
            print(address, flush=True)
            if open_browser:
                webbrowser.open(address)
            return
    except Exception:
        pass

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def send(self, body, content_type='application/json; charset=utf-8', status=200, download=None):
            if isinstance(body, (dict, list)):
                body = json.dumps(body, ensure_ascii=False).encode()
            elif isinstance(body, str):
                body = body.encode()
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Referrer-Policy', 'no-referrer')
            if download:
                self.send_header('Content-Disposition', f'attachment; filename="{download}"')
            if content_type.startswith('text/html') and not download:
                if urlsplit(self.path).path.startswith('/components/'):
                    self.send_header('Content-Security-Policy', "default-src 'none'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://esm.sh https://unpkg.com; style-src 'unsafe-inline' https://fonts.googleapis.com; font-src data: https://fonts.gstatic.com; img-src data: blob: https:; media-src data: blob:; connect-src 'none'; form-action 'none'; base-uri 'none'")
                else:
                    self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; frame-src 'self'; connect-src 'self'; base-uri 'none'")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            parsed = urlsplit(self.path)
            query = parse_qs(parsed.query)
            path = unquote(parsed.path)
            try:
                if path == '/api/health':
                    return self.send({'service': 'component-studio', 'root': str(root)})
                if path == '/api/library':
                    return self.send(load(root))
                if path in ['/api/source', '/api/export']:
                    component, version = select_version(root, query)
                    if path == '/api/export':
                        source = (root / version['files'][0]['path']).read_text()
                        return self.send(document(source, root, component['name'], inline_icons=True), 'text/html; charset=utf-8', download=f"{component['id']}-{version['id']}.html")
                    name = query.get('file', [version['files'][0]['name']])[0]
                    file = next((f for f in version['files'] if f['name'] == name), None)
                    if file is None:
                        raise ValueError('Source file not found.')
                    return self.send({'name': file['name'], 'content': (root / file['path']).read_text()})
                relative = 'app/index.html' if path == '/' else path.lstrip('/')
                if relative.split('/')[0] not in ['app', 'assets', 'components']:
                    return self.send({'error': 'Not found'}, status=404)
                file = (root / relative).resolve()
                if not file.is_relative_to(root) or not file.is_file():
                    return self.send({'error': 'Not found'}, status=404)
                content_type = mimetypes.guess_type(file.name)[0] or 'application/octet-stream'
                return self.send(file.read_bytes(), content_type + ('; charset=utf-8' if content_type.startswith(('text/', 'application/javascript')) else ''))
            except (ValueError, KeyError, OSError) as exc:
                return self.send({'error': str(exc)}, status=404)

    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    print(address, flush=True)
    if open_browser:
        webbrowser.open(address)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default=str(Path.cwd()), help='Component Studio project directory')
    parser.add_argument('--port', type=int, default=8765)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('init')
    sub.add_parser('list')
    sub.add_parser('check')
    save = sub.add_parser('add', help='Save a new component or an immutable revision')
    save.add_argument('--id', required=True)
    save.add_argument('--html', required=True)
    save.add_argument('--name')
    save.add_argument('--description')
    save.add_argument('--category')
    save.add_argument('--label')
    save.add_argument('--prompt')
    save.add_argument('--source', action='append', default=[])
    web = sub.add_parser('serve')
    web.add_argument('--open', action='store_true')
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    try:
        if args.command == 'init':
            init(root)
            emit({'root': str(root), 'status': 'ready'})
        elif args.command == 'add':
            emit(add(root, args))
        elif args.command == 'list':
            emit([{'id': c['id'], 'name': c['name'], 'category': c['category'], 'versions': len(c['versions']), 'latest': c['versions'][-1]['id']} for c in load(root)['components']])
        elif args.command == 'check':
            result = check(root)
            emit(result)
            return 0 if result['ok'] else 1
        else:
            serve(root, args.port, args.open)
    except (OSError, ValueError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
