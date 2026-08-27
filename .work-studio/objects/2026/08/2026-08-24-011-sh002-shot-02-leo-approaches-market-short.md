---
schema_version: 1
id: 2026-08-24-011
title: SH002 — Shot 02: Leo approaches (Market Short)
type: project
status: active
state: build
consequence: low
sensitivity: ordinary
domain: [architecture]
created_at: 2026-08-25T01:52:37Z
updated_at: 2026-08-25T01:54:19Z
next_action: SH002 is canon (CANON-002); further shots build under the shot state machine (WO 2026-08-24-010).


shot_status: approved






---
## Intent

Real Market Short shot (beat 02): Leo approaches, casual encounter. Build-out
continuation (WO 2026-08-24-010); positioned under Scene SC030 2026-08-23-004.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] SH002 is a real Market Short shot (beat 02), shot_status approved, recorded as CANON-002


## Constraints and non-goals

**Constraints:**
<!-- Boundaries the implementation must respect. -->

**Non-goals:**
<!-- Explicitly excluded work. -->

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
| [system] | V1 build-out (WO 2026-08-24-010), ws shot-status + ws relation | SH002 is a production shot record (beat 02: Leo approaches) — shot_status approved (blocking → animation → render → review → approved via ws shot-status), linked depends_on Scene SC030 2026-08-23-004, recorded as CANON-002. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

<!-- The single next action this Work Object routes to. -->

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-25T01:53:17Z — Shot status: none → blocking

- **State:** notice
- **Status:** active
- **Actor:** system
- **Rationale:** Shot state machine transition (V1, WO 2026-08-24-006).
### 2026-08-25T01:53:18Z — Shot status: blocking → animation

- **State:** notice
- **Status:** active
- **Actor:** system
- **Rationale:** Shot state machine transition (V1, WO 2026-08-24-006).
### 2026-08-25T01:53:19Z — Shot status: animation → render

- **State:** notice
- **Status:** active
- **Actor:** system
- **Rationale:** Shot state machine transition (V1, WO 2026-08-24-006).
### 2026-08-25T01:53:20Z — Shot status: render → review

- **State:** notice
- **Status:** active
- **Actor:** system
- **Rationale:** Shot state machine transition (V1, WO 2026-08-24-006).
### 2026-08-25T01:53:21Z — Shot status: review → approved

- **State:** notice
- **Status:** active
- **Actor:** system
- **Rationale:** Shot state machine transition (V1, WO 2026-08-24-006).
### 2026-08-25T01:54:05Z — Build-out: SH002 promoted to a production shot record (lifecycle build; shot_status approved)

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** V1 build-out (WO 2026-08-24-010): SH002 promoted out of notice to a production shot record; shot_status approved, recorded as CANON-002.
## Relationships

  REL-2026_08_24_011-001:
    type: depends_on
    from: wo:2026-08-24-011
    to: wo:2026-08-23-004
    basis: "V1 build-out WO 2026-08-24-010"
    created_at: 2026-08-25T01:53:06Z
