---
name: component-studio
description: "Create and refine reusable UI components for the user's Bencho-inspired Component Studio, saving interactive previews and versions to a separate local gallery. Use for Component Studio requests or components intended for this collection."
---

# Component Studio

Build components in Codex and keep their interface, source and revision history in the local gallery. The user prefers fresh chats with little setup context and no inline gallery UI. Return the selected component's gallery link after saving; show an inline preview only if explicitly requested.

## Start with the relevant context

Read [design-language.md](references/design-language.md) for the visual direction the user accepted. Consult [local-studio.md](references/local-studio.md) for the collection's location and commands. A user-specified studio location overrides the default.

Inspect the current collection with `scripts/studio.py --root <studio> list`. For a refinement, read the selected version's source from `library.json`; don't reconstruct it from chat history. The accepted header is also available in `assets/soft-header.html` as a starting reference when its patterns fit.

For a specific pattern, query `python3 <skill-dir>/scripts/reference.py "profile notification"`. This returns only a few relevant entries from the 169-component Bencho audit. Do not load the whole catalog into context. The 47 free entries were studied through live previews and public source; 122 Pro entries were static previews and descriptions. Their exact animation implementation is unverified.

## Build and save

Default to an HTML fragment or a self-contained HTML document with scoped CSS and JavaScript. If the user requests React, produce the React/CSS source plus a working HTML preview and attach the source files when saving. Adapt to an existing project's stack when the user names one.

The gallery wraps fragments with a viewport, theme support and a vendored `lucide` global. Use `data-lucide` for static icons; call `lucide.createIcons()` after inserting icons dynamically. The accepted header's `window.openai` and `Tweak` integrations are optional guards, not requirements for standalone components.

Keep the requested actions functional. Check the primary interaction, closing and keyboard behavior, and narrow layout when relevant. Follow [preview-workflow.md](references/preview-workflow.md) for the preview contract and the specific pitfalls already found in this studio.

Write working files under the studio's `work/`. Register a finished component or refinement with:

```sh
python3 <skill-dir>/scripts/studio.py --root <studio> add \
  --id date-picker --name "Date picker" --category Inputs \
  --description "A date picker with an unfolding calendar." \
  --html <absolute-preview-file> --label "Original"
```

Reuse the component id for a new revision. Old versions remain unchanged. To include React or CSS sources, add `--source <absolute-file>` for each file. Record the brief with `--prompt` when useful; do not include credentials or unrelated chat content.

Run `scripts/studio.py --root <studio> check` after registration. The gallery updates automatically while open. Start it with `scripts/studio.py --root <studio> serve` if needed. These commands have no model API calls: Codex is the designer, the gallery is the persistent viewer.

Keep the final response short: what changed, the component link, and a material verification limit if one remains. The reusable context belongs here and in the component files, not in long chat summaries.
