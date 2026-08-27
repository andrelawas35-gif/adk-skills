---
schema_version: 1
id: 2026-08-24-012
title: SH003 — Shot 03: the name lands (Market Short)
type: project
status: active
state: build
consequence: low
sensitivity: ordinary
domain: [architecture]
created_at: 2026-08-25T01:52:37Z
updated_at: 2026-08-25T02:19:21Z
next_action: SH003 is canon (CANON-003), shot_status approved via ws shot-status. Further shots build under the shot state machine (WO 2026-08-24-010).


shot_status: approved








---
## Intent

Real Market Short shot (beat 03): the name lands, Mara's hand stops. Build-out
continuation (WO 2026-08-24-010); positioned under Scene SC030 2026-08-23-004.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] SH003 is a real Market Short shot (beat 03), shot_status approved (blocking → animation → render → review → approved via ws shot-status), recorded as CANON-003


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
| [system] | V1 build-out (WO 2026-08-24-010), ws shot-status + ws relation | SH003 is a production shot record (beat 03: the name lands) — shot_status render (in progress via ws shot-status: blocking → animation → render), linked depends_on Scene SC030 2026-08-23-004. |
| [system] | verify-release-evidence follow-up (2026-08-25): SH003 approved record repair | SH003 reached shot_status approved via ws shot-status (blocking → animation → render → review → approved, distinct seconds 02:02:37Z/02:02:38Z) and is recorded as CANON-003 in canon-registry.md. This supersedes the earlier evidence row that described the in-progress render state. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

<!-- The single next action this Work Object routes to. -->

SH003 is canon (CANON-003), shot_status approved via ws shot-status. Further
shots build under the shot state machine (WO 2026-08-24-010).

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-25T01:53:22Z — Shot status: none → blocking

- **State:** notice
- **Status:** active
- **Actor:** system
- **Rationale:** Shot state machine transition (V1, WO 2026-08-24-006).
### 2026-08-25T01:53:23Z — Shot status: blocking → animation

- **State:** notice
- **Status:** active
- **Actor:** system
- **Rationale:** Shot state machine transition (V1, WO 2026-08-24-006).
### 2026-08-25T01:53:24Z — Shot status: animation → render

- **State:** notice
- **Status:** active
- **Actor:** system
- **Rationale:** Shot state machine transition (V1, WO 2026-08-24-006).
### 2026-08-25T01:54:06Z — Build-out: SH003 promoted to a production shot record (lifecycle build; shot_status render, in progress)

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** V1 build-out (WO 2026-08-24-010): SH003 promoted out of notice to a production shot record; shot_status render (in progress).
### 2026-08-25T02:02:37Z — Shot status: render → review

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** Shot state machine transition (V1, WO 2026-08-24-006).
### 2026-08-25T02:02:38Z — Shot status: review → approved

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** Shot state machine transition (V1, WO 2026-08-24-006).
### 2026-08-25T02:19:21Z — Record repair: Success evidence + evidence ledger corrected to approved; next_action synced

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** Verification follow-up (WO 2026-08-24-010): SH003's body record updated to reflect its actual approved state — Success evidence checkbox text corrected (render → approved) and ticked, corrected evidence row appended (CLI), next_action synced to canon.
## Relationships

  REL-2026_08_24_012-001:
    type: depends_on
    from: wo:2026-08-24-012
    to: wo:2026-08-23-004
    basis: "V1 build-out WO 2026-08-24-010"
    created_at: 2026-08-25T01:53:06Z
