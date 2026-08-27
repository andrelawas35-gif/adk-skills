---
schema_version: 1
id: 2026-08-24-007
title: P001 — Market Short project (V1 tracer)
type: project
status: active
state: design
consequence: meaningful
sensitivity: ordinary
domain: [architecture]
created_at: 2026-08-25T00:10:58Z
updated_at: 2026-08-25T01:39:51Z
next_action: P001 is the Market Short project root; sequences/scenes/shots build out under it (WO 2026-08-24-010).


---
## Intent

Seed Project node for the V1 Production Objects tracer (WO 2026-08-24-006
Decision 2). Top of the Project → Sequence → Scene → Shot hierarchy.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [ ] P001 is the top of the Market Short production hierarchy (Sequence SQ001 → Scene SC030 → Shot SH001), linked via `ws relation` and traversable via `ws graph`
- [ ] P001 is a real production record with a meaningful lifecycle state


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
| [system] | V1 build-out (WO 2026-08-24-010), ws relation + ws graph trace | P001 is the top of the Market Short production hierarchy — linked via ws relation (depends_on chain Shot SH001 2026-08-24-009 → Scene SC030 2026-08-23-004 → Sequence SQ001 2026-08-24-008 → Project P001) and traversable via ws graph trace. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

Continue the Market Short build-out (WO 2026-08-24-010): Sequence SQ001
and its scene/shot produce under P001.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-25T01:39:15Z — Build-out: P001 promoted to a real production project record

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** V1 build-out (WO 2026-08-24-010): the seed Project P001 is promoted out of notice to design as the top of the Market Short production hierarchy.
