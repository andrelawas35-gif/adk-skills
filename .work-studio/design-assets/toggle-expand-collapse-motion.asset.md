# asset.design.toggle-expand-collapse-motion Asset Record

**Work Object:** `2026-08-22-032`  
**Pipeline:** `references/DESIGN-ASSET-PIPELINE.md`  
**Status:** draft  
**Asset ID:** `asset.design.toggle-expand-collapse-motion`  
**Asset kind:** motion  
**Source of truth:** hand-authored draft; timing/easing/reduced-motion confirmed via a live breadth-sweep Grilling Session on WO `2026-08-22-038`, 2026-08-22; not yet a real implemented motion behavior  
**Projection status:** projections are read-only and must not be edited as asset truth.

## Asset Summary

Governed motion recipe for the "Show closed" / "Hide closed" toggle in
`.work-studio/command-center.html`. Currently the closed-Work-Objects section
snaps open/closed instantly via `display: none` / `display: block` (see
`tools/ws/command_center.py`) — this record proposes replacing that with an
eased transition, without committing to any code change yet. This is the
first real (non-tempfile) use of the `motion` asset kind added to
`VALID_ASSET_KINDS` during WO `2026-08-22-032`'s schema-capacity tracer.

**Confirmed recipe** (via live breadth-sweep Grilling Session, WO
`2026-08-22-038`, all three questions posed as multiple-choice, no
open-ended prompts):

- **Duration:** 150ms
- **Easing:** `ease-in-out`
- **Reduced-motion behavior:** when `prefers-reduced-motion` is set, shorten
  to 50ms rather than removing the transition entirely — motion is
  minimized, not eliminated.

## Lifecycle

| Step | Owning skill | Evidence |
|------|--------------|----------|
| Intake and identity | `design-manage-assets` | Hand-authored draft record; current frontier is `identity`, awaiting classification. |
| Motion composition | `design-govern-interaction-motion` | Duration, easing, and reduced-motion behavior confirmed via breadth-sweep Grilling Session, WO `2026-08-22-038`. |

## Verification Notes

- This is a draft record, hand-authored directly (not through `ws asset-ingest`), to test manual authoring against the registry schema.
- Timing, easing, and reduced-motion behavior are now confirmed via a live breadth-sweep Grilling Session (WO `2026-08-22-038`), testing the combined mandatory-nomination + breadth-sweep grilling mechanism against a real, already-pending decision.
- No code change has been made to `command-center.html`; the toggle still behaves exactly as before. Implementing this recipe in code is a separate step via `design-apply-design-direction`.

## Rollback

Delete this draft asset record if it has not been accepted. If accepted
later, retire it through the governing Work Object instead of deleting
history.
