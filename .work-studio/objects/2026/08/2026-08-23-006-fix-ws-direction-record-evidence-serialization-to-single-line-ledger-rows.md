---
schema_version: 1
id: 2026-08-23-006
title: Fix ws direction --record evidence serialization to single-line ledger rows
type: change
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
domain: [engineering, operations]
responds_to: 2026-08-23-005
created_at: 2026-08-23T23:48:24Z
updated_at: 2026-08-24T03:19:16Z
next_action: Route to conduct-work-object: review implementation evidence; transition to observe once affected-path recovery is confirmed on the real command (Incident 2026-08-23-005).









---
## Intent

Fix the evidence writer so `ws direction --record` persists a valid single-line
Evidence ledger row for any parsed Direction, instead of embedding multi-line
`format_direction()` output that breaks the markdown table. This is the bounded
prevention successor to Incident WO 2026-08-23-005 (evidence-writer defect
surfaced by the SC030 V0 tracer, WO 2026-08-23-004).

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] `ws direction --record` writes the Direction as ONE valid Evidence ledger table row (no leaked structured-field lines) for a Direction with Protect, Change, and Avoid populated. (Verified end-to-end in an isolated temp workspace.)
- [x] `ws validate` reports no Evidence-ledger table-format errors on the recorded object. (Verified: all default checks passed.)
- [x] Console output of `ws direction` still shows the multi-line human-readable Direction (display and persistence concerns stay separate). (Verified: console block unchanged.)
- [x] The general `append-evidence` path is protected from multi-line `--text` breaking the table (defense-in-depth, per Decision 1). (Verified: `\n` and `\r\n` normalize to `<br>` in a single cell.)


## Constraints and non-goals

**Constraints:**
- Keep the CLI dependency-free (stdlib only).
- Preserve the multi-line console rendering of a parsed Direction; only the persisted evidence row becomes single-line.
- Route all fixes through the deterministic CLI write path; do not hand-edit existing Evidence ledger rows.

**Non-goals:**
- No change to the Direction object schema or `parse_direction` semantics.
- No change to the Evidence ledger validation rules themselves.
- No deployment or release work in this Work Object.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Adopt single-line evidence serialization: call-site fix first, general guard as defense

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Fix location for the evidence-writer defect (Incident WO 2026-08-23-005). H1: serialize the recorded Direction to a single line at the call site in `cmd_direction` (keep `format_direction` multi-line for console display, add a single-line serialization for the evidence row). H2: guard `generate_evidence_entry` in `tools/ws/sections.py` against multi-line `text` (normalize newlines) so `append-evidence` is protected too. H3 (making `format_direction` itself single-line) rejected: it shares a console-display consumer that wants multi-line. |
| **Authorization** | Director: "do both" (2026-08-23) — authorizes creating this Change WO with the fix accepted as prevention; code implementation proceeds under implement-bounded-change authority. |
| **Confidence** | high for H1 being sufficient for the reported defect; medium for H2's broader behavior change (multi-line evidence rendering) needing a conscious choice. |
| **Actor** | director + conductor |
| **Revisit trigger** | If single-line serialization loses required structured detail for downstream readers, or if H2's normalization changes how existing multi-line evidence renders unexpectedly. |
| **Rationale** | The reported defect is call-site-specific (only `direction --record` reliably produces multi-line text). Fixing at the call site has the smallest blast radius and keeps console UX intact; adding the general guard protects every evidence caller. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | in-memory reproduction + code read | Root cause: cmd_direction passes multi-line format_direction() output verbatim into generate_evidence_entry(), which interpolates it into one table row with no newline escaping. Only line 1 stays in the table; Protect, Change, Avoid lines leak out and ws validate flags them (SC030 reported lines 6-8). |
| [decision] | director | Director accepted the evidence-writer fix as prevention and authorized this bounded Change Work Object linked responds_to Incident WO 2026-08-23-005 (do both, 2026-08-23). Decision 1 records the fix approach: H1 call-site single-line serialization first, H2 general guard in generate_evidence_entry as defense-in-depth. |
| [system] | ws relation add + frontmatter | Relationship recorded: REL-2026_08_23_006-001 responds_to wo:2026-08-23-005 written via ws relation add; frontmatter responds_to: 2026-08-23-005 added (runtime envelope reads frontmatter.responds_to; no CLI sets that field, so it mirrors corpus precedent). |
| [decision] | director | Director routed the Change WO to implementation (2026-08-23): apply Decision 1 and verify with ws validate on a recorded Direction. |
| [system] | implement-bounded-change | Implementation (Decision 1, surgical): direction.py adds format_direction_single_line() (reuses format_direction, joins lines with br); cmd_direction uses it for the evidence row while console output stays multi-line; sections.py generate_evidence_entry() normalizes newlines in any evidence text. Other threads' uncommitted work (including the dirty cmd_direction itself) preserved; only the evidence-writing line touched in __main__.py. |
| [system] | verification | Verified: end-to-end in an isolated temp workspace, ws direction --record wrote ONE valid 3-cell Evidence ledger row (newlines joined with br; no leaked Protect/Change/Avoid lines) and ws validate passed all checks; console output remained multi-line. H2 guard confirmed: multi-line append-evidence text normalizes to a single cell. Unit suite: 253 tests, no new failures (2 pre-existing failures from other threads' work; 1 pre-existing clock-flaky parity test). |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

Route to implement-bounded-change: apply Decision 1 (single-line evidence
serialization in `cmd_direction`, plus the `generate_evidence_entry` guard),
then verify with `ws validate` on a freshly recorded Direction.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-23T23:49:27Z — Create bounded Change WO responding to Incident 2026-08-23-005; Decision 1 records the fix approach

- **State:** notice
- **Status:** active
- **Actor:** conductor
- **Rationale:** Director authorized (do both). Root cause confirmed by reproduction; fix scoped to single-line evidence serialization (H1 call-site first, H2 general guard). Code implementation is NOT performed in this Work Object; it routes to implement-bounded-change under its own acceptance and authority.
### 2026-08-24T03:19:16Z — Implement Decision 1 and verify evidence-writer fix end-to-end

- **State:** verify
- **Status:** active
- **Actor:** conductor
- **Rationale:** Director routed to implement. Applied single-line evidence serialization (direction.py format_direction_single_line + cmd_direction call-site; sections.py newline guard). Verified end-to-end in an isolated temp workspace: ws direction --record writes one valid 3-cell Evidence ledger row and ws validate passes all checks; console output stays multi-line; append-evidence multi-line text normalized. No new unit-test failures (2 pre-existing, 1 pre-existing clock-flaky).
## Relationships

  REL-2026_08_23_006-001:
    type: responds_to
    from: wo:2026-08-23-006
    to: wo:2026-08-23-005
    basis: "Director authorized (do both, 2026-08-23)"
    created_at: 2026-08-23T23:48:37Z
