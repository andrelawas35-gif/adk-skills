---
schema_version: 1
id: 2026-08-25-018
title: Wire pipeline gate approvals through Director Console desktop surface (successor to 2026-08-25-011)
type: change
status: closed
state: close
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-26T04:05:09Z
updated_at: 2026-08-26T05:31:06Z
next_action: Awaiting director direction: outcome review (recommended) or further slices














---
## Intent

Wire pipeline gate approvals through the Director Console desktop surface so a
human can grant or deny tier gates without touching the CLI. Compose over the
proven `approvals.py` CLI seam (WO `2026-08-25-011` slice 3) — the durable
approval-record contract (`{tier, approved_by, at}`, identical to what
`pipeline.record_approval` writes) is the stable seam; this object changes only
the surface that produces those records.

Predecessor: WO `2026-08-25-011` (closed; outcome review confirmed delivery).
Dependency: desktop packaging lands in WO `2026-08-24-004`; sequence against
it explicitly rather than blocking.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [ ] An approval issued through the console/desktop surface resumes a live pipeline halted at its gate, observed across a process boundary
- [ ] A denial issued through the surface leaves the shot waiting with an audit record, no state mutation
- [ ] Approval records written by the surface are byte-compatible with the `record_approval` contract; pipeline consumes them unchanged
- [ ] Unknown gate / wrong-tier approvals rejected before any filesystem write
- [ ] `ws validate` shows no regression


## Constraints and non-goals

**Constraints:**
<!-- Boundaries the implementation must respect. -->
- Approval-record contract unchanged — surface composes over `approvals.py` semantics, never forks the format
- Gate enforcement semantics unchanged (waiting state, external approval records)
- COMP-041 GPU claim discipline preserved through any live-pipeline verification

**Non-goals:**
<!-- Explicitly excluded work. -->
- No changes to `run_pipeline` tier/retry/critic mechanics
- No authentication or multi-user support
- No new pipeline capabilities beyond the approval surface

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Slice 1: console bridge methods over imported approvals logic, single work_dir, one gate end-to-end

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Add three narrow methods to DirectorConsoleBridge — gate_status(work_dir), approve_gate(work_dir, tier), deny_gate(work_dir, tier, reason) — each delegating to the same logic approvals.py uses (imported, not copied, so record_approval byte-compatibility is structural). Add a minimal Gates panel to director_console/static (index.html + app.js) following the existing callBridge pattern. Tracer: run_pipeline in one OS process with scripted tiers (no GPU claim — the risk under test is the seam, not rendering), halted at the breakdown gate; Approve issued through the bridge resumes the external process into tier_a's own legitimate gate; negatives: deny leaves shot waiting with audit record and no state mutation, wrong-tier approve rejected pre-write with zero filesystem change. |
| **Authorization** | Director accepted the slice design ('accept this slice'). Local test authority only: temp dirs, subprocess pipeline, programmatic bridge invocation plus one manual panel click-through for the UI claim. |
| **Confidence** | high on record byte-compatibility (imported shared code makes divergence structurally impossible); medium on the live process-boundary observation through the new seam — exactly what the tracer tests. |
| **Actor** | director |
| **Revisit trigger** | If pywebview js_api threading interferes with file writes or subprocess observation, reopen toward a queue-file handoff between UI thread and bridge. If multi-shot discovery blocks real use, add registry scan as slice 2 rather than widening this one. |
| **Failure behavior** | If the resumed external process never observes the console-written record, or bytes differ from CLI-written records, the assumption fails: route to pressure-test-decision; claim nothing shipped. Bridge errors return structured {ok: False} diagnostics per existing _response contract; no partial writes. |
| **Observability** | Pipeline history notes naming the gate closed by a console-surface record; diff of console-written approval JSON vs record_approval output; filesystem snapshot proving wrong-tier rejection wrote nothing; tracer PASS/FAIL lines. |
| **Non-goals** | Multi-shot registry scan/queue view, authentication, installer/packaging (WO 2026-08-24-004 territory), any run_pipeline mechanics change. |
| **Rollback** | Revert bridge.py + static edits, delete tracer file; temp dirs auto-clean. No durable state outside temp dirs. |
| **Exit criteria** | Pass: console-originated approve observed resuming an external-process pipeline past the breakdown gate + deny and wrong-tier negatives clean -> verify-release-evidence. Fail -> pressure-test-decision. |

