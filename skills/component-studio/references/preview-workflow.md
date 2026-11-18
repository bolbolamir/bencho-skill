# Preview contract

The collection is an independent local web app. Build in Codex, register the preview with `studio.py add`, and inspect it in the gallery. Do not create an inline chat visualization unless the user requests one. Start fresh chats freely: the skill, manifest and saved sources carry the relevant context.

## Files

- Default input: literal HTML fragment with root-scoped style and script, or a full standalone document.
- Fragments get a viewport, `color-scheme`, a neutral page background, a quiet optional `.viz-dotted-background`, `.cursor-interaction`, and the local Lucide runtime.
- Each revision stores the raw source, generated preview and any `--source` attachments. Never edit a prior version's files for a refinement. Start from its raw source, write a working file, then save the result with the same component id.
- Export HTML returns a standalone document with the icon runtime embedded when wrapping a fragment. For a full document, keep dependencies self-contained or explicitly supplied by that document.
- React is supported as attached source beside a working HTML preview. Don't represent an unrendered TSX file as a completed preview. If a task needs a build tool, use one for the component and register its working standalone preview.

## Browser boundary

The preview iframe allows scripts and is isolated from the gallery's origin. It blocks network connections and outbound form actions. Local visual behavior belongs in explicit handlers. Native form submit can be blocked by preview environments, so wire a save button's click and input Enter path deliberately; don't rely solely on a default submit action. Local simulated controls should not pretend to have a backend connection.

Native `<dialog>` works in previews. Position an anchored dialog before `showModal()` so its first focused control cannot scroll an offscreen initial position into view. Calculate bounds from the viewport and known final dialog size, rather than a scaled rectangle halfway through an entrance animation. Test the narrowest supported width after opening a dialog, not only in the resting header.

Scope generic control selectors with low specificity, for example `#component :where(button,input)`. A rule such as `#component .app button { color: inherit; }` can silently override an inverse primary button's text and hide its label.

Static `data-lucide` placeholders are initialized by the wrapper. After dynamic insertion, call `lucide.createIcons()` if available. Keep icon-only actions labeled. Custom avatar gradients are fine; keep the component useful while optional assets load.

## Verification

Check actions that establish the requested behavior. For an interactive header, that means each dialog opens, save changes update visible state, counts track read items, and dismissal returns focus. For a slider, verify bounds and a keyboard path. For responsive components, inspect both the resting and expanded states at a narrow width. Apply reduced motion to travel, blur and physical effects while keeping the information available.

The gallery itself offers appearance and preview width controls, source inspection, export, reset and a revision selector. Use the selected component URL in the final response. Keep the user's chat focused on the design request and feedback, with implementation context in the files.
