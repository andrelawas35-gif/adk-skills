---
schema_version: 1
id: 2026-08-21-007
title: Expose --approve-direction on the run-phase6 CLI subcommand
type: change
status: closed
state: close
consequence: low
sensitivity: ordinary
domain: [engineering]
created_at: 2026-08-21T14:42:11Z
updated_at: 2026-08-21T14:45:58Z
next_action: Add --approve-direction to the run-phase6 argparse subcommand in runtime/graph.py, wire it into the existing run_phase6 call in main(), verify end-to-end via CLI only



---
## Intent

Found during `2026-08-21-006`'s demonstration run: `run_phase6(..., approve_direction=...)` is already implemented and tested (used by `runtime/tests/*` and this session's own demo), but `main()`'s `run-phase6` CLI subcommand (`runtime/graph.py:1288-1299`) never wires an `--approve-direction` flag to it -- the CLI can start a run and reach the `direction_gate` interrupt, but answering that interrupt currently requires a direct Python call, not a CLI-only workflow. Add the missing flag. No design decision here: the underlying behavior already exists, is already tested, and this only exposes it -- purely mechanical, unlike the earlier three-gate-types item (`2026-08-21-004`) which was blocked because no real call site existed at all. Skipping a separate tracer-bullet cycle for that reason; consequence is `low`.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] `run-phase6` CLI subcommand accepts `--approve-direction`/`--reject-direction` (store_true flags, not a single `{true,false}` value -- simpler with argparse's mutually-exclusive-group mechanism), passed through to `run_phase6`'s existing `approve_direction` parameter
- [x] `--resume`, `--approve-direction`, `--reject-direction` are mutually exclusive at the CLI via one `add_mutually_exclusive_group()` -- verified: passing two together errors before any graph code runs
- [x] Manually verified end-to-end via CLI only: start a run, reach the interrupt, approve via `--approve-direction`, confirmed `direction_approved: true` in the output -- no direct Python call needed. Regression check: `test_phase7_hypothesis` + `test_phase7_error_classes`, 6 tests, OK


## Constraints and non-goals

**Constraints:**
<!-- Boundaries the implementation must respect. -->

**Non-goals:**
<!-- Explicitly excluded work. -->

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Implement --approve-direction/--reject-direction as a mutually exclusive group alongside --resume

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | `run_phase6_parser` gains `--approve-direction`/`--reject-direction` (store_true) in the same `add_mutually_exclusive_group()` as `--resume`; `main()`'s handler computes `approve_direction` (True/False/None) and passes it through to the existing, unmodified `run_phase6(approve_direction=...)` parameter. No changes to `run_phase6` itself or to any graph node. |
| **Authorization** | Director: "Fix the missing --approve-direction CLI flag" |
| **Confidence** | high -- the underlying `approve_direction` parameter was already implemented, tested, and demonstrated working (WO `2026-08-21-006`'s run); this only exposes it via argparse, verified end-to-end via CLI with no regressions |
| **Actor** | director |
| **Revisit trigger** | None expected -- purely additive CLI surface over already-proven behavior |
| **Rationale** | Two boolean flags in a mutually-exclusive group is simpler than a single `--approve-direction {true,false}` value argument, and matches the existing `--resume` flag's style in the same parser exactly. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | this session: uv run python -m runtime.graph run-phase6 ... --approve-direction; uv run python -m runtime.graph run-phase6 ... --resume --approve-direction (mutual exclusion check); uv run --group test python -m unittest runtime.tests.test_phase7_hypothesis runtime.tests.test_phase7_error_classes; git diff runtime/graph.py | Implemented: run_phase6_parser gained a mutually exclusive group (--resume | --approve-direction | --reject-direction), runtime/graph.py main()'s run-phase6 handler now computes approve_direction from the two new store_true flags and passes it through to the existing, unmodified run_phase6(approve_direction=...) parameter. Verified end-to-end via CLI only (no direct Python call): run-phase6 to start + reach the direction_gate interrupt, then run-phase6 --approve-direction on the same thread/checkpoint-db produced direction_approved: true in the JSON output. Mutual exclusion verified: --resume --approve-direction together errors via argparse before any graph code runs. Regression check: uv run --group test python -m unittest runtime.tests.test_phase7_hypothesis runtime.tests.test_phase7_error_classes -- 6 tests, 91.7s, OK, no failures. git status confirms only runtime/graph.py's diff grew by this change; the pre-existing unrelated multi-repo-registry diff already in that file (WO 2026-08-21-005) was left untouched. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

<!-- The single next action this Work Object routes to. -->

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-21T14:42:33Z — create-and-skip-to-build-mechanical-fix

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director: fix the missing --approve-direction CLI flag. Purely mechanical -- run_phase6's approve_direction parameter is already implemented and tested; this only exposes it via argparse. No design decision or invented call site involved (unlike 2026-08-21-004's blocked gate-types item), so skipping design-tracer-bullet and going straight to build for this low-consequence, low-risk change.
### 2026-08-21T14:45:58Z — Closed: All three Success evidence items met and verified: --approve-direction/--reject-direction added to run-phase6's argparse group alongside --resume (mutually exclusive), wired through to the existing run_phase6(approve_direction=...) parameter, verified end-to-end via CLI only with no direct Python call, and confirmed no regressions via the two existing Phase 7 test suites.

- **State:** close
- **Status:** closed
- **Actor:** director
- **Rationale:** All three Success evidence items met and verified: --approve-direction/--reject-direction added to run-phase6's argparse group alongside --resume (mutually exclusive), wired through to the existing run_phase6(approve_direction=...) parameter, verified end-to-end via CLI only with no direct Python call, and confirmed no regressions via the two existing Phase 7 test suites.
