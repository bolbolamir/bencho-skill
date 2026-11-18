# Bencho-inspired Component Studio

A reusable Codex skill and local gallery for designing interactive UI components. Includes the accepted header example and a 169-component design study.

## Start the gallery

Requires Python 3.10 or newer. No Python packages or API key are needed.

```sh
cd studio
python3 studio.py serve --open
```

Open http://127.0.0.1:8765/. On macOS you can also run `studio/Start Studio.command`.

## Install the skill

Copy `skills/component-studio` to your Codex skills directory (normally `~/.codex/skills/`). In a fresh Codex chat, use:

```text
Use $component-studio to build a date picker. My studio is at /absolute/path/to/bencho-skill/studio. Save it to my gallery.
```

Replace `<checkout>` in the skill's local-studio reference with your actual checkout path, or supply your studio path in each request. The gallery's New component and Refine actions prepare prompts for fresh Codex chats. Codex generates the components; the browser does not call an AI service.

## Contents

- `skills/component-studio`: instructions, design reference, lookup helper, tokens and header source.
- `studio`: local gallery with live previews, revisions, source view and HTML export.
- `research`: component-by-component audit, visual reference sheets and original free theme tokens.

## Checks

```sh
python3 studio/studio.py --root studio check
node --check studio/app/studio.js
```

The gallery has been checked for immutable revisions, duplicate saves, concurrent writes and standalone export. The source study distinguishes 47 free live/source components from 122 Pro static previews; Pro motion implementations were not verified.

## Attribution

Inspired by [Bencho](https://bencho.dev/). This is an independent project, not the official Bencho library. Original Bencho theme tokens retain their MIT notice. Lucide's vendored runtime and license are under `studio/assets/`. The study uses screenshots for reference; it does not grant rights to Bencho branding or source photographs.
