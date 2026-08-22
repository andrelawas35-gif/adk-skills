# ReviewBadge Editorial-Contrast Composition Record

**Work Object:** `2026-08-22-017`  
**Skill:** `design-compose-design-system`  
**Asset:** `asset.design.reviewbadge` (component-family, status `active`)  
**Deliverable type:** design-system composition record for the confirmed creative direction  
**Confirmed creative direction:** director, 2026-08-22 — compose the `editorial-contrast` theme recipe: *"Stronger visual contrast for review-heavy editorial systems: higher contrast text and borders."*

## Composition scope

This record composes the `editorial-contrast` theme for the ReviewBadge
component family from the semantic tokens declared in
`reviewbadge.asset.md`. It states which properties are inherited, overridden,
and prohibited. It is a composition proposal; it does not apply any visual
implementation.

## Inherited (from the foundation/record)

- Status names: `draft`, `in_review`, `approved`, `blocked`.
- Label rules: `Draft`, `In review`, `Approved`, `Blocked`.
- Radius range: `4px` or `6px`; composed at `4px` (no creative confirmation
  needed inside the declared range).

## Overridden (higher contrast text and borders)

| Token | `draft` | `in_review` | `approved` | `blocked` |
|-------|---------|-------------|------------|-----------|
| `review.badge.background` | `#f8fafc` light gray | `#eff6ff` light blue | `#f0fdf4` light green | `#fef2f2` light red |
| `review.badge.text` | `#111827` near-black | `#111827` | `#111827` | `#111827` |
| `review.badge.border` | `#64748b` `2px` | `#2563eb` `2px` | `#16a34a` `2px` | `#b91c1c` `2px` |
| `review.badge.radius` | `4px` | `4px` | `4px` | `4px` |
| `review.badge.label` | `Draft` | `In review` | `Approved` | `Blocked` |

Design intent: light status-tinted surfaces keep each state's semantic hue
while dark near-black text and `2px` borders raise contrast for dense editorial
review reading. The `blocked` state adds a bold border and the declared
non-color contrast signal.

## Prohibited (unchanged)

- Changing status meanings.
- Hiding the `blocked` state.
- Using color as the only signal (`blocked` must include non-color contrast).

## Authority boundary

This record does not authorize implementation, browser rendering, export,
component-ledger registration, or external design-tool sync. The concrete
values above are the composition proposal under the confirmed direction; they
are presented for the director's review before any implementation.

## Verification needs

Before any implementation, the composition should be checked by
`design-verify-design-implementation` against a rendered ReviewBadge for text
contrast on each surface and the required non-color signal for `blocked`.
