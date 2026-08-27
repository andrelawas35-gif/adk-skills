---
name: business-balance-demand-supply-capacity
default_tier: high
description: "Use when demand, supply, capacity, inventory, constraints, and exception actions must become a feasible operating plan; never issues schedules, purchase orders, customer promises, staffing changes, or live-system writes without scoped authority."
---
# Balance Demand, Supply, and Capacity

## Governing principle

A feasible plan is a negotiated constraint model, not a demand wish. Keep
demand confidence, supply availability, capacity, inventory, bottlenecks,
service commitments, exceptions, and authority boundaries visible before work
is scheduled or promised.

## Boundaries and non-goals

This skill does:

- Reconcile demand signals, supply availability, capacity, inventory, backlog,
  constraints, and exception rules into a feasible operating-plan recommendation.
- Expose bottlenecks, scenario options, guardrails, escalation paths, and
  revisit cadence.
- Route commercial, supplier, workforce, process, delivery, cash, or risk gaps.

This skill does not:

- Issue production schedules, purchase orders, customer promises, ERP/MRP/CRM
  changes, staffing changes, or inventory moves.
- Redesign the recurring process, select suppliers, qualify opportunities, or
  approve money movement.
- Treat forecast demand as committed demand or nominal capacity as usable capacity.

## Inputs and preconditions

Use an activated Work Object with planning horizon, demand signal, supply
availability, capacity basis, inventory/service policy, backlog, constraints,
owner, exception rules, and the operating decision that must be made now.

## Required capabilities

- `file_read` and `content_search` — inspect permitted demand, supply,
  inventory, capacity, backlog, process, supplier, and customer evidence.
- `terminal_run` — run reproducible local capacity or scenario checks when useful.
- `file_write` — return a compact operating-plan recommendation through the
  conductor.
- `user_confirmation` — authorize schedules, purchase orders, staffing changes,
  customer promises, inventory actions, or live-system writes.
- `structured_output` — report feasibility, constraints, scenarios, and route.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Read-only feasibility analysis within the approved evidence boundary is allowed.
- Production schedules, purchase orders, inventory moves, customer delivery
  promises, supplier commitments, staffing changes, and live ERP/MRP/CRM writes
  require explicit scoped authority.
- Customer, supplier, workforce, inventory, and operational data may be private;
  store only minimum necessary summaries.
- For a high-consequence Work Object, confirmation must name the exact proposed
  mutation. Do not stage, annotate, change status, append History, or make any
  other mutation before receiving that scoped confirmation.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when demand
confidence, nominal capacity, supplier lead time, inventory policy, or an
exception action could reverse the feasible plan.

## Skill Grilling Profile

Apply the `business-balance-demand-supply-capacity` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge demand-as-commitment, nominal
capacity, hidden bottlenecks, supplier optimism, inventory blindness, and
unapproved customer promises.

## Business operating pipeline

Use `references/BUSINESS-OPERATING-PIPELINE.md` to distinguish this skill's
demand/supply/capacity feasibility frontier from the Work Object lifecycle and
the commercial pipeline. Route forward or back only when the evidence exposes a
different owning business frontier.

## Stage workflow

1. Define horizon, owner, service objective, planning boundary, demand signal,
   supply/capacity boundary, and excluded execution actions.
2. Inspect demand confidence, backlog, available capacity, supplier/material
   constraints, inventory policy, lead times, bottlenecks, quality limits, and
   cash or risk constraints.
3. Build feasible base/downside/upside options and identify the binding
   constraint. Separate committed demand from forecast, and nominal capacity
   from usable capacity.
4. Compare fulfill, level-load, prioritize, defer, source, add capacity, reduce
   scope, or escalate options with guardrails and exception rules.
5. Recommend an operating-plan choice with evidence gaps, owner, authority
   needs, revisit cadence, and downstream routes.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`.
- A forecast is not committed demand; a capacity number is not usable capacity
  without constraint, availability, and quality evidence.
- A feasible-plan recommendation is not a production schedule or customer promise.

## Work Object updates

Return the planning boundary, demand and supply evidence, capacity model,
constraint, scenarios, recommended plan, exceptions, authority needs, routes,
and revisit trigger to `conduct-work-object`.

## Routing and termination

- Demand/source uncertainty -> `business-manage-market-intelligence`,
  `business-manage-commercial-pipeline`, or `business-manage-customer-success`.
- Supplier constraint -> `business-source-and-govern-suppliers`.
- Workforce constraint -> `business-plan-workforce-accountability`.
- Process bottleneck -> `business-improve-operating-process`.
- Delivery commitment -> `business-direct-project-delivery`.
- Cash/inventory consequence -> `business-manage-liquidity-and-cash-runway`.
- Schedule, purchase, inventory, staffing, customer promise, or live-system
  action -> conductor for scoped authority.

## Output template

```markdown
## Demand, supply, and capacity decision
- **Scope:** <horizon, owner, service objective, boundary>
- **Evidence:** <demand, supply, capacity, backlog, inventory, constraints>
- **Scenarios and constraint:** <base, downside, upside and bottleneck>
- **Plan:** <fulfill | level-load | prioritize | defer | source | add capacity | reduce scope | escalate>
- **Exceptions and gaps:** <authority boundary, weak evidence, guardrails>
- **Authority and route:** <analysis only or exact gated action>
```

## Final self-check

- Are forecast demand, committed demand, nominal capacity, and usable capacity separate?
- Is the binding constraint and exception rule explicit?
- Is every schedule, purchase, promise, staffing change, inventory move, or system write gated?
