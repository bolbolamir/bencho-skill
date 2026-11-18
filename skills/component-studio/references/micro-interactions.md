# Micro-interaction specialist

Run this pass after the main agent has built a working component, before the finished revision is registered. Implement warranted refinements in the actual component; do not stop at suggestions when changes are needed. If the existing choreography already satisfies the brief, return concrete observations supporting that judgment instead of adding redundant effects. Work only in the handed-off working files and preserve the brief, accepted design, functionality and public API. Do not register a gallery version; the main agent owns integration and saving.

## Read the component as a system

Read `design-language.md`, `preview-workflow.md`, the component source and the main agent's handoff. Use `scripts/reference.py` with a few relevant pattern names to find Bencho examples; do not load the entire catalog.

Make a compact element/state map in working notes. Include each visible element, its role, the states that affect it and the reason it should move or stay still. Account for the trigger surface, icon, label, value/badge, indicator, border/shadow, container, siblings and revealed content when present. Static anchors are deliberate choices; considering every element does not mean animating every element.

For each supported interaction, trace input → immediate acknowledgment → state change → related responses → settled result. Include cancellation and reversal. Identify the shared state or progress value that should drive related properties. Derive feedback from the real state change, rather than running an unrelated decorative timeline. Preserve any effective choreography already present in a refinement.

## Give the interaction a physical logic

Use the following prompts for the component's actual interactions, without adding unrelated gestures or effects:

| Interaction | Relationships to consider |
| --- | --- |
| Tap / press | Where does the surface yield? Does its icon or label respond with the surface or slightly after it? Distinguish pointer-down, activation, release outside and cancellation. Do not commit a click action on pointer-down merely to make feedback feel faster. |
| Tab / segmented selection | Preserve the moving indicator's identity as position and width change. Coordinate selected text/icon emphasis, directional content movement and container resizing when relevant. Each option keeps its local state when another is selected; returning restores its selected item, input values, expansion and scroll position where present. Keep a stable reading anchor. Distinguish keyboard focus from selection and preserve the component's activation model. |
| Swipe / drag | Follow the pointer directly while held. Let distance and, where appropriate, release velocity determine commit versus return. Coordinate the foreground item, underlying item, depth, exposed action and position indicator. Settle from the actual release position; a cancelled gesture must restore the prior state. Respect the scrolling axis and provide a non-gesture path. |
| Actions: save, toggle, complete, remove, expand | Connect trigger feedback to the changed icon, label, count, status, progress, empty space and affected neighbors. Preserve an anchor through expansion. Let removal's neighbors close the gap coherently. Show pending, success or error only when those states exist; success follows a successful result. |

Borrow the motion ranges and material logic from `design-language.md`, then tune to the object's role and distance. Give related elements a clear order and shared driver, with small offsets only when they help the user follow the action. Avoid a uniform bounce, stagger, blur or particle treatment across every element. A completion accent should belong to the action and resolve quickly.

Keep animations interruptible. Rapid taps, a new tab target or a reversed swipe should continue from the current presentation toward the latest state without snapping to the original start. Cancel stale animations, timers and completion callbacks so they cannot overwrite newer state. Do not let transform-only movement leave focus, hit targets or layout inconsistent with what is visible. Input must remain usable during settling.

For tabs and comparable option switches, make the change fast but visibly followable: usually around 160–240 ms for content and its related elements, with a small directional displacement or shared geometry movement. An instant content swap or an opacity-only fade does not satisfy the user's preference when spatial movement is appropriate. Avoid long exit-then-enter sequences, large travel or animation locks. Keep the stateful panel mounted when practical; otherwise retain its state outside the visual tree under a stable key and restore it on return. A dataset change may require a new valid selection, but a tab click alone must not reset it.

## Bencho relationships to study

These are references for relationships, not a requirement to copy an effect. The local catalog records the research coverage; descriptions and stills do not establish exact spring settings or implementation details. Inspect an available live preview or public source when that detail matters. If unavailable, identify the motion as your interpretation.

| Reference | What it suggests | Evidence available in the studio audit |
| --- | --- | --- |
| [Like](https://bencho.dev/blocks/like) | One action links heart deformation, a local accent and a rolling count. | Free: live + public source studied. |
| [Liquid toggle](https://bencho.dev/blocks/liq-toggle) | The thumb's travel and directional stretch describe one moving material. | Free: live + public source studied. |
| [Card stack](https://bencho.dev/blocks/card-stack) | The chosen card and surrounding deck change their arrangement together. | Free: live + public source studied. |
| [Jelly tabs](https://bencho.dev/blocks/jelly-tabs) | A selection pill changes size and position while retaining its identity. | Pro: still + description; exact implementation unverified. |
| [Swipe deck](https://bencho.dev/blocks/swipe-deck) | A released foreground card cycles behind the deck, implying a coordinated change in order. | Pro: still + description; exact implementation unverified. |
| [Progress tracker](https://bencho.dev/blocks/progress-tracker) | Task completion connects the check, text, count, bar and final completion accent. | Pro: still + description; exact implementation unverified. |

The accepted `assets/soft-header.html` is also a local reference for an anchored trigger, expanding dialog, staged content and state that updates the header.

## Handoff to the specialist

The main agent should supply concrete paths and the supported interactions, for example:

```text
Act as the Component Studio micro-interaction specialist. The functional build
is ready. Read <skill-dir>/references/micro-interactions.md and its required
context, then implement the pass in the working files below.

Brief and accepted design: <request and constraints>
Working files you may edit: <absolute paths>
Preview / verification: <URL or command, component id if available>
Supported interactions and real state: <actions, gestures, data/backend limits>
Existing checks / known limitations: <what was checked and what remains>

Consider every element and coordinate the supported tap, tab, swipe and action
states. Keep scope and function intact. Do not edit saved revisions or register
a version. Return changed paths, a concise interaction/element map, the Bencho
references used, checks actually performed and any unresolved limits.
```

Usually one specialist owns this pass so the motion stays coherent. Split work among specialists only for independent components with disjoint files, then review the combined behavior.

## Review before saving

The specialist checks the edited component; the main agent reviews the integrated result. Use the browser when available and distinguish source inspection from behavior actually exercised. For the interactions that exist, check:

- The primary action, its visible state changes and the settled result. Inspect intermediate movement as well as the final frame; labels, clipping, stacking and neighbors must remain coherent.
- Rapid repetition and reversal, dismissal/reopening, interrupted settling, and pointer cancellation or release outside. For gestures, check short returns, committed swipes and ordinary scrolling.
- Switch away from an option and back after changing its local state. Confirm the same item, values, expansion and scroll position return where applicable. Check the transition at normal speed: movement is visible, quick and responsive to a new target before it settles.
- Keyboard operation, visible focus, correct selected/expanded/pressed values and focus return where appropriate. Keep swipe alternatives usable and avoid announcing every animation frame to assistive technology.
- Reduced motion: remove elastic travel, overshoot, particles and unnecessary stagger; preserve immediate state feedback and functional gestures. The state must not depend on an animation finishing or a `transitionend` event firing.
- Narrow layout in resting and expanded/changed states, and supported themes. Keep geometry inside its bounds, text readable and interactive targets aligned with their visual position.

Resolve regressions before registration. If live behavior cannot be exercised, report that limit and the source-level checks actually completed. The gallery's `check` command validates saved files; it does not validate motion quality or interaction behavior.
