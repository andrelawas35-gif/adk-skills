---
schema_version: 1
id: 2026-08-22-029
title: Manage liquidity and cash runway
type: change
status: active
state: explore
consequence: meaningful
sensitivity: private
created_at: 2026-08-22T15:07:45Z
updated_at: 2026-08-22T15:07:56Z
next_action: Awaiting real inputs from director: currency, horizon, current cash position, cash availability, dated obligations, expected inflows, cash-timing evidence, constraints, owner, and the liquidity decision or escalation threshold to evaluate. No financial figures are fabricated.


---
## Intent

<!-- Describe what this Work Object accomplishes and why it exists. -->

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [ ] 


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
| [decision] | Director request, business-manage-liquidity-and-cash-runway skill activation | Opened per director request to give business-manage-liquidity-and-cash-runway a real decision Work Object. Closes the gap identified in WO 2026-08-22-026 Decision 1: the first business typed edge (via ws relation add) had no real business decision to attach to. This object is the real decision, not a demo. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

<!-- The single next action this Work Object routes to. -->

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T15:07:45Z — Started via ws start (created + evidence + explore + activate supporting)

- **State:** explore
- **Status:** active
- **Actor:** governance-conduct-work-object
- **Rationale:** Financial records default to private sensitivity per the skill's own consequence/authority rules. Consequence set to meaningful per director choice (not an active/near-term crisis).

## Relationships

  REL-2026_08_22_029-001:
    type: responds_to
    from: wo:2026-08-22-029
    to: wo:2026-08-22-026
    basis: "Opened to satisfy WO 2026-08-22-026 Decision 1's deferred business-edge exit criterion"
    created_at: 2026-08-22T15:07:56Z
