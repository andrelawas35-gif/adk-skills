---
schema_version: 1
id: 2026-08-22-016
title: Promote business operating pipeline into graph runtime tracer
type: change
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
domain: [business, architecture, engineering]
created_at: 2026-08-22T13:05:34Z
updated_at: 2026-08-22T13:09:03Z
next_action: Route to alawas-engineering-verify-release-evidence for review of the business graph runtime tracer; later LangGraph business-router promotion remains a separate slice.







---
## Intent

Promote the accepted business operating pipeline from reference guidance into a
bounded runtime graph tracer: a deterministic NetworkX projection of the route,
a Pydantic business handoff proposal schema, and a plain-language frontier
router. The tracer must remain read-only and must not mutate canonical Work
Objects, live business systems, money, personnel, suppliers, customers, or
external records.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] Runtime can parse `references/BUSINESS-OPERATING-PIPELINE.md` into a
      deterministic business route and ownership map.
- [x] Runtime can build a NetworkX business skill graph from that canonical
      route.
- [x] Runtime can route a plain-language business frontier to an owning
      business skill.
- [x] Runtime can emit a strict Pydantic business handoff envelope that rejects
      skill/domain mismatches.
- [x] Focused tests cover the business graph, frontier router, Pydantic
      envelope, component-governance aliasing, and existing Work Object
      projection invariants.


## Constraints and non-goals

**Constraints:**
<!-- Boundaries the implementation must respect. -->
- Source of truth remains `references/BUSINESS-OPERATING-PIPELINE.md`.
- Runtime projection is advisory/runtime-plane only, never canonical truth.
- Preserve the Work Object lifecycle as the governing lifecycle route.
- Preserve existing NetworkX Work Object projection behavior.
- Preserve strict governance-domain validation for routed skills.

**Non-goals:**
<!-- Explicitly excluded work. -->
- No live business-system mutation.
- No CRM, supplier, customer, money, pricing-publication, personnel, or external
  commitment action.
- No full LangGraph business subgraph beyond the first graph-runtime tracer.
- No replacement of the Work Object lifecycle or existing handoff graph.
- No cleanup of unrelated dirty worktree changes.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Implement first business graph runtime tracer

| Field | Value |
|-------|-------|
| **Decision type** | bounded-change |
| **Result** | pass |
| **Scope** | Implement the accepted recommendation's first three graph capabilities: business skill graph projection, business frontier router, and Pydantic business handoff schema. |
| **Authorization** | Director asked whether business skills were integrated with LangGraph/Pydantic/NetworkX, then said "do recommendation" after the recommended first slice was named. |
| **Confidence** | medium-high — basis: repository evidence showed business governance already exists in runtime handoffs, while the business operating pipeline remained reference-only and explicitly listed deterministic runtime routing as a revisit trigger. |
| **Actor** | director |
| **Revisit trigger** | Real business Work Object use shows the frontier router needs richer evidence extraction, the runtime needs a checkpointed LangGraph business router, or the graph must include business entities beyond skills. |
| **Rationale** | The smallest useful promotion is a read-only graph tracer over the canonical business pipeline, not a live business operations engine. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [gap] | ws transition audit (verify) | No decision record with result: pass and populated scope found. Requirement coverage evidence is expected before verify transition. |
| [system] | runtime/business.py; runtime/tests/test_business_graph.py; tools/ws/component_governance.py | Implemented the first business graph runtime tracer: parses BUSINESS-OPERATING-PIPELINE.md, builds a NetworkX DiGraph of the business route, routes plain-language business frontiers to owning skills, emits strict Pydantic BusinessHandoffEnvelope proposals, normalizes alawas-* adapter names to runtime core skill names, and declares governance aliases for governance-govern-scorecards and governance-review-outcome-and-adapt. |
| [system] | uv run --python 3.11 python -m unittest runtime.tests.test_business_graph tests.test_component_governance runtime.tests.test_projection -v | Focused verification passed: 38 tests ran successfully across the new business graph tracer, component-governance runtime enforcement, and existing NetworkX Work Object projection invariants. |
| [system] | Work Object decision record repair, 2026-08-22 | Removed the leftover placeholder decision table so Decision 1 now presents a single populated pass decision for the accepted business graph runtime tracer. The earlier transition audit gap is retained as historical evidence of the pre-repair record shape, not as the current decision state. |
| [system] | runtime/tests/test_business_graph.py | The new test module covers five checked success outcomes: parsing the canonical pipeline reference, building the NetworkX graph, routing frontier text, validating the Pydantic business handoff envelope, and rejecting mismatched governance domains. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

Route to `alawas-engineering-verify-release-evidence` for release-evidence
review of the read-only business graph runtime tracer. A checkpointed LangGraph
business-router promotion remains a separate future slice.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T13:08:19Z — Created and bounded accepted business graph tracer

- **State:** notice
- **Status:** active
- **Actor:** codex
- **Rationale:** Director accepted the recommended first graph-runtime slice: business skill graph projection, frontier router, and Pydantic business handoff schema; scope is read-only runtime tracer only.
### 2026-08-22T13:08:20Z — Implemented accepted business graph runtime tracer

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** Added runtime/business.py, tests for the business graph projection/router/handoff schema, and governance aliases needed for the canonical business route; focused verification passed.
### 2026-08-22T13:08:47Z — Repaired decision record shape

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** The verify transition audit saw the template decision table before cleanup; the Work Object now has one populated pass decision and a concrete next move.
