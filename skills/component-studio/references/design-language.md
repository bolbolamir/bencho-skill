# The user's accepted component direction

The user studied Bencho with Codex and accepted the resulting soft header. Treat that header as the strongest concrete example. The language is calm at rest and physical in use: compact neutral interfaces, rounded geometry and motion that explains changes. This is an aesthetic reference, not a mandate to duplicate a proprietary component or apply every effect everywhere.

## Material and type

Light surfaces are warm whites and grays: canvas `#fff`, surface `#f7f7f6`, nested surfaces `#f1f1f0` and `#ecebe7`; main ink `#17181a`, secondary `#6f6e68`. Dark surfaces use canvas `#0a0a0a`, surfaces around `#171717`–`#262626`, off-white ink and muted gray secondary text. Use theme-aware product variables, preferably `light-dark()` with an explicit color scheme. Bright color belongs to a selected state, status, data or a small identity asset such as an avatar.

Use a low-opacity ink wash for hover and inset one-pixel edges where useful. Most ordinary surfaces stay flat. Refraction and glass belong to an actual lens or translucent element, rather than the whole interface.

Inter or a close system sans is appropriate. Body and control text is generally 12–16 px with 400/500 weights. Titles are often 18–20 px and slightly tight. Avoid undersized essential text; use tabular figures on animated numbers.

## Geometry

Common gaps are 6, 8, 10, 12 and 16 px. Typical card padding is 16–22 px. Large component/modals use 24–28 px corners; nested fields and rows use about 12–16 px; pills are fully rounded. These are starting relationships, not one compulsory radius for all elements. Nested corners should agree visually with the outer shape and padding.

Keep a small control's intrinsic size useful. The space around a component belongs to the preview, not necessarily to its production API. Adapt to the real container down to a narrow mobile width without scaling text into illegibility.

## Motion

Reliable observed curves:

```css
--arrive: cubic-bezier(.22, 1, .36, 1);
--give: cubic-bezier(.24, 1.34, .38, 1);
```

Color and opacity often settle in 160–220 ms. Shape and layout changes commonly take 360–600 ms, with a small content stagger of roughly 25–70 ms. Use 0.96 press compression on ordinary buttons, a little more on small icon controls. Hover motion is local, restrained and interruptible.

Motion spring examples: positional settling around stiffness 380 / damping 34 / mass .7–1; a livelier detail around 500 / 18 / .8; a gentle toggle around 170 / 21.5 / .9. Match the spring to the object's weight and role rather than using one preset for everything.

## Behavior that carries the style

- Preserve identity and an anchor as a pill becomes a menu or a button opens a modal.
- Let neighboring items respond: selected options make room, cards advance into a vacated depth and expanding images redistribute width.
- Make related properties follow one driver. A completion value can control checkbox fill, check drawing and strike-through.
- While held, follow the pointer directly; use momentum and springs to settle after release. Normalize input coordinates when content is scaled.
- Keep geometry coherent. An elastic thumb can lengthen and thin reciprocally; a shape's growth should stay within its container.
- Give a completed action a short landing: a check, count change, small deformation or relevant status color.
- Include equivalent focus and keyboard paths, explicit open/selected values, reversible local interactions and reduced-motion behavior.

The accepted header combines a logo/workspace switcher, unread bell and profile chip. Each opens a native dialog anchored below its trigger with a short expansion and slight content stagger. Workspace and profile saves update the header. Notification actions update the badge. Escape and outside click dismiss. Its source is in `assets/soft-header.html`; borrow relevant relationships rather than copying its whole interface into unrelated components.

`assets/bencho-tokens.css` is the original free token file with its MIT notice; it is an optional output asset. Its dark `--bg` is pure black whereas the live site's canvas was `#0a0a0a`. The catalog lookup returns pattern-specific defaults when needed. Source photos were not included in the public free repository.
