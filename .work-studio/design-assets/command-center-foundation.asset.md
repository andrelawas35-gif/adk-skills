# asset.design.command-center-foundation Asset Record

**Work Object:** `2026-08-22-037`  
**Pipeline:** `references/DESIGN-ASSET-PIPELINE.md`  
**Status:** draft  
**Asset ID:** `asset.design.command-center-foundation`  
**Asset kind:** foundation  
**Source of truth:** this asset record, composed from a token-inventory discovery of tools/ws/command_center.py's inline styles, with three naming decisions confirmed by the director on 2026-08-22  
**Projection status:** projections may read this record; they are read-only and must not be edited as asset truth.

## Asset Summary

The first governed design foundation in this repo, naming every raw CSS
value discovered in `tools/ws/command_center.py`'s inline `<style>` block as
a semantic token. Greenfield composition — no prior foundation existed to
inherit from. This record organizes and names existing values; it does not
yet change any code. Two consolidations were confirmed by the director
during composition (see Decisions below) as intentional forward-looking
choices, each creating a small, explicitly tracked divergence between this
record and the current code until implementation reconciles them.

## Foundation Tokens

### Color

| Token | Value | Currently used at |
|---|---|---|
| `color.text.primary` | `#1a1a1a` | body / h1 text |
| `color.text.muted` | `#666` | 7 places: `.section-label`, `.id`, `.cons`, `.stale`, `.attn`, `.card-link`, `.count-empty` |
| `color.danger` | `#b91c1c` | `.cons-high`, `.card-flag` |
| `color.bg.page` | `#fff` | page background |
| `color.bg.chip` | `#eee` | `.pill`, `.count-pill` backgrounds |
| `color.bg.warning` | `#fff7ed` | `.banner` |
| `color.text.warning` | `#92400e` | `.banner` |
| `color.bg.danger-soft` | `#fef2f2` | `.banner.danger` |
| `color.text.danger-strong` | `#991b1b` | `.banner.danger` |
| `color.border.hairline` | `#ddd` | `.row` divider |
| `color.border.default` | `#e5e5e5` | `.summary-card` border |

**Consolidation (Decision 1, closed by Decision 2):** `color.text.subtle`
(`#555`, previously only `.count-pill`) is retired into `color.text.muted`
(`#666`). `.count-pill` still renders `#555` in code as of this record;
Decision 2 confirms the code should change to `#666` rather than reversing
the consolidation — implementation is routed, not yet applied.

### Typography

| Token | Value |
|---|---|
| `font.family.base` | `-apple-system, sans-serif` |
| `font.family.mono` | `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace` (fallback stack added by Decision 2; previously bare `monospace`, not yet reflected in code) |
| `size.xl` | `20px` (h1) |
| `size.lg` | `18px` (`.card-total`) |
| `size.md` | `13px` (`.section-label`, `.row`, `.banner`, `.card-title`) |
| `size.sm` | `12px` (`.id`) |
| `size.xs` | `11px` (`.pill`, `.cons`, `.stale`, `.attn`, `.count-pill`, `.count-empty`, `.card-flag`, `.card-link`) |
| `weight.medium` | `500` |
| `weight.semibold` | `600` |

### Spacing

Kept exactly as discovered — director confirmed no rounding to a stricter
grid.

| Token | Value |
|---|---|
| `space.1` | `4px` |
| `space.2` | `6px` |
| `space.3` | `8px` |
| `space.4` | `10px` |
| `space.5` | `12px` |
| `space.6` | `14px` |
| `layout.gap.md` | `1rem` |
| `layout.gap.lg` | `1.25rem` |
| `layout.gap.xl` | `2rem` |

### Other

| Token | Value |
|---|---|
| `radius.sm` | `6px` |
| `radius.md` | `8px` |
| `border.width.default` | `1px` |

**Standardization (Decision 1, closed by Decision 2):** `border.width.default`
(`1px`) replaces the two-width split. `.row`'s divider still renders `0.5px`
in code as of this record; Decision 2 confirms the code should change to
`1px` rather than reversing the standardization — implementation is routed,
not yet applied.

**Not yet covered by this foundation** (carried forward from the discovery,
not resolved here): dark-mode variants, responsive breakpoints, animation/
transition tokens. Expanding coverage is a separate future decision, per
this Work Object's non-goals.

## Lifecycle

| Step | Owning skill | Evidence |
|------|--------------|----------|
| Intake and identity | `design-manage-assets` | Composed from a token-inventory discovery (`design-build-design-foundation`); current frontier is `foundation`, owned by `design-compose-design-system`. |
| Foundation composition | `design-compose-design-system` | Naming and the two consolidation/standardization decisions confirmed by the director, WO `2026-08-22-037` Decision 1. |
| Grilling session (breadth-sweep, 3 branches) | `design-compose-design-system` | All three open properties (`.count-pill` color, `.row` border, mono fallback stack) grilled and resolved by the director, WO `2026-08-22-037` Decision 2. All resolved to "update code." |

## Verification Notes

- This record composes and names tokens; it does not itself verify that
  code matches these names. `design-apply-design-direction` and
  `design-verify-design-implementation` own confirming and verifying any
  future code change against this foundation.
- Three explicit gaps exist between this record and current code
  (`.count-pill`'s `#555`, `.row`'s `0.5px` border, bare `monospace`) and are
  named above, not silently absorbed as if code already matched. All three
  are confirmed (Decision 2) to be closed by updating code, not the record.
- Code has not yet been changed — routed to `alawas-engineering-implement-bounded-change`.
- This is a draft proposal, not yet an accepted canonical foundation.

## Rollback

Delete this draft asset record if it has not been accepted. If accepted
later, retire it through the governing Work Object instead of deleting
history.
