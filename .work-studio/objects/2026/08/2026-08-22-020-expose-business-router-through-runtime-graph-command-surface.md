---
schema_version: 1
id: 2026-08-22-020
title: Expose business router through runtime.graph command surface
type: change
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
domain: [business, engineering]
created_at: 2026-08-22T13:19:31Z
updated_at: 2026-08-22T13:22:19Z
next_action: Recommended next slice: decide whether to integrate the business router into Phase 6 dispatch.








---
## Intent

Expose the accepted checkpointed business operating router through the broader
`runtime.graph` command surface so operators can run, inspect, and approve
business handoff routing from the same runtime CLI used for other graph paths.

## Success evidence

- [x] `runtime.graph` recognizes `run-business-router` as a first-class command.
- [x] `runtime.graph` recognizes `inspect-business-router` as a first-class command.
- [x] Fresh business-router runs require an explicit `--next-gap` before routing.
- [x] A paused router thread can be inspected from the broader runtime CLI.
- [x] Director approval can resume the checkpointed router from the broader runtime CLI.
- [x] Focused business graph tests and governance/projection seam checks pass.


## Constraints and non-goals

**Constraints:**
- Keep this slice to runtime command exposure; do not wire the business router
  into Phase 6 canonical execution yet.
- Preserve the existing business router's authority boundary:
  `read-only`, `read-only-propose`, or `governed` only.
- Keep checkpoint state runtime-only and outside canonical `.work-studio/`
  writes.
- Preserve unrelated dirty work in the repository.

**Non-goals:**
- No deployment, release, adapter regeneration, or global skill installation.
- No new business skills.
- No Phase 6 business auto-routing.
- No canonical Work Object mutation from the graph runtime.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Expose the business router as sibling runtime.graph commands

| Field | Value |
|-------|-------|
| **Decision type** | decision / authority |
| **Result** | pass |
| **Scope** | Add `run-business-router` and `inspect-business-router` to `runtime.graph`; keep Phase 6 integration out of scope. |
| **Authorization** | User requested "do next slice" after accepting the prior business graph/runtime recommendation path. |
| **Confidence** | high for CLI exposure; medium for operator UX — basis: subprocess tests exercise run, inspect, approval, and missing-gap failure paths. |
| **Actor** | Codex |
| **Revisit trigger** | Revisit when Phase 6 should route business handoffs automatically or when the business router needs canonical writes. |
| **Rationale** | Sibling commands provide a low-risk operational bridge: the business router becomes visible in the main runtime CLI without expanding side effects or Phase 6 behavior. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | runtime/graph.py | Added runtime.graph commands set entries and argparse subcommands for run-business-router and inspect-business-router. |
| [system] | runtime/graph.py | run-business-router invokes runtime.business.run_business_router with checkpoint DB, frontier inputs, evidence list, authority boundary, and approve/reject resume handling. |
| [system] | runtime/graph.py | Fresh runtime.graph business-router runs return exit code 2 when --next-gap is missing, preserving an explicit routing frontier requirement. |
| [system] | runtime/tests/test_business_graph.py | Added RuntimeGraphBusinessRouterCliTests covering run, inspect, approve resume, and missing-next-gap behavior through python -m runtime.graph. |
| [system] | command | uv run --python 3.11 python -m unittest runtime.tests.test_business_graph -v completed successfully: 14 tests passed. |
| [system] | command | uv run --python 3.11 python -m unittest runtime.tests.test_business_graph tests.test_component_governance runtime.tests.test_projection -v completed successfully: 45 tests passed. |
## Open questions

- Should the next slice integrate the business router into Phase 6 dispatch, or
  keep adding operator-facing graph utilities first?

## Next move

Route to conductor for evidence recording, validation, and next-slice decision.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T13:21:57Z — Entered verification after bounded CLI implementation

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** runtime.graph command exposure and subprocess tests were implemented; verification evidence will be appended through the ledger.
### 2026-08-22T13:22:19Z — Completed bounded runtime.graph business-router CLI exposure

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** The broader runtime CLI now exposes business router run, inspect, and approval resume paths; focused and seam verification passed.
