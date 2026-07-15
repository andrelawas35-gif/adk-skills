---
schema_version: 1
id: "2026-07-15-003"
title: "Qualify PKM Memory Candidate gate"
type: "change"
status: "active"
state: "verify"
consequence: "meaningful"
sensitivity: "ordinary"
created_at: "2026-07-15T14:20:20Z"
updated_at: "2026-07-15T14:26:30Z"
next_action: "Review the verified qualification evidence before deciding whether a future live-PKM runtime exercise is warranted; no deployment or export is authorized."
---

# Qualify PKM Memory Candidate gate

## Intent

Correct and qualify the Memory Candidate admission gate so a PKM-derived
candidate enters a Work Object only through an approved, redacted Evidence
Bridge, without copying protected personal-memory content.

## Success evidence

- [decision] The gate is explicit in the signal-capture skill and applies even
  after explicit activation.
- [system] A focused contract test proves the canonical skill, cross-package
  fixture, and every generated adapter contain the gate.
- [system] The qualification record identifies the executed user path, the
  missing-bridge recovery path, deviations, and remaining assumptions.

## Constraints and non-goals

- [decision] This pilot is limited to a documentation-and-contract correction
  in `turn-signal-into-work` and generated adapters.
- [decision] Do not read, copy, export, or alter Personal Institution records.
- [decision] Do not deploy, release, or export this change.
- [decision] Do not change the existing Work Object schema or add a Personal
  Institution integration.

## Evidence ledger

- 2026-07-15T14:20:20Z — [system] Issue #17 identifies the Slice 2
  qualification pilot and requires a real Change Work Object without protected
  personal-memory content.
- 2026-07-15T14:20:20Z — [system] `skills/core/turn-signal-into-work/SKILL.md`
  previously prohibited scanning and copying but did not name the Memory
  Candidate admission check or say that explicit activation cannot bypass it.
- 2026-07-15T14:20:20Z — [decision] The user confirmed the public test seam:
  test `turn-signal-into-work` so a candidate may enter a Work Object only as a
  user-approved, redacted Evidence Bridge and direct personal-memory content
  is blocked.
- 2026-07-15T14:20:20Z — [system] `python3 -m unittest
  tests/test_memory_candidate_gate.py -v` first failed because the named gate
  and its required conditions were absent from the core and adapters.
- 2026-07-15T14:20:20Z — [system] After the bounded correction and adapter
  generation, the same focused command passed: 4 tests, 0 failures.

## Decisions and revisit triggers

### 2026-07-15T14:20:20Z — Accepted tracer bullet: enforce the admission boundary at signal capture

- **Branch chosen**: Add an explicit Memory Candidate gate to
  `turn-signal-into-work`, require an approved, redacted Evidence Bridge before
  personal context can enter Work Studio, and cover it with a contract test
  propagated through all generated adapters.
- **Authorization**: The user explicitly confirmed this test seam and bounded
  gate behavior.
- **Riskiest assumption**: The existing generic prohibition was sufficiently
  precise to prevent an activated Memory Candidate from being copied into a
  Work Object.
- **Failure behavior**: When no approved bridge exists, retain no personal
  content, report the evidence gap, and request only a minimum necessary
  approved summary or stable reference.
- **Observability**: The focused contract verifies the core wording, the
  cross-package fixture, and all three generated adapters.
- **Rollback**: Revert the one canonical-skill change, its fixture scenario,
  test, and generated artifacts together; no external or personal data state
  exists to reverse.
- **Non-goals**: Automated Personal Institution retrieval, migration of
  personal records, deployment, export, or a broader PKM integration.
- **Exit criteria**: The focused gate test and full repository suite pass; the
  evidence record plainly names any untested live-PKM assumption.
- **Revisit trigger**: Reopen if a Personal Institution integration introduces
  a different bridge format or an activation path that can bypass the gate.

## Tracer bullet

- **Entry and resulting state**: A user explicitly activates a PKM-derived
  Memory Candidate; the signal skill either receives an approved redacted
  bridge and routes it to the conductor, or stops with a minimum-summary
  request without storing personal content.
- **Authorization boundary**: User approval for the bridge is required;
  explicit work activation alone is insufficient.
- **Verification seam**: `tests/test_memory_candidate_gate.py` exercises the
  public skill contract and generated-adapter propagation.

## Implementation evidence

- [system] Added `tests/test_memory_candidate_gate.py` before the correction;
  its initial execution failed as expected.
