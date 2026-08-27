---
schema_version: 1
id: 2026-08-22-021
title: Integrate business router into Phase 6 dispatch
type: change
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
domain: [business, engineering]
created_at: 2026-08-22T13:23:21Z
updated_at: 2026-08-22T13:28:33Z
next_action: Recommended next slice: decide whether to add explicit business_scope metadata to Work Objects.











---
## Intent

Integrate the deterministic business operating router into Phase 6 dispatch so
business-scoped Work Objects can produce business-aware dispatch envelopes,
branch proposals, join proposals, and checkpoint inspection state without
canonical writes or live business-system mutations.

## Success evidence

- [x] Phase 6 dispatch detects explicitly business-scoped Work Objects from title, `next_action`, or open questions.
- [x] Phase 6 dispatch stores `business_route_result` and `business_handoff_envelope` in checkpoint state.
- [x] Phase 6 `handoff_envelope` routes to the business-router target skill when business routing applies.
- [x] Phase 6 branch receipts honor the dispatch business route, including governance targets such as scorecards.
- [x] `inspect_phase6` exposes whether a checkpoint contains a business handoff.
- [x] Existing non-business Phase 6 state routing remains regression-tested.
- [x] Business, governance, projection, and Phase 6 concurrent checks pass.


## Constraints and non-goals

**Constraints:**
- Preserve Phase 6 as a runtime-plane graph: no canonical Work Object writes
  during dispatch, branch, join, inspect, or approval.
- Use the deterministic business router functions inside Phase 6 rather than
  nesting a second checkpointed LangGraph.
- Trigger business routing only from explicit business-scoped dispatch signals,
  not incidental mentions in non-goals or evidence body text.
- Preserve existing state-based routing for non-business Work Objects.
- Preserve unrelated dirty work in the repository.

**Non-goals:**
- No deployment or release.
- No adapter regeneration or global skill installation.
- No live CRM, inventory, finance, supplier, customer, or operational mutation.
- No replacement of the standalone `runtime.business` router CLI.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Use deterministic business routing inside Phase 6 dispatch

| Field | Value |
|-------|-------|
| **Decision type** | decision / authority |
| **Result** | pass |
| **Scope** | Phase 6 dispatch and branch proposal behavior for business-scoped Work Objects. |
| **Authorization** | User explicitly instructed: "integrate the router into phase 6 dispatch". |
| **Confidence** | high for runtime behavior; medium for business-scope detection heuristic — basis: focused business tests, Phase 6 lifecycle regression tests, and concurrent Phase 6 checks pass. |
| **Actor** | Codex |
| **Revisit trigger** | Revisit when business scope must be declared via frontmatter/schema instead of inferred from title, next_action, or open questions. |
| **Rationale** | Calling deterministic business routing during Phase 6 dispatch makes business Work Objects route through the business operating pipeline while preserving Phase 6 checkpointing and non-writer guarantees. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | runtime/graph.py | Phase6State now carries business_route_result and business_handoff_envelope checkpoint fields. |
| [system] | runtime/graph.py | phase6_dispatch calls deterministic business routing for explicitly business-scoped Work Objects and emits a governed dispatch HandoffEnvelope to the routed target skill. |
| [system] | runtime/graph.py | Phase 6 branch proposal derivation honors business_handoff_envelope.to_skill, including governance-domain business pipeline targets. |
| [system] | runtime/graph.py | inspect_phase6 now reports has_business_handoff_envelope and business_route_result from runtime checkpoint state. |
| [system] | runtime/tests/test_business_graph.py | Added Phase6BusinessDispatchIntegrationTests covering dispatch routing, branch route honoring, and checkpoint inspection for business handoffs. |
| [system] | runtime/tests/test_handoff_graph.py | Adjusted lifecycle determinism expectation so business-routed Work Objects are evaluated against their business_handoff_envelope target instead of the generic state router. |
| [system] | command | uv run --python 3.11 python -m unittest runtime.tests.test_business_graph -v completed successfully: 17 tests passed. |
| [system] | command | uv run --python 3.11 python -m unittest runtime.tests.test_business_graph tests.test_component_governance runtime.tests.test_projection runtime.tests.test_handoff_graph.Phase6HandoffTests.test_fanout_join_runs_both_branches_and_join_once runtime.tests.test_handoff_graph.Phase6HandoffTests.test_crash_before_join_resumes_without_duplicated_join runtime.tests.test_handoff_graph.Phase6HandoffTests.test_multi_state_determinism_across_lifecycle -v completed successfully: 51 tests passed. |
| [system] | command | uv run --python 3.11 python -m unittest runtime.tests.test_phase6_concurrent -v completed successfully: 2 tests passed. |
## Open questions

- Should business scope become an explicit Work Object frontmatter field rather
  than a runtime detection heuristic?

## Next move

Route to verification/release evidence review; recommended next slice is an
explicit business-scope declaration if the heuristic proves too broad or too
narrow.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T13:28:06Z — Entered verification after Phase 6 business dispatch integration

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** Phase 6 dispatch now stores business route and handoff checkpoint payloads for business-scoped Work Objects while preserving non-business routing.
### 2026-08-22T13:28:33Z — Completed Phase 6 business dispatch integration

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** Business-scoped Phase 6 runs now route dispatch, branches, join proposal, and inspection through deterministic business operating-pipeline payloads while non-business regression checks remain green.
