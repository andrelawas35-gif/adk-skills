---
schema_version: 1
id: 2026-08-22-018
title: Add checkpointed LangGraph business operating router
type: change
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-22T13:10:40Z
updated_at: 2026-08-22T13:13:42Z
next_action: Route to alawas-engineering-verify-release-evidence for release-evidence review of the checkpointed business router; CLI command-surface wiring and Phase 6 integration remain separate future slices.








---
## Intent

Add a checkpointed LangGraph business operating router on top of the read-only
business graph tracer from Work Object `2026-08-22-016`. The router should
classify a business frontier, validate that the move stays inside a non-mutating
authority boundary, resolve the next business skill through the canonical
business route, emit a Pydantic handoff proposal, and pause for director
approval before completion.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] A LangGraph `StateGraph` exists for the business operating router.
- [x] The graph checkpoints router state using SQLite.
- [x] The graph pauses at a director gate with the proposed business handoff.
- [x] The graph resumes with approval or rejection and records the result in
      runtime state.
- [x] The router rejects live-mutation authority boundaries.
- [x] Focused tests pass for business graph/router, component governance, and
      existing NetworkX Work Object projection behavior.


## Constraints and non-goals

**Constraints:**
<!-- Boundaries the implementation must respect. -->
- Build on `runtime/business.py` and the canonical
  `references/BUSINESS-OPERATING-PIPELINE.md` parser.
- Keep the router runtime-plane only; it may checkpoint, inspect, and propose,
  but must not write canonical Work Objects or mutate business systems.
- Use the existing LangGraph checkpoint/interrupt pattern already present in
  `runtime/graph.py`.
- Preserve the prior NetworkX projection and Pydantic business handoff behavior.

**Non-goals:**
<!-- Explicitly excluded work. -->
- No CLI command-surface wiring.
- No integration into the Phase 6 generic handoff graph.
- No live CRM, customer, supplier, pricing, money, personnel, or external-system
  action.
- No generated adapter regeneration or global install.
- No cleanup of unrelated dirty worktree changes.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Implement checkpointed business router slice

| Field | Value |
|-------|-------|
| **Decision type** | bounded-change |
| **Result** | pass |
| **Scope** | Add a checkpointed LangGraph business router with classify, authority-validation, route, proposal, and director-gate nodes. Excludes CLI wiring, canonical writes, live business effects, and adapter/global-install changes. |
| **Authorization** | Director said "do next slice" immediately after Work Object `2026-08-22-016` completed with the next route: checkpointed LangGraph business-router promotion remains a separate slice. |
| **Confidence** | medium-high — basis: the previous tracer already supplies deterministic routing and Pydantic handoff validation; existing runtime has LangGraph checkpoint and interrupt patterns to reuse. |
| **Actor** | director |
| **Revisit trigger** | Router needs command-line access, Phase 6 integration, richer frontier extraction from Work Object bodies, or real business entity graph nodes. |
| **Rationale** | This is the smallest safe runtime promotion: checkpoint, inspect, and approval-gate business handoff proposals without making runtime state canonical or touching live business operations. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | runtime/business.py | Added build_business_router_graph with LangGraph classify_frontier, validate_authority, route_skill, propose_handoff, and director_gate nodes over BusinessRouterState. |
| [system] | runtime/business.py | Added SQLite checkpoint support for the business router using SqliteSaver and a no-pickle JsonPlusSerializer; run_business_router can start a thread or resume it with Command(resume=<approval>). |
| [system] | runtime/business.py | Added inspect_business_router so the runtime can report checkpointed values, pending next nodes, awaiting_approval, and whether a handoff envelope exists for a router thread. |
| [system] | runtime/business.py | The business_router_validate_authority node rejects unsupported live-mutation boundaries and allows only read-only, read-only-propose, or governed proposal states. |
| [system] | runtime/tests/test_business_graph.py | Added BusinessRouterGraphTests covering checkpointed director-gate pause, inspectable handoff proposal state, approval resume, rejection resume, and live-mutation boundary rejection. |
| [system] | uv run --python 3.11 python -m unittest runtime.tests.test_business_graph tests.test_component_governance runtime.tests.test_projection -v | Focused verification passed: 41 tests ran successfully across the business graph/router suite, component-governance runtime enforcement, and existing NetworkX Work Object projection behavior. |
## Open questions

- Should the business router get a CLI command surface next, or should it be
  integrated into the existing Phase 6 handoff graph first?

## Next move

Route to `alawas-engineering-verify-release-evidence` for release-evidence
review of the checkpointed business router. CLI command-surface wiring and
Phase 6 integration remain separate future slices.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T13:13:38Z — Created accepted checkpointed business router slice

- **State:** notice
- **Status:** active
- **Actor:** codex
- **Rationale:** Director asked to do the next slice after the business graph tracer; this object bounds the next promotion to a read-only checkpointed LangGraph router.
### 2026-08-22T13:13:40Z — Implemented checkpointed LangGraph business router

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** Added business router StateGraph nodes and tests for checkpointed pause/resume, inspection, and authority-boundary rejection; focused verification passed.
