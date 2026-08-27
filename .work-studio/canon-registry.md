# Canon Registry

<!--
  Approved production artifacts for the Director Console (WO 2026-08-24-006,
  Decision 3). A Component-Ledger-pattern index: the approved Shot Work Object
  (shot_status: approved + History) IS the canon record; this index is a
  derived pointer list for discoverability. The design-asset pipeline is
  design-domain (asset.design.* ID prefix, design-only kinds/statuses/
  owning-skills) and does not hold production artifacts.

  Entry schema: canon-id; artifact (shot WO + shot status); tier; scene /
  sequence / project placement; approved-at; approved-by; depends-on;
  depended-on-by; notes. Status values: canon | superseded | retired.
  Entries are pointers to the approved Shot WO, never copies. Retired entries
  are preserved, never deleted.
-->

## CANON-001 — SH001 market establishing (approved)

- **artifact:** Shot `2026-08-24-009` (SH001 — Shot 01 market establishing)
- **canon status:** canon
- **shot status:** approved (via `ws shot-status`, V1 shot state machine)
- **tier:** hero
- **placement:** Scene SC030 `2026-08-23-004` → Sequence SQ001 `2026-08-24-008` → Project P001 `2026-08-24-007`
- **approved at:** 2026-08-25T00:18:16Z (shot_status transition to approved)
- **approved by:** director (director-directed V1 build-out, WO `2026-08-24-010`; approval of the shot's production state via the shot state machine)
- **depends-on:** Scene SC030 `2026-08-23-004`
- **depended-on-by:** none yet
- **notes:** First director-approved canon entry — SH001 reached approved via
  the shot state machine (blocking → animation → render → review → approved)
  under the director-directed V1 build-out. The approval is of the shot's
  production state, not a director's visual render review (renders arrive in
  V3/V4). The approved Shot WO is the source of truth; this entry is a pointer.

## CANON-002 — SH002 Leo approaches (approved)

- **artifact:** Shot `2026-08-24-011` (SH002 — Shot 02: Leo approaches)
- **canon status:** canon
- **shot status:** approved (via `ws shot-status`, V1 shot state machine)
- **tier:** hero
- **placement:** Scene SC030 `2026-08-23-004` → Sequence SQ001 `2026-08-24-008` → Project P001 `2026-08-24-007`
- **approved at:** 2026-08-25T01:53:17Z (shot_status transition to approved)
- **approved by:** director-directed V1 build-out (WO `2026-08-24-010`)
- **depends-on:** Scene SC030 `2026-08-23-004`
- **depended-on-by:** none yet
- **notes:** Second director-approved canon entry — SH002 reached approved via
  the shot state machine under the director-directed build-out; approval of
  the shot's production state (visual render approval deferred to V3/V4).
  The approved Shot WO is the source of truth; this entry is a pointer.

## CANON-003 — SH003 the name lands (approved)

- **artifact:** Shot `2026-08-24-012` (SH003 — Shot 03: the name lands)
- **canon status:** canon
- **shot status:** approved (via `ws shot-status`, V1 shot state machine)
- **tier:** hero
- **placement:** Scene SC030 `2026-08-23-004` → Sequence SQ001 `2026-08-24-008` → Project P001 `2026-08-24-007`
- **approved at:** 2026-08-25T02:02:38Z (shot_status transition to approved)
- **approved by:** director-directed V1 build-out (WO `2026-08-24-010`)
- **depends-on:** Scene SC030 `2026-08-23-004`
- **depended-on-by:** none yet
- **notes:** Third director-approved canon entry — SH003 reached approved via
  the shot state machine under the director-directed build-out (finishing the
  in-flight shot); approval of the shot's production state (visual render
  approval deferred to V3/V4). The approved Shot WO is the source of truth;
  this entry is a pointer.