**Tracer result (2026-08-26): PASS (automated).** Implemented approvals.py helper extraction (status_payload/approve_gate/deny_gate + ApprovalError; CLI wrappers byte-identical), bridge.py gate_status/approve_gate/deny_gate delegating to the imported module, Gates panel in static/index.html + app.js, tracer_console_gate.py, and updated test_director_console_bridge surface set (+4 gate unit tests). Observed: [A] subprocess run_pipeline halted waiting@breakdown; bridge.approve_gate resumed a SECOND subprocess into tier_a's own legitimate gate; console record structurally identical to record_approval output (keys {tier, approved_by, at}, indent=2). [B] bridge deny wrote denial-breakdown.json with reason, shot_state.json byte-unchanged, shot still waiting@breakdown on next process run. [C] wrong-tier approve returned ok:false 'not waiting at' with zero filesystem change; missing-dir gate_status returned structured FileNotFoundError. Regression: tracer_gates.py PASS after refactor; focused tests 6/6. Gap: manual panel click-through not yet performed (director step).

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [gap] | ws transition audit (build) | No decision record with result: pass found at build transition. An accepted decision record is expected before entering build state. |
| [system] | implement-bounded-change slice 1 run, 2026-08-26 | Console-gate tracer PASS. approvals.py: extracted status_payload/approve_gate/deny_gate + ApprovalError (CLI wrappers byte-identical, unknown-gate/tier-mismatch/status order preserved). bridge.py: gate_status/approve_gate/deny_gate delegate to imported approvals module via path-bootstrapped lazy import; structured _response errors. static/: Gates panel with Check Gate/Approve/Deny + reason input. Tracer (tracer_console_gate.py): [A] subprocess run_pipeline halted waiting@breakdown, bridge.approve_gate resumed a SECOND subprocess into tier_a gate, record structurally identical to record_approval ({tier, approved_by, at}, indent=2); [B] deny wrote denial record, shot_state.json byte-unchanged; [C] wrong-tier ok:false pre-write zero fs change, missing-dir structured FileNotFoundError. Regression: tracer_gates PASS post-refactor; test_director_console_bridge 6/6 (surface set extended per accepted design); generate-adapters --check clean; ws validate baseline 51 unchanged. Suite note: full pytest blocked by pre-existing hang in unmodified test_engineering_handoff_cli.py + hardware-bound operator tests excluded; all other runnable files executed - failures confined to files with zero import overlap with this change. |
| [gap] | ws transition audit (verify) | Unresolved [gap] entries exist in the Evidence ledger. Residual uncertainty should be reviewed before proceeding. |
| [system] | verify-release-evidence slice 1, 2026-08-26 | Independent verification, all second-run executed: (1) SUCCESS PATH - tracer_console_gate.py PASS again: subprocess run_pipeline halted waiting@breakdown; bridge.approve_gate resumed a SECOND external process into tier_a gate; record structurally identical to record_approval ({tier, approved_by, at}, indent=2). (2) REGRESSION - tracer_gates.py PASS post-refactor (CLI loop intact); test_director_console_bridge + workspace 11/11. (3) EXTRA NEGATIVES beyond implementation run: approve on status=failed shot rejected pre-write with structured ApprovalError and zero filesystem change; unknown-gate via bridge structured error; deny-on-failed-shot writes audit record only (by-design CLI parity, no state mutation); missing-dir gate_status FileNotFoundError. (4) BASELINE - ws validate 51 unchanged. GAPS: manual Gates-panel click-through through the real pywebview window NOT performed (artifact_rendering is manual-fallback here) - UI claim remains unverified; python -m director_console.app returned rc=0 inconclusively without observable window in this session. |
| [system] | manual click-through, 2026-08-26 | Director executed the Gates-panel flow in the real pywebview window (.venv python -m director_console): [1] Approve on ws-gate-demo wrote approval-breakdown.json ({approved_by: director, at, tier}) through bridge -> approvals helper -> record_approval contract - backend effect verified on disk even though panel feedback initially looked unchanged. [2] Feedback gap surfaced and fixed within scope: decideGate confirmation was instantly overwritten by stale gate reload; fix adds persistent prefix confirmation plus a records-on-disk listing (additive status_payload records field; app.js renderGate/loadGateStatus/decideGate updates). Post-fix unit checks 11/11, tracer PASS, records listing observed empty->approval-breakdown.json after approve. [3] Director re-click-through on fresh SH-DEMO2: Deny produced exactly the expected persistent line (Denial recorded (denial-breakdown.json); a running pipeline consumes it ... records on disk). UI claim VERIFIED by the human operator. |
| [decision] | Outcome review, 2026-08-26 | Director outcome review: hypothesis CONFIRMED - console-originated gate decisions produce records a separately-running pipeline observes and acts on, byte-compatible with the record_approval contract, with pre-write rejection of invalid approvals (tracer PASS twice independently + director-executed real-window click-through). Direction selected: stop (close). Residuals dispositioned as named follow-ups rather than defects: multi-shot registry scan out of scope; desktop packaging/installer remains WO 2026-08-24-004; Decision 1 revisit triggers never fired. Post-closure: bridge gate methods + approvals helpers are track-components candidates. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

