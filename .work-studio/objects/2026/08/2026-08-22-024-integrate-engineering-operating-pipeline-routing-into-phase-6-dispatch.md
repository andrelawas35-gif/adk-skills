---
schema_version: 1
id: 2026-08-22-024
title: Integrate engineering operating-pipeline routing into Phase 6 dispatch
type: change
status: active
state: observe
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-22T13:51:11Z
updated_at: 2026-08-22T14:00:50Z
next_action: alawas-governance-review-outcome-and-adapt: review the verified local Phase 6 engineering dispatch tracer outcome and decide close versus next slice; do not deploy.
















---
## Intent

Integrate the verified engineering operating-pipeline tracer into Phase 6
dispatch as a bounded successor to Work Object `2026-08-22-023`. The target is
for runtime dispatch to recognize engineering-scoped Work Objects and propose
the correct engineering operating-pipeline handoff without disturbing existing
business dispatch or generic lifecycle routing.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] A design tracer defines the smallest Phase 6 engineering dispatch change.
- [x] Phase 6 can prefer explicit `engineering_scope` metadata when present.
- [x] Engineering-scoped Work Objects can route through `runtime.engineering`
      handoff proposal logic.
- [x] Existing business Phase 6 dispatch tests still pass.
- [x] Generic lifecycle routing remains the fallback when engineering scope is
      absent or false.
- [x] The slice verifies locally without deployment, live CI/CD mutation,
      adapter regeneration, or schema migration unless separately accepted.


## Constraints and non-goals

**Constraints:**
- Preserve current business routing behavior and precedence.
- Preserve generic Work Object lifecycle routing for non-engineering work.
- Use the verified engineering graph tracer from `2026-08-22-023` as source
  evidence; do not redesign the engineering operating pipeline in this slice.
- Keep canonical Work Object writes under governance/CLI control.
- Preserve unrelated dirty work already present in the repository.

**Non-goals:**
- No deployment or release.
- No live CI/CD, production, external service, or incident-system mutation.
- No adapter regeneration or global skill installation.
- No broad schema migration unless a design decision explicitly accepts it.
- No checkpointed engineering LangGraph router unless separately designed and
  accepted.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Accepted successor for Phase 6 engineering dispatch

| Field | Value |
|-------|-------|
| **Decision type** | decision / delegation |
| **Result** | pass |
| **Scope** | Create a successor Work Object for integrating engineering operating-pipeline routing into Phase 6 dispatch. The accepted successor covers design and later bounded implementation of explicit `engineering_scope` dispatch recognition, while preserving business and generic routing. |
| **Authorization** | User accepted the recommended successor after review of Work Object `2026-08-22-023` by saying "accept recommended successor". |
| **Confidence** | high for successor routing; medium for final integration shape — basis: the predecessor tracer verified local engineering graph projection and business/component governance seams, while Phase 6 engineering dispatch has not yet been designed. |
| **Actor** | user (acceptance), Codex (successor record) |
| **Revisit trigger** | Revisit if Phase 6 dispatch requires schema migration, checkpointed engineering router support, adapter regeneration, deployment authority, or live CI/CD/incident-system integration. |
| **Rationale** | The predecessor proved deterministic engineering graph routing locally; the next smallest useful slice is to let Phase 6 recognize engineering-scoped work without widening into deployment or production operations. |

### Decision 2 — Accepted Phase 6 engineering dispatch tracer

| Field | Value |
|-------|-------|
| **Decision type** | decision / authority |
| **Result** | pass |
| **Scope** | Implement the smallest Phase 6 engineering dispatch tracer: detect explicit `engineering_scope: true`, route the extracted next gap through `runtime.engineering`, store `engineering_route_result`, `engineering_handoff_envelope`, and normal `handoff_envelope`, let branch dispatch honor the routed engineering skill, preserve business routing precedence, and preserve generic fallback when engineering scope is absent or false. |
| **Authorization** | User accepted the immediately preceding tracer design by saying "accept this tracer and route to implementation". |
| **Confidence** | high for bounded dispatch seam; medium for future engineering router surface — basis: Phase 6 already has analogous business dispatch helpers and tests, while checkpointed engineering router and CLI surfaces are explicit non-goals. |
| **Actor** | user (acceptance), Codex (design record) |
| **Revisit trigger** | Revisit before adding a checkpointed engineering LangGraph router, CLI `run-engineering-router`, schema migration, adapter regeneration, deployment, live CI/CD, production, or incident-system integration. |
| **Rationale** | The accepted slice tests whether Phase 6 can consume the verified engineering graph projection as dispatch evidence without widening into a new router or production operations. |

**Accepted tracer-bullet design:**

