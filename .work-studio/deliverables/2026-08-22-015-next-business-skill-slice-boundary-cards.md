# Next Business-Skill Slice Boundary Cards

**Work Object:** `2026-08-22-015`  
**Source report:** `.work-studio/deliverables/2026-08-22-008-comprehensive-business-skill-portfolio.md`  
**Slice:** four Wave 1 candidates after the completed seven-skill tranche and
the business operating pipeline.

## Slice recommendation

Design, but do not yet implement, these four skills:

1. `business-govern-initiative-portfolio`
2. `business-design-pricing-and-packaging`
3. `business-manage-liquidity-and-cash-runway`
4. `business-balance-demand-supply-capacity`

## Why this slice

The first tranche gave Work Studio strategic choice, market evidence,
driver-based planning, enterprise risk, supplier governance, project delivery,
and customer success. The operating pipeline then gave those skills a shared
routing spine. This next slice fills the highest-leverage control gaps before
adding quality, organizational change, data governance, and continuity:

- portfolio governance decides which initiatives deserve scarce attention;
- pricing/packaging converts market and value assumptions into an offer shape;
- liquidity/runway protects survival when accounting profit hides cash timing;
- demand/supply/capacity turns commercial demand into feasible operating plans.

## Boundary Card 1: `business-govern-initiative-portfolio`

**Trigger:** Multiple initiatives, projects, or change bets compete for funding,
capacity, sequence, pause/stop, or executive attention.

**Governing question:** Which initiatives should start, continue, pause, stop,
or be resequenced given strategy, capacity, dependencies, risk, expected
benefit, and current evidence?

**Minimum evidence:**

- strategic objectives and non-goals;
- list of candidate initiatives with owner, intended outcome, status, cost,
  capacity demand, dependency, risk, and expected benefit;
- current commitments and hard constraints;
- evidence quality for benefit, urgency, reversibility, and downside.

**Output:** Portfolio decision record with initiative disposition, sequence,
capacity/risk implications, rejected alternatives, authority needs, and review
trigger.

**Non-goals:**

- Does not create strategy; routes strategic uncertainty to
  `business-formulate-strategy`.
- Does not run project delivery; routes accepted bounded initiatives to
  `business-direct-project-delivery`.
- Does not approve spend, staffing, customer/vendor promises, or cancellation
  communications.

**Authority gates:** Funding, cancellation, staffing/resource reallocation,
public/executive commitments, customer/vendor impact, and materially changing
an accepted Work Object route require scoped authority.

**Routes:**

- strategic fit gap -> `business-formulate-strategy`;
- market-demand gap -> `business-manage-market-intelligence`;
- money consequence -> `business-assess-financial-decision` or
  `business-build-driver-based-plan-and-forecast`;
- capacity consequence -> `business-plan-workforce-accountability`;
- delivery control -> `business-direct-project-delivery`;
- risk conflict -> `business-manage-enterprise-risk`.

**Overlap tests:**

- If the decision is one initiative's scope/schedule/change control, use
  `business-direct-project-delivery`.
- If the decision is one reversible implementation path, use
  `alawas-engineering-implement-bounded-change`.
- If the decision is a whole portfolio allocation or stop/start sequence, this
  skill owns it.

## Boundary Card 2: `business-design-pricing-and-packaging`

**Trigger:** A business must choose value metric, package structure,
price/range, discount fences, offer terms, or a pricing test before selling,
publishing, quoting, or forecasting.

**Governing question:** What pricing and packaging choice best matches customer
value, market evidence, economics, fairness, operational feasibility, and the
business's strategy?

**Minimum evidence:**

- target segment, use case, value driver, willingness-to-pay evidence or gap;
- competitor/substitute price references with dates and source quality;
- cost, margin, service burden, and cash-timing assumptions;
- package boundaries, included/excluded features, discount rules, and test
  constraints.

**Output:** Pricing/packaging recommendation with value metric, package
structure, price/range or test range, discount fences, assumptions, authority
needs, and review trigger.

**Non-goals:**

- Does not publish prices, grant discounts, quote customers, or change a live
  commerce/CRM system.
- Does not replace financial viability analysis; routes economics to
  `business-assess-financial-decision`.
- Does not substantiate public marketing claims by itself; routes claims to
  market intelligence, legal/compliance, or owner review.

**Authority gates:** Published prices, discount promises, customer quotes,
regulated-market claims, discriminatory or protected-class-sensitive pricing,
and live-system changes require scoped authority.

**Routes:**

- market evidence gap -> `business-manage-market-intelligence`;
- commercial opportunity -> `business-manage-commercial-pipeline`;
- financial viability -> `business-assess-financial-decision`;
- forecast baseline effect -> `business-build-driver-based-plan-and-forecast`;
- delivery/service burden -> `business-direct-project-delivery` or
  `business-improve-operating-process`.

**Overlap tests:**

- If the decision is whether one deal is worth taking, use
  `business-manage-commercial-pipeline` plus financial assessment.
- If the decision is the offer's reusable value metric, package, price, or
  discount rule, this skill owns it.

