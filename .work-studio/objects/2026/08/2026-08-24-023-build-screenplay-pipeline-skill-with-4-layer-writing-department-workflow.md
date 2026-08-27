---
schema_version: 1
id: 2026-08-24-023
title: Build screenplay pipeline skill with 4-layer writing department workflow
type: change
status: active
state: notice
consequence: low
sensitivity: ordinary
domain: [production]
created_at: 2026-08-25T01:57:09Z
updated_at: 2026-08-25T01:57:09Z
next_action: "Awaiting activation/classification (notice state)"
---
## Intent

Break down a screenplay or story document into structured production data:
scenes, shots, characters, locations, props, and dialogue. Follows a 4-layer
workflow: Layer 1 (story structure — acts, sequences, beats), Layer 2
(scene breakdown — location, time, characters, action), Layer 3 (shot list
— camera, framing, duration, transitions), Layer 4 (production requirements
— assets needed, effects, audio cues). Outputs feed the shot pipeline and
asset pipeline.

Parent: WO `2026-08-23-001` §5.7. Component: COMP-051.

## Success evidence

- [ ] Accepts a screenplay/story document and produces structured breakdown
- [ ] Generates scene-level breakdown with location, characters, props
- [ ] Generates shot list with camera descriptions and estimated durations
- [ ] Identifies required assets and flags missing ones against the asset registry
- [ ] Output is directly consumable by shot pipeline (`2026-08-24-021`)


## Constraints and non-goals

**Constraints:**
- Breakdown is mechanical extraction, not creative rewriting
- Must preserve director's original intent — no editorial changes
- Shot list is a suggestion; director approves before it drives production

**Non-goals:**
- No screenplay writing or dialogue generation
- No creative story decisions
- No storyboard generation (visual work belongs to other pipelines)

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
