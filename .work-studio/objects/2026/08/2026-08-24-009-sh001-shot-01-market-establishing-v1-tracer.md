---
schema_version: 1
id: 2026-08-24-009
title: SH001 — Shot 01 market establishing (V1 tracer)
type: project
status: active
state: build
consequence: low
sensitivity: ordinary
domain: [architecture]
shot_status: approved
shot_tier: hero
created_at: 2026-08-25T00:10:58Z
updated_at: 2026-08-25T02:19:47Z
next_action: SH001 is the first canon entry; further shots build under the shot state machine (WO 2026-08-24-010).








---
## Intent

Seed Shot node for the V1 Production Objects tracer (WO 2026-08-24-006
Decision 2). Leaf of the Project → Sequence → Scene → Shot hierarchy;
carries the shot_status / shot_tier metadata fields.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] SH001 is a real production shot record (shot_status: approved; shot_tier: hero), positioned under Scene SC030
- [x] SH001 carries its production state via `ws shot-status` and is recorded as the first canon entry


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
| [system] | V1 build-out (WO 2026-08-24-010), ws shot-status | SH001 is a production shot record — shot_status approved (via ws shot-status: blocking → animation → render → review → approved), shot_tier hero, positioned under Scene SC030 2026-08-23-004; recorded as the first director-approved canon entry (CANON-001). |
| [system] | verify-release-evidence follow-up (2026-08-25): SH001 record repair | SH001's production state is carried via ws shot-status (blocking → animation → render → review → approved) and it is recorded as the first director-approved canon entry, CANON-001, in canon-registry.md. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

Continue the Market Short build-out (WO 2026-08-24-010): SH001 is the first
canon entry; further shots build under the shot state machine.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-25T00:18:00Z — Shot status: blocking → animation

- **State:** notice
- **Status:** active
- **Actor:** system
- **Rationale:** Shot state machine transition (V1, WO 2026-08-24-006).
### 2026-08-25T00:18:06Z — Shot status: animation → render

- **State:** notice
- **Status:** active
- **Actor:** system
- **Rationale:** Shot state machine transition (V1, WO 2026-08-24-006).
### 2026-08-25T00:18:11Z — Shot status: render → review

- **State:** notice
- **Status:** active
- **Actor:** system
- **Rationale:** Shot state machine transition (V1, WO 2026-08-24-006).
### 2026-08-25T00:18:16Z — Shot status: review → approved

- **State:** notice
- **Status:** active
- **Actor:** system
- **Rationale:** Shot state machine transition (V1, WO 2026-08-24-006).
### 2026-08-25T01:39:16Z — Build-out: SH001 promoted to a production shot record (lifecycle build; shot_status approved)

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** V1 build-out (WO 2026-08-24-010): the seed Shot SH001 is promoted out of notice to a production shot record; its shot_status is approved and it is the first canon entry.
## Relationships

  REL-2026_08_24_009-001:
    type: depends_on
    from: wo:2026-08-24-009
    to: wo:2026-08-23-004
    basis: "V1 tracer Decision 2"
    created_at: 2026-08-25T00:11:20Z