- Does this build on WO `2026-08-24-004` desktop packaging directly, or can the existing `director_console` web app serve as the first surface before native packaging lands?

## Next move

<!-- The single next action this Work Object routes to. -->

Route to `alawas-design-design-tracer-bullet`: design the smallest slice — one gate closed end-to-end through the chosen console surface, records byte-compatible with the `record_approval` contract.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-26T04:05:16Z — Created as successor to closed 2026-08-25-011

- **State:** notice
- **Status:** active
- **Actor:** director
- **Rationale:** Outcome review of 2026-08-25-011 confirmed delivery (6/6 success evidence, each slice verified twice) and selected create-successor: wire pipeline gate approvals through the Director Console desktop surface, composing over the proven approvals.py CLI seam so the durable approval-record contract stays unchanged. Desktop dependency: WO 2026-08-24-004.
### 2026-08-26T04:06:05Z — Routed to design-tracer-bullet

- **State:** notice
- **Status:** active
- **Actor:** system
- **Rationale:** Concrete scope inherited from outcome review direction. Smallest slice: one gate closed end-to-end through the console surface with contract-compatible records.
### 2026-08-26T04:07:03Z — Design state: smallest console-gate slice

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** Concrete scope inherited from outcome review direction; no divergent exploration needed (skip-explore precedent of parent 2026-08-25-011).
### 2026-08-26T04:22:27Z — Slice 1 accepted: console bridge over approvals logic

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director accepted the tracer design: gate_status/approve_gate/deny_gate bridge methods delegating to imported approvals.py logic, minimal Gates panel, scripted-tier external-process pipeline, one gate end-to-end plus deny and wrong-tier negatives.
### 2026-08-26T05:11:10Z — Slice 1 implemented; route to verify-release-evidence

- **State:** verify
- **Status:** active
- **Actor:** system
- **Rationale:** Console-gate tracer PASS all three scenarios (external-process resume, deny audit semantics, pre-write rejection) with contract-compatible records; CLI regression clean. Open gap: manual Gates-panel click-through pending director execution.
### 2026-08-26T05:13:40Z — Verify-release-evidence complete: slice 1 verified (automated); UI click-through manual-fallback

- **State:** verify
- **Status:** active
- **Actor:** system
- **Rationale:** Second independent tracer run PASS all scenarios; extra negatives clean (failed-status approve pre-write rejection, unknown gate, missing dir); CLI regression and validate baseline intact. Remaining gap: human click-through of the Gates panel in the real pywebview window.
### 2026-08-26T05:26:59Z — Manual click-through verified; slice 1 evidence complete

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Director executed Approve and Deny in the real pywebview window: records written contract-correctly, persistent feedback confirmed exactly as specified after the accepted UX fix. All Decision 1 exit criteria now met including the UI claim.
### 2026-08-26T05:30:05Z — Outcome review: evidence complete

- **State:** observe
- **Status:** active
- **Actor:** system
- **Rationale:** All Decision 1 exit criteria verified including director-executed UI click-through. Entering observe for formal outcome review.
### 2026-08-26T05:31:00Z — Outcome review: confirmed; stop

- **State:** observe
- **Status:** active
- **Actor:** director
- **Rationale:** Director accepted stop: slice delivered and doubly evidenced (automated tracer x2 + human UI verification); residuals routed as follow-ups.
### 2026-08-26T05:31:06Z — Closed: Outcome review confirmed: Director Console bridge closes pipeline gates across a process boundary with record_approval-compatible records; verified twice by automated tracer and once by director-executed UI click-through. Successor candidates (multi-shot queue view) are new scope.

- **State:** close
- **Status:** closed
- **Actor:** system
- **Rationale:** Outcome review confirmed: Director Console bridge closes pipeline gates across a process boundary with record_approval-compatible records; verified twice by automated tracer and once by director-executed UI click-through. Successor candidates (multi-shot queue view) are new scope.
