# ReviewBadge Create-Review-Approve Experience-Pattern Stewardship Record

**Work Object:** `2026-08-22-017`  
**Skill:** `design-steward-experience-patterns`  
**Asset:** `asset.design.reviewbadge` (component-family, status `active`)  
**Pattern:** `create-review-approve` (ux-pattern)  
**Deliverable type:** experience-pattern stewardship record  

## Pattern goal

Confirm the reusable behavior preserved by the ReviewBadge across visual
themes and implementations: an item's review status must be readable at a
glance, non-color signals must carry the urgent state, and status meanings
must not change between themes.

## States and required behavior

| State | User meaning | Required badge behavior |
|-------|--------------|-------------------------|
| `draft` | Work exists but is not ready for review. | Label `Draft`; low emphasis. |
| `in_review` | Work is waiting for a reviewer decision. | Label `In review`; active but not final. |
| `approved` | Work passed review. | Label `Approved`; positive but not celebratory. |
| `blocked` | Work cannot proceed without recovery. | Label `Blocked`; urgent, must include non-color contrast. |

## Accessibility and content expectations

- The `blocked` state must not rely on color alone; the composition record's
  bold border and label carry the non-color signal.
- Labels are fixed human-readable status names across themes.

## Evidence links

- Behavior declarations originate in `reviewbadge.asset.md` (UX Pattern
  section), accepted to `active` on 2026-08-22.
- Composition proposal: `.work-studio/deliverables/2026-08-22-017-reviewbadge-editorial-contrast-composition.md`.

## Authority boundary

This record does not style the pattern, choose visual themes, implement code,
or claim accessibility compliance from a written pattern alone. Any
accessibility claim would require verification against a rendered badge and
scoped authority.

## Gaps

- No rendered badge exists yet, so contrast and non-color-signal expectations
  are unverified behavior, not confirmed accessibility.
