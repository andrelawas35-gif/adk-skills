---
schema_version: 1
id: 2026-08-22-023
title: Design engineering operating pipeline graph capabilities
type: change
status: active
state: observe
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-22T13:35:42Z
updated_at: 2026-08-22T13:52:32Z
next_action: Successor Work Object 2026-08-22-024 owns the next slice; predecessor can be closed after outcome review if no further predecessor-specific decision is needed.























---
## Intent

Design the smallest governed tracer bullet for adding engineering operations
and pipeline capabilities to the Work Studio graph system. The target capability
is an engineering operating pipeline parallel to the business operating
pipeline, projected into NetworkX/Pydantic/LangGraph without replacing the Work
Object lifecycle or granting deployment authority.

## Success evidence

- [x] A bounded tracer-bullet design exists for `references/ENGINEERING-OPERATING-PIPELINE.md`.
- [x] The design names the minimal `runtime/engineering.py` projection surface.
- [x] The design defines the Pydantic handoff envelope and NetworkX route graph acceptance checks.
- [x] The design states how Phase 6 should eventually recognize `engineering_scope` without breaking business or generic lifecycle routing.
- [x] The design records non-goals, rollback, observability, and exit criteria before implementation.


## Constraints and non-goals

**Constraints:**
- Preserve canonical non-writer runtime behavior.
- Do not implement the pipeline until a tracer bullet is accepted.
- Do not modify live repositories, CI systems, deployments, production, or
  external services.
- Fit the existing domains in `tools/ws/component_governance.py`:
  engineering, operations, governance, design, and cross-cutting.
- Preserve unrelated dirty work already present in the repository.

**Non-goals:**
- No adapter regeneration.
- No global skill installation.
- No production release, deployment, or incident-system integration.
- No schema migration in this design slice.
- No broad engineering roadmap beyond the first tracer bullet.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Route engineering graph capabilities to tracer-bullet design

| Field | Value |
|-------|-------|
| **Decision type** | decision / delegation |
| **Result** | pass |
| **Scope** | Create a design-stage Work Object for an engineering operating pipeline and graph projection tracer; no implementation yet. |
| **Authorization** | User said "go ahead and route it" after the live-question recommendation routed the idea as prototype-ready. |
| **Confidence** | high for routing; medium for final capability shape — basis: current repo already has business pipeline precedent, Phase 6 routing, NetworkX projection, Pydantic handoffs, and engineering/operations/governance domains. |
| **Actor** | Codex |
| **Revisit trigger** | Revisit if design evidence shows engineering should be handled by lifecycle routing only, or if existing operations skills need expansion before runtime projection. |
| **Rationale** | A tracer-bullet design prevents a broad engineering-ops architecture from ballooning; it should first prove one pipeline reference plus one runtime projection can route engineering frontiers deterministically. |

### Decision 2 — Accepted engineering operating-pipeline tracer bullet

| Field | Value |
|-------|-------|
| **Decision type** | decision / authority |
| **Result** | pass |
| **Scope** | Implement the first engineering operating-pipeline tracer: add `references/ENGINEERING-OPERATING-PIPELINE.md`, add minimal `runtime/engineering.py`, and add focused parser/NetworkX/Pydantic routing tests for engineering frontiers. |
| **Authorization** | User accepted the immediately preceding tracer-bullet design by saying "accept". |
| **Confidence** | high for bounded implementation scope; medium for later Phase 6 integration — basis: this design mirrors the already-tested business operating-pipeline pattern but defers `engineering_scope` and checkpointed router integration. |
| **Actor** | user (acceptance), Codex (design record) |
| **Revisit trigger** | Revisit before adding Phase 6 `engineering_scope`, checkpointed engineering LangGraph router, schema migration, adapter regeneration, or any live CI/CD/deployment/incident integration. |
| **Rationale** | The smallest useful engineering slice proves a canonical pipeline reference plus deterministic runtime projection can route CI/verification and deployment/recovery frontiers without changing canonical state or touching external systems. |

**Accepted tracer-bullet design:**

