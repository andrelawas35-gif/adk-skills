---
schema_version: 1
id: 2026-08-24-026
title: Build precedent harvester skill for automated recipe extraction from closed Work Objects
type: change
status: active
state: notice
consequence: low
sensitivity: ordinary
domain: [production]
created_at: 2026-08-25T01:57:17Z
updated_at: 2026-08-25T01:57:17Z
next_action: "Awaiting activation/classification (notice state)"
---
## Intent

Automatically extract validated production techniques from closed Work Objects
and register them in the precedent ledger (`.work-studio/precedent-ledger.md`).
When a production Work Object reaches `closed` state with successful evidence,
this skill extracts the repeatable recipe: what tools were used, what
parameters worked, what constraints applied, and what the hardware requirements
were. Builds the Creative Precedent Library that the scene planner queries.

Parent: WO `2026-08-23-001` §5.5. Component: COMP-054.

## Success evidence

- [ ] Triggers on Work Object close events in the production domain
- [ ] Extracts structured recipe: tools, parameters, constraints, hardware
- [ ] Registers new precedent entries in `precedent-ledger.md`
- [ ] Links precedent back to source Work Object for full provenance
- [ ] Scene planner (`2026-08-24-017`) can query precedents by technique type


## Constraints and non-goals

**Constraints:**
- Only harvests from successfully closed WOs — failed attempts are not precedents
- Precedent entries must include hardware validation (which GPU, how much VRAM)
- Must not modify the source Work Object

**Non-goals:**
- No technique invention — only captures what actually worked
- No precedent ranking or recommendation (scene planner's judgment)
- No cross-project precedent sharing (single-studio scope)

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