## Boundary Card 3: `business-manage-liquidity-and-cash-runway`

**Trigger:** The business needs to know whether cash obligations can be met,
when cash runs short, which levers buy runway, or when escalation/financing is
needed.

**Governing question:** Can the business meet obligations when due under base
and downside timing assumptions, and what bounded action or escalation is
needed before a cash constraint becomes harm?

**Minimum evidence:**

- current cash position and near-term cash availability;
- known payables, receivables, payroll, debt, tax, inventory, rent, and other
  obligations by date;
- committed inflows and evidence quality;
- base/downside/upside cash-timing assumptions;
- covenant, insolvency, legal, tax, or financing constraints when known.

**Output:** Cash runway and liquidity decision record with timing gaps, runway
date/range, highest-leverage variables, escalation triggers, safe options, and
authority boundaries.

**Non-goals:**

- Does not move money, borrow, invest, pay, collect, file taxes, or give legal,
  accounting, insolvency, or investment advice.
- Does not replace the integrated planning baseline; routes baseline modeling
  to `business-build-driver-based-plan-and-forecast`.
- Does not hide cash timing inside profit or revenue.

**Authority gates:** Payments, transfers, borrowing, investment, collections,
credit decisions, covenant/insolvency matters, and external creditor/customer
communications require scoped authority and qualified review when appropriate.

**Routes:**

- one bounded economics choice -> `business-assess-financial-decision`;
- integrated baseline -> `business-build-driver-based-plan-and-forecast`;
- supplier/payment consequence -> `business-source-and-govern-suppliers`;
- workforce/payroll consequence -> `business-plan-workforce-accountability`;
- risk threshold -> `business-manage-enterprise-risk`.

**Overlap tests:**

- If the question is "is this one choice financially attractive?", use
  `business-assess-financial-decision`.
- If the question is "can we meet obligations on time under scenarios?", this
  skill owns it.

## Boundary Card 4: `business-balance-demand-supply-capacity`

**Trigger:** Forecast demand, available capacity, supply constraints, inventory,
staffing, supplier lead times, or service commitments must be reconciled into a
feasible operating plan.

**Governing question:** What demand/supply/capacity plan is feasible, evidence
backed, and safe under uncertainty, and which exceptions need escalation?

**Minimum evidence:**

- demand forecast or opportunity/customer-success signal with confidence;
- available capacity by role, asset, supplier, material, or process constraint;
- inventory/service-level policy and known constraints;
- lead times, bottlenecks, backlog, quality limits, and risk signals;
- exception rules and authority boundary for schedule, purchasing, inventory,
  and customer promises.

**Output:** Feasible operating-plan recommendation with capacity constraint,
scenario plan, exception decisions, escalations, guardrails, and revisit
cadence.

**Non-goals:**

- Does not issue production schedules, purchase orders, customer promises, ERP
  changes, or staffing changes without scoped authority.
- Does not redesign recurring process flow; routes process experiments to
  `business-improve-operating-process`.
- Does not own supplier selection or commercial opportunity qualification.

**Authority gates:** Production scheduling, inventory moves, purchase orders,
customer delivery promises, supplier commitments, staffing changes, and live
ERP/MRP/CRM writes require scoped authority.

**Routes:**

- demand/source uncertainty -> `business-manage-market-intelligence`,
  `business-manage-commercial-pipeline`, or `business-manage-customer-success`;
- supplier constraint -> `business-source-and-govern-suppliers`;
- workforce constraint -> `business-plan-workforce-accountability`;
- process bottleneck -> `business-improve-operating-process`;
- delivery commitment -> `business-direct-project-delivery`;
- cash/inventory consequence -> `business-manage-liquidity-and-cash-runway`.

**Overlap tests:**

- If the decision is supplier qualification, use
  `business-source-and-govern-suppliers`.
- If the decision is recurring flow improvement, use
  `business-improve-operating-process`.
- If the decision is cross-constraint feasibility across demand, supply,
  capacity, and exceptions, this skill owns it.

## Slice-level pairwise checks

- The slice does not replace the Work Object lifecycle; all durable state,
  evidence, transitions, and authority records still route through
  `alawas-governance-conduct-work-object`.
- The slice does not replace the commercial pipeline; commercial opportunity
  stage movement remains with `business-manage-commercial-pipeline`.
- The slice extends the business operating pipeline by adding missing route
  owners for portfolio allocation, pricing, liquidity, and demand/supply
  feasibility.
- Quality/CAPA, organizational change, data governance, and continuity remain
  deferred unless an overlap test proves they block implementation.

## Recommended implementation boundary

If accepted, implement only these four skill contracts, their Skill-Aware
Grilling profiles, fixture/test coverage, component-ledger entries, runtime
governance-domain mapping, generated skill map, and generated Codex, Claude
Code, and GitHub Copilot adapters.

Do not globally install, deploy, contact external parties, mutate live business
systems, move money, alter personnel/supplier/customer records, or implement
the remaining Wave 1 skills without separate authority.
