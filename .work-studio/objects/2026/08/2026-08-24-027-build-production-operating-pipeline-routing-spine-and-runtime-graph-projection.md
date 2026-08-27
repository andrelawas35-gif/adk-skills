---
schema_version: 1
id: 2026-08-24-027
title: Build production operating pipeline routing spine and runtime graph projection
type: change
status: active
state: notice
consequence: meaningful
sensitivity: ordinary
domain: [production, architecture]
created_at: 2026-08-25T01:57:18Z
updated_at: 2026-08-25T01:57:18Z
next_action: "Awaiting activation/classification (notice state)"
---
## Intent

Define the production domain's two-layer operating pipeline. Layer A is the
creative routing spine — the ownership map and handoff rules for production
work, following the same pattern as `BUSINESS-OPERATING-PIPELINE.md` and
`ENGINEERING-OPERATING-PIPELINE.md`. Layer B is the GPU execution graph — a
new pattern with no precedent in the existing system, defining how GPU-bound
work is sequenced, queued, and tracked across the three operators (Blender,
ComfyUI Flux, ComfyUI Hunyuan3D).

Creates `references/PRODUCTION-OPERATING-PIPELINE.md` as the canonical
reference document. Projects into the runtime graph (WO `2026-08-22-016`).

Parent: WO `2026-08-23-001` §6. Component: COMP-055.

## Success evidence

- [ ] `references/PRODUCTION-OPERATING-PIPELINE.md` authored with Layer A and Layer B
- [ ] Layer A follows ownership-map pattern from business/engineering pipelines
- [ ] Layer B defines GPU execution graph with state machine and queue semantics
- [ ] Pipeline integrates with GPU orchestration protocol (`2026-08-24-013`)
- [ ] Projects into runtime graph alongside business and engineering pipelines


## Constraints and non-goals

**Constraints:**
- Layer A must follow the established pipeline reference document pattern
- Layer B is genuinely new — no forcing it into the routing-spine pattern
- Must be compatible with runtime graph projection (WO `2026-08-22-016`)

**Non-goals:**
- No implementation of the GPU scheduler (protocol only, per `2026-08-24-013`)
- No changes to business or engineering pipelines
- No runtime graph implementation (that's a separate WO)

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — <summary>

| Field | Value |
|-------|-------|
| **Decision type** | decision / authority / delegation |
| **Result** | pass / fail / pending |
| **Scope** | <!-- what this decision applies to --> |
| **Authorization** | <!-- who or what authorized this --> |
| **Confidence** | <!-- high / medium / low, plus basis. Scope-qualify when the decision's parts differ: 'high for <X>; low for <Y> — basis: <why>' --> |
| **Actor** | <!-- who made the decision --> |
| **Revisit trigger** | <!-- condition that would cause reconsideration --> |
| **Rationale** | <!-- why this decision was made --> |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|


## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

<!-- The single next action this Work Object routes to. -->

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
