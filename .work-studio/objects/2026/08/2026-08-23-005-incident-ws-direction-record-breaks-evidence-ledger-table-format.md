---
schema_version: 1
id: 2026-08-23-005
title: Incident: ws direction --record breaks Evidence ledger table format
type: incident
status: active
state: observe
consequence: meaningful
sensitivity: ordinary
domain: [operations, engineering]
created_at: 2026-08-23T23:47:34Z
updated_at: 2026-08-24T03:19:41Z
next_action: Observation window: next real Scene Object direction recording must produce a valid single-line Evidence ledger row and pass ws validate; close the incident only after that real-corpus recording confirms recovery.







---
## Intent

Incident record for the evidence-writer defect: `ws direction --record` embeds
multi-line `format_direction()` output into a single Evidence ledger table row,
breaking the markdown table format and tripping `ws validate`. Surfaced by the
SC030 V0 tracer (WO 2026-08-23-004), reported on WO 2026-08-23-001. This object
frames the incident, preserves the verified diagnosis, and routes prevention to
a bounded linked Change Work Object (WO 2026-08-23-006). The incident stays
open until the affected path (`ws direction --record`) is restored and verified.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [ ] Incident is framed with verified diagnosis, containment, and routed prevention recorded.
- [ ] Bounded linked Change Work Object exists with `responds_to` this incident.
- [ ] Affected path (`ws direction --record`) writes valid single-line Evidence ledger rows and `ws validate` passes on a recorded Direction.
- [ ] Incident transitions to `observe` only after affected-path recovery is verified on the real command, not on a proxy signal.


## Constraints and non-goals

**Constraints:**
- Preserve sanitized evidence only; no raw logs, secrets, or customer content.
- Keep containment, restoration, diagnosis, and prevention distinct.
- Do not implement the fix inside this incident; route it to the Change Work Object.

**Non-goals:**
- No code changes in this Work Object.
- No claim of recovery until the affected path is verified.
- No closure of the incident on containment alone.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Confirm evidence-writer defect and route prevention to a bounded Change Work Object

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | The finding is a confirmed defect, not a hypothesis: root-cause mechanism reproduced in-memory (multi-line `format_direction()` embedded verbatim into one Evidence ledger row). Containment already applied on WO 2026-08-23-004 (manual single-line repair). Prevention routed to a separate linked Change Work Object (WO 2026-08-23-006, `responds_to`). |
| **Authorization** | Director: "do both" (2026-08-23). |
| **Confidence** | high — mechanism reproduced and validator behavior confirmed. |
| **Actor** | director + conductor |
| **Revisit trigger** | If the Change Work Object's fix cannot make `ws direction --record` write a valid single-line row without losing required structured detail, reopen the fix approach. |
| **Rationale** | Confirmed defects get routed to bounded change work rather than being fixed inline or silently converted; the incident remains open until affected-path recovery is verified. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | in-memory reproduction | Reproduced: format_direction() returns a multi-line string (Direction header plus Protect, Change, Avoid lines) and generate_evidence_entry() embeds it verbatim into one Evidence ledger table row, so only line 1 stays inside the table and the structured-field lines leak out below it. |
| [system] | tools/ws/validate.py + cmd_direction | Affected path confirmed: ws validate Evidence ledger structural check flags any non-pipe-prefixed line after the table header (SC030 reported lines 6-8). The general append-evidence path exposes the same seam when --text is multi-line. |
| [testimony] | WO 2026-08-23-001 / WO 2026-08-23-004 | SC030 V0 tracer (WO 2026-08-23-004) surfaced the defect; it is recorded on WO 2026-08-23-001 Evidence ledger and its next_action. The affected row on WO 2026-08-23-004 was manually repaired to a single-line row (newlines replaced with br tags). |
| [decision] | director | Director authorized opening this Incident Work Object and creating a bounded linked Change Work Object (responds_to) for the fix, 2026-08-23 (do both). |
| [system] | Change WO 2026-08-23-006 | Affected-path recovery verified: Change WO 2026-08-23-006 implemented Decision 1 (single-line evidence serialization) and passed end-to-end in an isolated temp workspace — ws direction --record wrote ONE valid 3-cell Evidence ledger row and ws validate passed all checks; append-evidence multi-line text is also normalized. Incident remains open for observation, not closed. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

Change WO `2026-08-23-006` fixes `ws direction --record` evidence serialization
to single-line ledger rows; incident stays open until affected-path recovery is
verified on the real command.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-23T23:48:17Z — Open Incident: evidence-writer defect framed and routed to bounded Change work

- **State:** notice
- **Status:** active
- **Actor:** conductor
- **Rationale:** Diagnosis verified (root-cause mechanism reproduced in-memory; validator flags the broken rows). Containment was already applied on WO 2026-08-23-004 (manual single-line repair). Affected path (ws direction --record) is NOT yet restored. Prevention routed to a bounded linked Change Work Object (responds_to).
### 2026-08-24T03:19:41Z — Affected-path recovery verified; incident to observe (not closed)

- **State:** observe
- **Status:** active
- **Actor:** conductor
- **Rationale:** Change WO 2026-08-23-006 implemented Decision 1 and verified the affected path end-to-end: ws direction --record writes a valid single-line Evidence ledger row and ws validate passes. Per incident skill, recovery-verified incidents transition to observe with a bounded observation window and are NOT closed.
