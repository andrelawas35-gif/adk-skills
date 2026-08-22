---
schema_version: 1
id: 2026-08-22-029
title: Manage liquidity and cash runway
type: change
status: active
state: observe
consequence: meaningful
sensitivity: private
created_at: 2026-08-22T15:07:45Z
updated_at: 2026-08-22T15:13:15Z
next_action: Monitor: confirm the $50,000 receivable lands ~2026-08-30 and rent clears ~2026-09-01 as predicted. Revisit only if the receivable amount/timing, rent amount, or cash position changes materially before then.






---
## Intent

Evaluate whether to hold off (delay) the rent payment due 2026-09-01, given
current cash of $100,000, an expected $50,000 receivable on 2026-08-30, and
rent of $30,000. This is the studio's first real business decision run through
`business-manage-liquidity-and-cash-runway`, opened specifically to give the
graph/loop tracer (WO 2026-08-22-026) a genuine business edge to attach.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] Real cash-timing inputs gathered (no fabricated figures)
- [x] Base and downside receivable-timing scenarios computed
- [x] Recommendation reached with authority boundary stated
- [x] Real business edge exists and traces (the `responds_to` edge to WO 2026-08-22-026, written 2026-08-22T15:07:56Z, now backed by this Decision 1 — no separate edge needed)


## Constraints and non-goals

**Constraints:**
- None currently — the initial "can't delay payment" constraint was director-confirmed wrong and dropped during grilling.

**Non-goals:**
- Not a full 12-month runway certification — only the 08-30/09-01 event window is analyzed; the rest of the horizon has no inflow/obligation visibility yet.
- No payment, financing, or external communication action taken or authorized — analysis only.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Pay rent on schedule; no liquidity justification for holding off

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | The 2026-09-01 rent payment ($30,000), evaluated against 2026-08-30 receivable timing ($50,000) and current cash ($100,000). |
| **Authorization** | Director-supplied real financial inputs; analysis-only, no payment action executed or authorized. |
| **Confidence** | high (basis: [testimony] all three figures director-confirmed; even the downside scenario — receivable late — leaves $70,000 after rent, a wide margin, not a marginal call). |
| **Actor** | business-manage-liquidity-and-cash-runway |
| **Revisit trigger** | If the receivable amount, rent amount, or due dates change; if a new near-term obligation appears before rent clears; or if cash position drops materially before 2026-09-01. |
| **Rationale** | Base case: $150,000 available before rent, $120,000 after. Downside case (receivable slips past due date): $100,000 available, $70,000 after. Both scenarios clear rent with comfortable margin — holding off would add landlord/relationship risk for no cash-timing benefit. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [decision] | Director request, business-manage-liquidity-and-cash-runway skill activation | Opened per director request to give business-manage-liquidity-and-cash-runway a real decision Work Object. Closes the gap identified in WO 2026-08-22-026 Decision 1: the first business typed edge (via ws relation add) had no real business decision to attach to. This object is the real decision, not a demo. |
| [testimony] | director, direct chat input | Director-supplied real inputs. Currency/horizon: USD, 12 months. Current cash position: $100,000. Dated obligation: rent due 2026-09-01 (amount not specified -- gap). Expected inflow: $50,000 receivable expected 2026-08-30. Constraint: cannot delay payment (referent unspecified -- likely the rent obligation, not confirmed). Decision to evaluate: 'should we hold off' (referent of 'hold off' not specified -- gap). |
| [testimony] | director, direct chat input | Rent amount: $30,000, due 2026-09-01. Constraint 'can't delay payment' was director-confirmed WRONG and dropped -- rent CAN be delayed if needed; the decision under evaluation is exactly whether to. Decision referent resolved: 'should we hold off' = hold off the rent payment. |
| [inference] | arithmetic over the three director-supplied figures (cash, receivable, rent) | Base/downside scenario computation: Base (receivable lands 08-30 on time) = $100,000 + $50,000 = $150,000 before rent; after $30,000 rent = $120,000 remaining. Downside (receivable slips past 08-30) = $100,000 before rent; after $30,000 rent = $70,000 remaining. Both scenarios clear rent with wide margin -- no liquidity gap in either case. This is a computed inference from the three testimony figures, not a separately confirmed fact. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

The `responds_to` edge to WO 2026-08-22-026 (written before this decision
existed) now originates from a Work Object carrying a real accepted decision
— no additional edge needs to be manufactured. Return to WO 2026-08-22-026
and mark its deferred exit-criteria item ("one real business edge... is
written and traced") as met, citing this object and Decision 1 as the
evidence. Monitor: confirm the 2026-08-30 receivable and 2026-09-01 rent
payment land as expected; revisit only if the revisit trigger fires.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T15:07:45Z — Started via ws start (created + evidence + explore + activate supporting)

- **State:** explore
- **Status:** active
- **Actor:** governance-conduct-work-object
- **Rationale:** Financial records default to private sensitivity per the skill's own consequence/authority rules. Consequence set to meaningful per director choice (not an active/near-term crisis).
### 2026-08-22T15:12:29Z — Decision 1 reached: pay rent on schedule, no liquidity justification for holding off. Base scenario leaves $120,000 after rent, downside (receivable late) leaves $70,000 -- both clear comfortably. Constraint 'can't delay payment' was surfaced as contradicting the decision framing, director confirmed it was wrong and it was dropped.

- **State:** observe
- **Status:** active
- **Actor:** business-manage-liquidity-and-cash-runway
- **Rationale:** Analysis-only decision reached with real inputs; no build/verify/release work applies. Moving to observe to monitor whether the 08-30 receivable and 09-01 rent payment land as predicted.
## Relationships

  REL-2026_08_22_029-001:
    type: responds_to
    from: wo:2026-08-22-029
    to: wo:2026-08-22-026
    basis: "Opened to satisfy WO 2026-08-22-026 Decision 1's deferred business-edge exit criterion"
    created_at: 2026-08-22T15:07:56Z