- **Riskiest assumption:** a small engineering operating-pipeline reference plus `runtime/engineering.py` can route engineering frontiers deterministically without disturbing Work Object lifecycle routing, business routing, or canonical non-writer guarantees.
- **Bounded path:** add `references/ENGINEERING-OPERATING-PIPELINE.md`; add `runtime/engineering.py` with `EngineeringPipelineSpec`, `EngineeringFrontierRoute`, `EngineeringHandoffEnvelope`, `load_engineering_pipeline_spec()`, `build_engineering_skill_graph()`, `route_engineering_frontier()`, `engineering_path()`, and `propose_engineering_handoff()`; add focused tests.
- **Primary frontier to prove:** `CI failure / verification gap` routes to `engineering-verify-release-evidence`.
- **Secondary frontier:** `deployment rollback / recovery` routes to `operations-deploy-with-recovery`.
- **Authorization boundary:** local repo edits and local tests only; no deployment, live CI mutation, production, incident system, or external service access.
- **Failure behavior:** if parsing, domain mapping, or handoff validation fails, stop and route to design or governance repair rather than widening scope.
- **Observability:** focused tests show deterministic parsing, graph edges/domains, frontier routing, handoff validation, and preserved business/component governance checks.
- **Non-goals:** no Phase 6 `engineering_scope`, no checkpointed engineering router, no schema migration, no adapter regeneration, no live CI/CD or production integration.
- **Rollback:** remove the new reference, runtime module, and tests; no canonical or external runtime state should be changed.
- **Exit criteria:** focused engineering graph tests pass; existing business graph tests pass; component governance tests pass; Work Object validates.

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | references/BUSINESS-OPERATING-PIPELINE.md | Business domain already has a canonical operating pipeline reference with route, ownership map, handoff rules, minimum handoff record, and revisit triggers. |
| [system] | runtime/business.py | Business runtime already demonstrates the target implementation pattern: NetworkX route graph, Pydantic business handoff envelope, deterministic frontier router, and checkpointed LangGraph router. |
| [system] | runtime/graph.py | Phase 6 dispatch now carries domain-specific routing payloads and explicit scope handling for business routing, providing a runtime integration precedent for engineering_scope. |
| [system] | tools/ws/component_governance.py | Component governance taxonomy already recognizes engineering, operations, governance, design, and cross-cutting domains. |
| [system] | skills/core | Current engineering/operations skill set includes engineering-implement-bounded-change, engineering-verify-release-evidence, operations-deploy-with-recovery, and operations-diagnose-production-incident. |
| [inference] | investigation synthesis | The smallest useful next move is a tracer-bullet design for an engineering operating pipeline reference plus runtime projection, before implementation or Phase 6 engineering_scope integration. |
| [decision] | user | User accepted the proposed engineering operating-pipeline tracer-bullet design by saying "accept". |
| [system] | Work Object Decision 2 | Accepted design bounds implementation to ENGINEERING-OPERATING-PIPELINE reference, runtime/engineering.py projection, and focused tests; Phase 6 engineering_scope and live CI/CD are explicit non-goals. |
| [system] | bounded implementation | Added references/ENGINEERING-OPERATING-PIPELINE.md, runtime/engineering.py, runtime/tests/test_engineering_graph.py, and engineering/operations aliases in tools/ws/component_governance.py within the accepted tracer boundary. |
| [system] | verification command | uv run --python 3.11 python -m unittest runtime.tests.test_engineering_graph runtime.tests.test_business_graph tests.test_component_governance -v completed with 31 tests passing. |
| [system] | release-evidence runtime observation | Direct local runtime observation loaded the engineering pipeline graph: 8 route entries, 7 nodes, 7 edges; CI/verification gap routed high-confidence to engineering-verify-release-evidence; deployment rollback recovery routed high-confidence to operations-deploy-with-recovery; unknown frontier fell back low-confidence to engineering-implement-bounded-change. |
| [system] | release-evidence focused tests | uv run --python 3.11 python -m unittest runtime.tests.test_engineering_graph runtime.tests.test_business_graph tests.test_component_governance -v completed with 31 tests passing during verify route. |
| [gap] | release-evidence boundary | No live CI/CD, production deployment, external service, incident system, or release environment was exercised; this verification is local release evidence only and makes no deployment or release-ready claim. |
| [decision] | user | User accepted the recommended successor route: create Work Object 2026-08-22-024 for Phase 6 engineering dispatch integration. |
## Open questions

- What is the smallest engineering frontier that should prove the pipeline:
  CI failure, implementation slice, release gate, dependency risk, or incident
  diagnosis?
- Should `engineering_scope` be explicit frontmatter from the start, or remain
  a later Phase 6 integration slice?

## Next move

Route to `alawas-governance-review-outcome-and-adapt` to review the verified
local tracer outcome and decide close versus next slice. Do not deploy.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T13:36:20Z — Routed engineering graph capability recommendation to tracer-bullet design

- **State:** design
- **Status:** active
- **Actor:** codex
- **Rationale:** Live-question investigation found no engineering-native operating pipeline yet; business pipeline and Phase 6 routing provide the precedent for a bounded design slice.
### 2026-08-22T13:36:44Z — Prepared design route for engineering operating pipeline graph capabilities

- **State:** design
- **Status:** active
- **Actor:** codex
- **Rationale:** The Work Object now contains the investigation evidence, bounded design constraints, and next specialist route for a tracer-bullet design.
### 2026-08-22T13:39:28Z — Accepted engineering operating-pipeline tracer design

- **State:** build
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted the proposed bounded tracer; implementation is now scoped to the reference, runtime projection, and focused tests only.
### 2026-08-22T13:39:39Z — Recorded accepted tracer-bullet design and routed to implementation

- **State:** build
- **Status:** active
- **Actor:** codex
- **Rationale:** The design is now accepted and the next specialist route is bounded implementation.
### 2026-08-22T13:44:17Z — Implemented engineering operating-pipeline tracer

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** The accepted bounded path was implemented locally and the engineering/business/component-governance seam passed focused verification.
### 2026-08-22T13:44:38Z — Updated verify-stage next move

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** The Work Object body now matches the verify-stage frontmatter next_action after bounded implementation.
### 2026-08-22T13:47:50Z — Verified engineering operating-pipeline tracer evidence

- **State:** observe
- **Status:** active
- **Actor:** codex
- **Rationale:** Accepted local tracer exit criteria were verified with direct runtime observation, focused tests, governance checks, and Work Object validation; deployment and live CI/CD remain explicit gaps outside scope.
### 2026-08-22T13:48:03Z — Aligned observe-stage next move

- **State:** observe
- **Status:** active
- **Actor:** codex
- **Rationale:** The Work Object body now matches the observe-stage frontmatter next_action after release-evidence verification.
### 2026-08-22T13:52:32Z — Accepted successor route

- **State:** observe
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted creating successor Work Object 2026-08-22-024 for Phase 6 engineering dispatch integration after local tracer review.
