# Bencho component builder reference

Studied 17 November 2026. Reference: [bencho.dev](https://bencho.dev/). This records the user's requested design direction for future component builds in this workspace.

The design read: compact, neutral product interfaces with soft geometry and expressive physical behavior. Most surfaces are quiet; the interaction supplies the personality. New components should look plausible beside the reference examples and respond with the same attention to geometry, timing and nearby elements.

## Coverage and evidence

Every one of the **169 entries** in the site's public catalog was opened individually. The review recorded the preview, explanation, interaction category and exposed controls. **47 entries** exposed live free components and have corresponding public source folders. **122 entries** displayed Pro preview images; their motion is described by the site but could not be freely exercised in this session. Exact Pro implementation and timing are unverified.

For the free set, 46 guided demonstrations were started and sampled; Label input was exercised directly. Additional direct checks verified pointer and keyboard toggling, checklist completion and counter stepping. This is design research, not exhaustive browser or accessibility testing. A direct automated drag did not establish Slide to confirm's completed state; its behavior below is grounded in public source and description.

Sources: [catalog](https://bencho.dev/), [free component repository](https://github.com/cabralorenzo/bencho), [theme tokens](https://github.com/cabralorenzo/bencho/blob/main/tokens.css). Repository snapshot: `c65992417427bb09e661674ffa800bef29adef49`. The separately saved [component index](bencho-component-index.md) covers every entry, with a link to its own page and an explicit evidence label.

## Color and material

The light theme is subtly warm. The dark theme uses mostly neutral black and gray. The main contrast is between surface levels, with restrained outlines and low-opacity washes. Bright colors belong principally to photos, avatars, data categories, selected content or status.

| Role | Light | Dark |
| --- | --- | --- |
| Website background | `#ffffff` | `#0a0a0a` |
| Surface | `#f7f7f6` | `#0f0f0f` |
| Surface 2 | `#f1f1f0` | `#181818` |
| Surface 3 | `#ecebe7` | `#202020` |
| Board | `#ffffff` | `#1a1a1a` |
| Primary ink | `#17181a` | `#ffffff` |
| Secondary ink | `#3c3b37` | `#b4b4b4` |
| Tertiary ink | `#5c5b56` | `#9a9a9a` |
| Muted ink | `#6f6e68` | `#828282` |
| Faint ink | `#85847e` | `#6b6b6b` |
| Selection blue | `#0d99ff` | `#3aa9ff` |
| Signal/focus | `#2231dd` | inherited `#2231dd` in free tokens |
| Success | `#15803d` | `#34d17a` |

Values above come from the public stylesheet and free tokens. The free package's dark `--bg` is `#000000`; the live website uses `#0a0a0a`. Preserve that distinction when choosing between a component theme and a website canvas. The [saved token file](bencho-tokens.css) is the official free-component version, with its original license.

Surface construction often uses a base plus a translucent ink wash. A light wash is commonly 6%; the live site's dark wash is about 5.3%, while the free token file uses 9%. These layers are intentionally distinct. Selected controls gain local contrast. Hover often changes a fill by a few percentage points. Borders can be an inset one-pixel shadow. Saturated gradients are specific to an orb, photo, data display or effect rather than a global backdrop.

Glass is a component material where needed: a lens, sheen, refraction, rim light or translucent control. Many ordinary cards remain flat. Edge highlights, surface contrast and shadow should describe actual depth.

## Typography

The website uses **Inter** for interface text and **Plus Jakarta Sans** first in its display stack. Its other declared fallbacks include Google Sans, Maison Neue and Instrument Sans. Numeric and ordinary interface text share the same family; numeric displays often use tabular figures. Code has a separate system monospace stack.

Common observed sizes in component styles:

| Use | Typical size |
| --- | --- |
| Tiny numeric/metadata labels | 11–12 px |
| Compact buttons, tags and controls | 12–14 px |
| Item titles and primary body text | 14–16 px |
| Inspector title | 18–19 px |
| Metric, amount or time | 30 px |

Weights are usually 400 and 500; the page heading uses 600. The observed heading at the default browser width was 38 px with a 1.05 line height and `-0.022em` tracking. Large numerical displays commonly tighten tracking to about `-0.03em`. Component text remains compact and readable, without large typographic jumps. Keep a stable numeric baseline while individual digits animate.

## Spacing and geometry

There is no single radius or rigid spacing value for everything. The consistency comes from related sizes and nested proportions.

| Relationship | Observed examples |
| --- | --- |
| Small internal separation | 2, 4, 6, 8 px |
| Icon-to-label or related content gap | 8–12 px |
| Major internal group gap | 12–16 px |
| Typical card padding | 16–20 px |
| Gallery gap at observed width | 12 px |
| Gallery and inspector surfaces | 28 px radius |
| Many component cards | 20 px radius |
| Photo card or smaller inset | 10–17 px radius |
| Pills and circular controls | fully rounded |

Specific examples matter: Card stack starts at a 14 px corner, Palette at 14 px, Now playing at 16 px, Like at 22 px, Search at 24 px and Slide to confirm at 28 px. Toast stack exposes a 14 px collapsed peek and a 10 px expanded gap. Card padding, inset radii and image corners must agree visually.

The gallery gives a small control abundant surrounding space. Preserve the distinction between the demonstration frame and the component itself: the component should retain useful intrinsic dimensions and adapt to its actual container. A rounded gallery tile is not part of every component's production API.

## Motion vocabulary

Two repeatedly observed CSS curves are strong anchors:

```css
--ease-arrive: cubic-bezier(0.22, 1, 0.36, 1);
--ease-give: cubic-bezier(0.24, 1.34, 0.38, 1);
```

The first front-loads movement and eases into place. The second adds restrained overshoot. Each component still has its own tuning. These are observed reference values, not a claim that Bencho exposes official global variables with these names.

| Change | Repeated source examples |
| --- | --- |
| Small color, opacity or hover feedback | 160–220 ms |
| Local transform or tooltip | 160–420 ms |
| Width, shape or layout transition | 420–600 ms |
| Character/column or item stagger | around 40–70 ms in several examples |
| Card stack selected viewer | 920 ms in; 660 ms out |

Actual source spring examples:

```ts
// Toast stack and several related positional changes.
{ type: "spring", stiffness: 380, damping: 34, mass: 1 }

// A livelier avatar/menu detail; mass varies by element.
{ type: "spring", stiffness: 500, damping: 18, mass: 0.8 }

// Create menu's liquid shape.
{ stiffness: 220, damping: 14, mass: 0.5 }

// Liquid toggle at its default speed.
{ type: "spring", stiffness: 170, damping: 21.5, mass: 0.9 }
```

Use these as starting points only when the moving object is comparable. A toggle has gentler settling than a playful avatar insertion. A heavy card, tooltip and number column should not all move identically.

Several free components implement a shared custom spring pattern with `k = 0.08 + tune/100 * 0.16` and per-frame decay `d = 0.62 + tune/100 * 0.2`. Decay is exponentiated by elapsed frame time. The loop parks when settled, and interruption resumes from the current position and velocity. This frame-based model is distinct from Motion's physical-unit stiffness values.

## Interaction principles to carry into new work

1. **Maintain the object's identity.** Search grows from its icon; Create menu expands from its pill; the player grows from its compact bar. Keep an anchor and a recognizable silhouette through the transition.
2. **Make neighbors participate.** An enlarged selection displaces neighboring choices. Expanded photos redistribute width. The next card moves into the previous card's depth. This surrounding response is a major part of the feel.
3. **Keep physical quantities coherent.** The liquid toggle lengthens along its velocity and uses reciprocal perpendicular scale to retain area. Aspect ratio preserves image area. Confirmation geometry is derived so the expanding handle stays inside its track.
4. **Derive related movement from one driver.** Checkbox fill, check and strike-through share a completion value. One spring can drive width, height and corner; secondary content can enter on its own short opacity schedule.
5. **Respond immediately to the hand.** While held, follow the pointer. Use the spring for settling after release. Derive flings from recent velocity and normalize client coordinates when a preview is scaled.
6. **Use a local influence field.** Docks, letters, images, dots and rulers respond most strongly near the cursor, with a gentle falloff across neighbors.
7. **Treat press as a material change.** Many ordinary buttons compress to roughly 0.96; some smaller controls use 0.90–0.92. A tiny control's exaggeration can be stronger than a whole card's.
8. **Sequence meaning.** Labels can leave before a sidebar contracts. Counts update with the selection. New content follows the space made for it. Exit and return should have clear destinations.
9. **Support interruption.** Rapid retargeting should continue from the visible state. Avoid stacking competing CSS transforms and animation controllers on the same element.
10. **Let completion land.** A small check, count change, brief deformation or semantic color gives closure. Elaborate particles belong to explicitly celebratory interactions.

The source's mechanical examples are particularly useful: [Liquid toggle](https://bencho.dev/blocks/liq-toggle), [Magnetic select](https://bencho.dev/blocks/magnet-select), [Image accordion](https://bencho.dev/blocks/image-accordion), [Checklist](https://bencho.dev/blocks/checklist), [Create menu](https://bencho.dev/blocks/liq-create), [Rolling counter](https://bencho.dev/blocks/rolling-counter), [Card stack](https://bencho.dev/blocks/card-stack).

## Actions and state design

For a requested build, define the complete interaction before styling: resting, hover/focus, pressed/held, moving, settling, selected/open, working, completed and error where relevant. Selection needs a real persistent value. A menu needs closing and focus behavior. A slider needs a bounded value and an accessible way to change it. A code field needs paste and deletion behavior. The demo may be visual, but any requested production action must be wired to the intended application behavior.

The demos include simulated actions. The free Upload dropzone uses example files, and Voice note has a demonstration waveform. Do not infer that a demo already contains a production upload or recording service.

The public source uses React, TypeScript, ordinary component CSS and a mix of custom animation, Motion, canvas, Three.js and `liquid-gooey`; Lucide appears in many free components. This is not one standard form-control package with a single interchangeable skin. Choose the smallest implementation that captures the requested behavior and fits the host project.

The source review found a reduced-motion reference in 36 of 47 free blocks. That is evidence of a recurring pattern, not a full accessibility certification. Future builds should include keyboard equivalents, visible focus, useful labels and reduced-motion behavior deliberately. Preserve the interaction's information when reducing travel, blur, physics or particle effects.

Sound is part of the broader site: the free repository contains 24 Web Audio interface sounds. Keep sound optional and associated with a user action. The review read the sound definitions and categories; it did not conduct a listening audit of every sound.

## Builder working agreement

When the user names a component or describes a new interaction:

- Use this reference and the matching entries in the index as the default visual direction.
- Build the requested component and its states, using the host project's stack and conventions. If there is no host project, a self-contained React/TypeScript component with scoped CSS and a preview is a reasonable starting point.
- Carry the neutral palette, compact typography, related radii and physical choreography into new compositions. Adapt the behavior to the actual use case.
- Expose a small set of meaningful tuning controls only where useful: size/corner, speed/settle, reach/pull, count/gap or one material parameter.
- Verify the states that matter in the browser, including rapid retargeting and at least one keyboard path. Check light/dark and reduced motion when provided.
- Reuse public MIT code with its attribution when appropriate. The free repository does not include the site's licensed photos. Exact Pro source requires authorized access; builds based on the public Pro preview should be described as original interpretations.

The project keeps a small `AGENTS.md` pointing here so this direction remains concrete and recoverable in later work. The user's later instructions override these defaults.
