# Local collection

Default project: `<checkout>/studio`.

Gallery: `http://127.0.0.1:8765/`. A selected item uses `?component=soft-header`.

Installed skill: `<skill-dir>`.

The project has `library.json`, immutable files under `components/<id>/v001/`, the gallery under `app/`, a vendored Lucide bundle under `assets/`, and `studio.py`. The root `AGENTS.md` is intentionally small; there is no dependency on the original research chat.

Typical commands, using the skill's own helper:

```sh
python3 <skill-dir>/scripts/studio.py --root <checkout>/studio list
python3 <skill-dir>/scripts/studio.py --root <checkout>/studio serve
```

Keep the server in a retained execution session while the user uses the gallery. If the same gallery is already running on the requested port, `serve` returns its URL without starting another. A different service on that port is an error; use a different explicit `--port` rather than stopping an unrelated service.

The user can double-click `Start Studio.command` in the project to open the gallery themselves. It starts a local server or opens the existing one. Closing that Terminal stops a server started by that launcher.

`library.json` is the collection's source of truth. The add command locks updates and writes it atomically. Register the same source twice and it returns the existing version. Different source creates a new immutable version. Use the helper rather than hand-editing version records.

The gallery's New component and Refine actions prepare a brief for a fresh Codex chat. They do not run a model from the browser. No API key or separate model service is involved in this mode.