- [system] Added the named gate and missing-bridge recovery behavior to
  `skills/core/turn-signal-into-work/SKILL.md` and Scenario 7 to the shared
  cross-package contract fixture.
- [system] Ran `python3 tools/generate-adapters.py`; the canonical core change
  propagated to Codex, Claude Code, and GitHub Copilot artifacts and their
  checksums/manifests.

## Verification and release evidence

- **Routes exercised**: [system] The live signal was classified by
  `turn-signal-into-work`; `conduct-work-object` created and updated this
  Change Work Object; `design-tracer-bullet` supplied the accepted bounded
  design; `implement-bounded-change` supplied the red-green bounded change;
  and `verify-release-evidence` supplied this proportionate evidence record.
- [system] Focused gate contract: `python3 -m unittest
  tests/test_memory_candidate_gate.py -v` — verified, 4 tests passed.
- [system] Verified user path: an approved, redacted bridge is the only
  admissible representation for a Memory Candidate in a Work Object.
- [system] Verified recovery path: with no approved bridge, the skill directs
  a minimum necessary approved summary or stable reference and does not copy
  personal-memory content; after that approved bridge is supplied, the signal
  may route through the conductor without copying the source record.
- [system] Deviation status: none observed. The implementation matched the
  accepted tracer bullet; the two fixture trailing spaces caught by diff
  hygiene were formatting corrections, not a changed path, authority, or
  boundary.
- [system] Privacy boundary: the test uses only policy text and fixture text;
  no Personal Institution archive, private record, secret, or external system
  was accessed.
- [system] Security boundary: no credentials, network calls, deployment, or
  external writes were used.
- [system] Full suite: `sh tests/run.sh` — verified; 33 Python contract tests,
  10 installer tests, Codex installation/reproducibility checks, and the
  generator drift gate all passed.
- [system] Conformance: `python3 tools/verify-conformance.py --all` —
  verified; behavioral-matrix and structural-adapter checks passed.
- [system] Diff hygiene: `git diff --check` — verified after removal of two
  fixture trailing spaces.
- [inference] Live runtime enforcement depends on each platform loading its
  generated adapter and following the documented instructions; this repository
  qualification does not exercise a real Personal Institution archive.

## Open questions

- Unresolved: whether a future Personal Institution implementation will expose
  an Evidence Bridge format that needs machine-enforced schema validation.
- Unresolved: whether each installed platform follows the gate under a fresh,
  live PKM task rather than only through the contract artifacts.

## Next move

Review the verified qualification evidence before deciding whether a future
live-PKM runtime exercise is warranted; no deployment or export is authorized.

## History

- 2026-07-15T14:20:20Z — Captured and activated the PKM Memory Candidate gate
  change; state `notice`; status `active`; actor `agent`; platform `codex`;
  rationale: issue #17 and the user request provide a bounded, meaningful
  qualification signal without authorizing access to personal-memory content.
- 2026-07-15T14:20:20Z — Accepted tracer bullet recorded; state `design`;
  status `active`; actor `agent`; platform `codex`; rationale: the user
  confirmed the public signal-capture contract seam and the gate’s exact
  approved-bridge boundary.
- 2026-07-15T14:20:20Z — Implemented bounded gate correction; state `build`;
  status `active`; actor `agent`; platform `codex`; rationale: the red test
  showed the explicit activation-bypass protection was missing.
- 2026-07-15T14:20:20Z — Recorded focused verification evidence; state
  `verify`; status `active`; actor `agent`; platform `codex`; rationale: the
  focused contract passed after adapter generation; the complete suite remains
  the next qualification check.
- 2026-07-15T14:22:05Z — Recorded qualification verification evidence; state
  `verify`; status `active`; actor `agent`; platform `codex`; rationale: the
  complete test, installer, reproducibility, conformance, and diff-hygiene
  checks passed; live-PKM runtime behavior remains explicitly unverified.
- 2026-07-15T14:24:30Z — Strengthened qualification evidence after review;
  state `verify`; status `active`; actor `agent`; platform `codex`; rationale:
  make each Slice 2 handoff, both bridge paths, and the absence of material
  deviations explicit and regression-tested.
- 2026-07-15T14:26:30Z — Corrected qualification evidence after review; state
  `verify`; status `active`; actor `agent`; platform `codex`; rationale:
  assert the documented approved-bridge recovery route and align the focused
  test count with the committed four-test contract suite.
