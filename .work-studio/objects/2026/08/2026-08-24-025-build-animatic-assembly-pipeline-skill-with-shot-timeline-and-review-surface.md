---
schema_version: 1
id: 2026-08-24-025
title: Build animatic assembly pipeline skill with shot timeline and review surface
type: change
status: active
state: notice
consequence: low
sensitivity: ordinary
domain: [production]
created_at: 2026-08-25T01:57:15Z
updated_at: 2026-08-25T01:57:15Z
next_action: "Awaiting activation/classification (notice state)"
---
## Intent

Assemble individual shot renders into a timed sequence (animatic) for director
review. Manages the shot timeline: ordering, duration, transitions, and audio
sync. Produces a reviewable output (video file or frame sequence with audio
track) that represents the current state of a scene or sequence. The review
surface is the director's primary tool for evaluating pacing and flow.

Parent: WO `2026-08-23-001` §5.8. Component: COMP-053.

## Success evidence

- [ ] Assembles shot renders into a timed sequence
- [ ] Respects audio-locked shot durations from performance pipeline
- [ ] Supports reordering, trimming, and transition specification
- [ ] Produces reviewable video output with audio track
- [ ] Tracks sequence versions and director notes per review cycle


## Constraints and non-goals

**Constraints:**
- Shot order and timing are director decisions — this skill assembles, not edits
- Audio-locked shots cannot be retimed without director override
- Output format must be playable without specialized tools

**Non-goals:**
- No color grading or compositing (future post-production concern)
- No editorial pacing decisions
- No final export or delivery formatting

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
