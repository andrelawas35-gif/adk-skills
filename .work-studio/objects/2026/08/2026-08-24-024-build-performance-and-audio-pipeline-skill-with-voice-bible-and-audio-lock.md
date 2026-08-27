---
schema_version: 1
id: 2026-08-24-024
title: Build performance and audio pipeline skill with voice bible and audio lock
type: change
status: active
state: notice
consequence: low
sensitivity: ordinary
domain: [production]
created_at: 2026-08-25T01:57:14Z
updated_at: 2026-08-25T01:57:14Z
next_action: "Awaiting activation/classification (notice state)"
---
## Intent

Translate directorial performance notes into structured TTS parameters and
manage the voice/audio lifecycle for each character. Maintains a voice bible
(voice_id, style parameters, emotional range per character). Orchestrates the
TTS operator (`2026-08-24-016`) to generate takes, presents A/B/C/D takes for
director selection, and locks approved audio to shots. Audio lock means the
shot's timing is now driven by the approved take's duration.

Parent: WO `2026-08-23-001` §5.2. Component: COMP-052.

## Success evidence

- [ ] Maintains a voice bible with per-character voice profiles
- [ ] Translates performance direction ("angry but restrained") into TTS parameters
- [ ] Generates multiple takes via TTS operator and presents for selection
- [ ] Locks selected audio to shots, setting shot duration from take length
- [ ] Tracks audio version history per shot


## Constraints and non-goals

**Constraints:**
- Director selects takes — this pipeline presents, never chooses
- Audio lock is a governance-level commitment (changes require director override)
- Voice bible is the single source of truth for character voices

**Non-goals:**
- No sound effects or music (separate concern)
- No voice acting or performance quality judgment
- No lip sync (future capability, depends on animation system)

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