- **Riskiest assumption:** Phase 6 can add `engineering_scope` dispatch recognition by mirroring the business dispatch seam without breaking business routing or generic lifecycle fallback.
- **Bounded path:** add Phase 6 engineering dispatch helpers that detect explicit `engineering_scope`, extract a next gap, call `runtime.engineering.route_engineering_frontier()` and `propose_engineering_handoff()`, and return runtime-only engineering payloads for branch dispatch.
- **State and output:** input is a Phase 6 Work Object with `engineering_scope: true`; output is a runtime `handoff_envelope` plus `engineering_route_result` and `engineering_handoff_envelope`; canonical Work Object state is not mutated by runtime dispatch.
- **Authorization boundary:** local repo edits and local tests only; no deployment, release, live CI/CD mutation, production, external service, incident system, adapter regeneration, or global install.
- **Failure behavior:** if engineering routing cannot parse or validate the handoff, stop and route back to design/governance rather than falling through silently as a false success.
- **Observability:** tests cover explicit `engineering_scope: true`, `engineering_scope: false`, branch propagation, business precedence, and preserved generic fallback.
- **Non-goals:** no checkpointed engineering LangGraph router, no CLI `run-engineering-router`, no schema migration, no adapter regeneration, no deployment, no live CI/CD or production integration.
- **Rollback:** remove the engineering Phase 6 helper functions, state keys, and tests; the existing business/generic dispatch path should remain intact.
- **Exit criteria:** new Phase 6 engineering dispatch tests pass; existing business Phase 6 tests pass; component governance tests pass; generic fallback proves `engineering_scope: false` does not route engineering; Work Object validates.

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [decision] | user | User accepted the recommended successor route after outcome review of Work Object 2026-08-22-023. |
| [system] | predecessor Work Object 2026-08-22-023 | Predecessor verified local engineering graph projection: direct runtime observation routed CI/verification gaps to engineering-verify-release-evidence and deployment rollback/recovery to operations-deploy-with-recovery; focused engineering/business/component-governance tests passed. |
| [decision] | user | User accepted the Phase 6 engineering dispatch tracer and requested routing to implementation. |
| [system] | Work Object Decision 2 | Accepted design bounds implementation to explicit engineering_scope Phase 6 dispatch helpers, runtime.engineering handoff proposal payloads, branch propagation, and tests preserving business precedence and generic fallback; checkpointed engineering router, CLI surface, schema migration, adapters, deployment, and live CI/CD are non-goals. |
| [system] | bounded implementation | Implemented explicit engineering_scope Phase 6 dispatch in runtime/graph.py, including engineering_route_result, engineering_handoff_envelope, normal handoff_envelope, branch propagation, inspect_phase6 exposure, business precedence, and generic fallback preservation. |
| [system] | verification command | uv run --python 3.11 python -m unittest runtime.tests.test_engineering_graph runtime.tests.test_business_graph tests.test_component_governance -v completed with 37 tests passing. |
| [system] | non-goal boundary check | No actual checkpointed engineering router or engineering CLI command symbols were added in runtime/graph.py or tools; deployment, adapter regeneration, schema migration, live CI/CD, production, and external integrations were not performed. |
| [system] | release-evidence runtime observation | Direct local Phase 6 observation verified engineering_scope dispatch: dispatch, branch_a, run_phase6 join, and inspect_phase6 all reported engineering-verify-release-evidence; governance_domain was engineering; engineering_route_result and engineering_handoff_envelope were present. |
| [system] | release-evidence focused tests | uv run --python 3.11 python -m unittest runtime.tests.test_engineering_graph runtime.tests.test_business_graph tests.test_component_governance -v completed with 37 tests passing during verify route. |
| [system] | release-evidence boundary check | Boundary check found no actual checkpointed engineering router or engineering CLI command symbols in runtime/graph.py or tools. |
| [gap] | release-evidence boundary | No live CI/CD, production deployment, external service, incident system, or release environment was exercised; verification is local release evidence only and makes no deployment or release-ready claim. Temporary SQLite scratch was left under the system temp directory to avoid a Windows cleanup lock during observation. |
## Open questions

- Resolved for this slice: `engineering_scope` is optional explicit metadata,
  not a required schema field or inferred signal.
- Resolved for this slice: Phase 6 engineering dispatch only proposes and
  propagates the engineering handoff; CLI inspection/approval and checkpointed
  engineering router surfaces are deferred.

## Next move

Route to `alawas-governance-review-outcome-and-adapt` to review the verified
local Phase 6 engineering dispatch tracer outcome and decide close versus next
slice. Do not deploy.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T13:52:04Z — Created successor for Phase 6 engineering dispatch

- **State:** design
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted the reviewed recommendation to create a bounded successor from verified local engineering graph projection into Phase 6 dispatch design.
### 2026-08-22T13:54:42Z — Accepted Phase 6 engineering dispatch tracer

- **State:** build
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted the bounded tracer design; implementation is scoped to explicit engineering_scope dispatch, runtime.engineering payloads, branch propagation, and preservation tests only.
### 2026-08-22T13:58:01Z — Implemented Phase 6 engineering dispatch tracer

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** The accepted bounded path was implemented locally and verified against engineering, business, and component-governance seams without deployment or broader router scope.
### 2026-08-22T14:00:35Z — Verified Phase 6 engineering dispatch tracer evidence

- **State:** observe
- **Status:** active
- **Actor:** codex
- **Rationale:** Accepted local tracer exit criteria were verified with direct runtime observation, focused tests, boundary checks, and Work Object validation; live CI/CD and deployment remain explicit gaps outside scope.
### 2026-08-22T14:00:50Z — Aligned observe-stage next move

- **State:** observe
- **Status:** active
- **Actor:** codex
- **Rationale:** The Work Object body now matches the observe-stage frontmatter next_action after release-evidence verification.
