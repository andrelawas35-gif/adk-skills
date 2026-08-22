# Business Operating Pipeline

## Purpose

The business operating pipeline is the canonical routing spine for business-domain
questions in Work Studio. It does not replace the Work Object lifecycle. A Work
Object still governs durable state, authority, evidence, and resumption; this
pipeline decides which business skill owns the next business question.

## Pipeline distinction

| Pipeline | Owns | Does not own |
|----------|------|--------------|
| Work Object lifecycle | Work state: notice, explore, design, build, verify, release, observe, close. | Business-domain judgment by itself. |
| Commercial pipeline | Sales opportunity qualification, stage movement, forecast, and close decisions. | Strategy, finance approval, delivery planning, or customer-success outcomes. |
| Business operating pipeline | Cross-business routing from strategy through market, demand, money, capacity, suppliers, operations, delivery, customers, risk, and review. | Lifecycle state transitions, live-system mutation, or external commitments. |

## Canonical route

Use this order as a default route map, not a mandatory sequence. Enter at the
first skill that owns the current decision frontier, then route to the next
skill only when the evidence exposes that downstream question.

```text
business-formulate-strategy
→ business-govern-initiative-portfolio
→ business-manage-market-intelligence
→ business-design-pricing-and-packaging
→ business-manage-commercial-pipeline
→ business-assess-financial-decision
→ business-build-driver-based-plan-and-forecast
→ business-manage-liquidity-and-cash-runway
→ business-plan-workforce-accountability
→ business-source-and-govern-suppliers
→ business-balance-demand-supply-capacity
→ business-improve-operating-process
→ business-direct-project-delivery
→ business-manage-customer-success
→ business-manage-enterprise-risk
→ alawas-governance-govern-scorecards
→ alawas-governance-review-outcome-and-adapt
→ business-formulate-strategy when the evidence changes the strategic choice set
```

## Ownership map

| Business frontier | Owning skill |
|-------------------|--------------|
| Objective, arena, advantage, non-goals, assumptions, strategic review trigger | `business-formulate-strategy` |
| Initiative start, continue, pause, stop, defer, resequence, and portfolio attention/capacity allocation | `business-govern-initiative-portfolio` |
| Market boundary, demand signals, competitors, substitutes, uncertainty, refresh cadence | `business-manage-market-intelligence` |
| Value metric, package boundary, price/range, discount fence, offer terms, and pricing test | `business-design-pricing-and-packaging` |
| Sales opportunity qualification, stage exit, forecast, close decision | `business-manage-commercial-pipeline` |
| One bounded cash, cost, break-even, return, or scenario decision | `business-assess-financial-decision` |
| Integrated driver-based profit, cash, and balance-sheet planning baseline | `business-build-driver-based-plan-and-forecast` |
| Cash timing, obligations, runway, liquidity gap, and escalation options | `business-manage-liquidity-and-cash-runway` |
| Roles, capacity, skills, ownership, and workforce-accountability gaps | `business-plan-workforce-accountability` |
| Make/buy, sourcing strategy, supplier selection, governance, performance response | `business-source-and-govern-suppliers` |
| Demand/supply/capacity feasibility, inventory, bottlenecks, and operating-plan exceptions | `business-balance-demand-supply-capacity` |
| Recurring work map, constraint, process experiment, safeguards, operating measure | `business-improve-operating-process` |
| Bounded initiative scope, schedule, dependency, change-control, recovery, escalation | `business-direct-project-delivery` |
| Post-sale onboarding, adoption, realized outcomes, health, renewal risk, intervention priority | `business-manage-customer-success` |
| Risk appetite, tolerance, treatment, ownership, monitoring, residual exposure | `business-manage-enterprise-risk` |
| Outcome scorecard, review evidence, proposal candidate, learning loop | `alawas-governance-govern-scorecards` and `alawas-governance-review-outcome-and-adapt` |

## Handoff rules

1. Stay inside the same Work Object when the next business question is part of
   the same bounded decision and does not need separate ownership, acceptance
   evidence, or authority.
2. Create a linked Work Object when the next question has a different owner,
   consequence, sensitivity, material acceptance criteria, or implementation
   path.
3. Route to the conductor for any lifecycle transition, History entry, Evidence
   ledger entry, successor Work Object, authority record, or external-effect
   boundary.
4. Treat pricing, legal, tax, accounting, regulated claims, public commitments,
   customer contact, supplier contact, CRM edits, money movement, personnel
   actions, and live-system mutation as gated actions requiring scoped
   authority and often a specialist outside this pipeline.
5. Do not let a later-stage skill silently settle an earlier-stage assumption.
   If downstream evidence contradicts strategy, market, demand, money, capacity,
   supplier, process, delivery, customer, or risk assumptions, route back to the
   owning skill and preserve the contradiction.

## Minimum handoff record

Every business-to-business-skill handoff should name:

- current Work Object ID and lifecycle state;
- current business frontier and owning skill;
- evidence that made the current frontier sufficiently answered;
- open assumption or gap that belongs to the next skill;
- whether the next question stays in the same Work Object or needs a linked
  successor;
- exact authority boundary if the next move would touch external people,
  money, personnel, suppliers, customers, public claims, or live systems.

## Revisit triggers

Revisit this pipeline when:

- real Work Object use shows recurring route ambiguity;
- a missing business domain such as pricing, quality, continuity, portfolio
  governance, data governance, or change management becomes a repeated handoff
  gap;
- the runtime needs deterministic routing rather than reference guidance;
- evidence shows the canonical order causes premature downstream work or hides
  upstream uncertainty.
