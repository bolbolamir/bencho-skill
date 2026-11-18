# Component Studio

This is the user's persistent component collection. Use the installed `$component-studio` skill for design and refinement requests here.

The design direction and preview workflow live in that skill. Inspect `library.json` and only the selected component's source; the original research chat is not needed.

Work in `work/`. Save finished previews with `python3 studio.py add` and reuse the component id for a new immutable revision. Keep previous versions intact. `python3 studio.py list` summarizes the collection; `python3 studio.py check` validates its references.

The gallery runs with `python3 studio.py serve` at http://127.0.0.1:8765/. It refreshes when the library changes. Present component previews there instead of inline in chat unless requested. Use a fresh chat for a new component when useful; preserve context through source and versions rather than long conversation summaries.
