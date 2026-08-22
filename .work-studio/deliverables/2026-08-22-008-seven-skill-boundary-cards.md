# Seven-Skill Business Boundary Cards

**Work Object:** `2026-08-22-008`
**Design status:** accepted boundary-card tracer
**Scope:** first design tranche for seven proposed business-management skills

## Purpose

These cards test whether the accepted first tranche has clean ownership before
full `SKILL.md` implementation. Each card defines one recurring management
decision, its evidence boundary, output, authority gates, routes, and overlap
tests against the four installed business skills:

- `business-manage-commercial-pipeline`
- `business-assess-financial-decision`
- `business-plan-workforce-accountability`
- `business-improve-operating-process`

## Shared implementation constraints

- The conductor owns Work Object lifecycle writes.
- Each business skill owns one domain decision record, not execution.
- External communications, money movement, personnel actions, contracts,
  supplier/customer commitments, live-system writes, and regulated claims remain
  explicitly gated.
- Private business data is summarized minimally in Work Objects; restricted
  material is never stored there.
- If an overlap test fails, stop before implementation and route back to
  `alawas-thinking-pressure-test-decision`.

## Boundary Card 1: `business-formulate-strategy`

**Trigger:** A Work Object needs coherent strategic choices before portfolio,
market, product, financial, or operating decisions can be evaluated.

**Governing question:** What strategic objective, arena, advantage thesis,
non-goals, assumptions, and review trigger should govern downstream work?

**Minimum evidence:** Current purpose, goal horizon, relevant constraints,
stakeholders, alternatives, assumptions, existing commitments, and evidence for
why the choice matters now.

**Output:** Strategy choice record with objective, arena, advantage thesis,
explicit non-goals, assumptions, downstream routes, confidence, owner, and
revisit trigger.

**Non-goals:** Does not allocate initiatives, approve spend, set pricing, create
marketing claims, redesign operations, or make public commitments.

**Authority gates:** Owner/board approval, public commitments, material
reallocation, regulated claims, and external communications.

**Routes:** Market evidence gap -> `business-manage-market-intelligence`;
money consequence -> `business-assess-financial-decision`; capacity consequence
-> `business-plan-workforce-accountability`; execution portfolio -> future
`business-govern-initiative-portfolio` or conductor.

**Overlap tests:**

- Pipeline: If the question is about one named opportunity, route to pipeline;
  strategy owns the choice set that defines which opportunities matter.
- Finance: If the question is whether a chosen option is affordable or has a
  return profile, route to finance; strategy owns the strategic thesis before
  modeling.
- Workforce: If the question is role coverage or capacity, route to workforce;
  strategy owns what work should matter.
- Process: If the question is current/future operational flow, route to process;
  strategy owns the direction that makes process changes relevant.

## Boundary Card 2: `business-manage-market-intelligence`

**Trigger:** A Work Object needs market, demand, competitor, substitute, or
signal evidence before a business recommendation can stand.

**Governing question:** What market boundary, demand signal, competitor or
substitute evidence, uncertainty, and refresh cadence should inform the current
decision?

**Minimum evidence:** Market definition, target segment, known sources, demand
signals, competitor/substitute list, source dates, source reliability,
confidence, and decision the evidence will influence.

**Output:** Market-intelligence brief with boundary, signals, confidence,
contradictions, refresh trigger, and downstream recommendation impact.

**Non-goals:** Does not qualify sales opportunities, contact prospects, set
strategy alone, create marketing claims, scrape restricted data, or buy data.

**Authority gates:** Paid/licensed data, scraping, competitor or customer
contact, personal data, publication, and claims based on market evidence.

**Routes:** Named opportunity -> `business-manage-commercial-pipeline`;
strategic implication -> `business-formulate-strategy`; pricing implication ->
future pricing skill; financial effect -> `business-assess-financial-decision`.

**Overlap tests:**

- Pipeline: If evidence concerns one buyer's intent, authority, timing, or next
  commitment, route to pipeline; market intelligence owns aggregate or external
  market evidence.
- Finance: If the issue is contribution, break-even, cash, or downside, route
  to finance; market intelligence owns the market assumptions feeding the model.
- Workforce: If evidence changes staffing or capability needs, route to
  workforce after market boundaries are explicit.
- Process: If evidence concerns how work currently flows, route to process;
  market intelligence owns outside-in demand and competitive signals.

## Boundary Card 3: `business-build-driver-based-plan-and-forecast`

**Trigger:** A Work Object needs an integrated business baseline that connects
operating drivers to profit, cash, and balance-sheet implications.

**Governing question:** Which drivers, scenarios, assumptions, and refresh rules
should form the planning baseline for future business decisions?

**Minimum evidence:** Planning horizon, currency, driver definitions, source
records, current operating baseline, assumptions, scenario ranges, constraints,
and decision owner.

**Output:** Driver-based plan with baseline, assumptions, scenario ranges,
driver sensitivity, evidence gaps, refresh cadence, and routeable consequences.

**Non-goals:** Does not move money, approve budget, file accounts, replace
accounting advice, or decide one bounded investment by itself.

**Authority gates:** Private financial data, budget commitments, accounting or
tax claims, financing actions, and publication of forecasts.

**Routes:** One bounded money decision -> `business-assess-financial-decision`;
cash shortfall control -> future liquidity skill; capacity driver -> workforce;
process-cost driver -> process improvement.

**Overlap tests:**

- Pipeline: If the driver is unsupported revenue from named opportunities,
  route to pipeline for buying evidence; planning owns the baseline once
  evidence is classified.
- Finance: If the question is proceed/revise/defer/stop for one choice, route
  to finance; planning owns the reusable baseline.
- Workforce: If the forecast depends on role coverage, route to workforce for
  capacity evidence; planning owns integrated driver effects.
- Process: If process timing/cost assumptions are weak, route to process;
  planning owns the scenario model, not current-state mapping.

## Boundary Card 4: `business-manage-enterprise-risk`

**Trigger:** A Work Object needs risk appetite, tolerance, treatment, ownership,
or residual exposure across more than one decision or function.

**Governing question:** What risk should be accepted, reduced, transferred,
avoided, or monitored, by whom, and with what residual exposure?

**Minimum evidence:** Risk statement, cause, consequence, affected objectives,
current controls, likelihood/effect basis, appetite or tolerance, owner,
treatment options, residual risk, and review trigger.

**Output:** Risk decision record with treatment recommendation, owner,
residual exposure, authority boundary, monitoring evidence, and revisit trigger.

**Non-goals:** Does not provide legal, actuarial, safety, insurance, audit, or
compliance opinions; does not accept risk on behalf of accountable humans.

**Authority gates:** Risk acceptance, safety/privacy/security/money exposure,
insurance or contractual transfer, regulated matters, and public risk claims.

**Routes:** Active harm -> `operations-diagnose-production-incident`; control
design -> future controls/compliance skill; money consequence -> finance; role
ownership -> workforce.

**Overlap tests:**

- Pipeline: If the risk is limited to one opportunity's close/forecast action,
  route to pipeline; enterprise risk owns cross-objective exposure.
- Finance: If the main question is cash, cost, or return under scenarios, route
  to finance; risk owns appetite, treatment, and residual exposure.
- Workforce: If ownership or role capacity is the issue, route to workforce;
  risk owns the exposure decision and treatment boundary.
- Process: If a recurring flow creates the risk, route to process for the
  experiment; risk owns whether the residual exposure is acceptable.

## Boundary Card 5: `business-source-and-govern-suppliers`

**Trigger:** A Work Object needs make/buy, sourcing strategy, supplier
selection, supplier governance, or supplier performance response.

**Governing question:** Which supplier or sourcing path should be recommended,
under what evidence, relationship model, performance expectations, and
authority boundary?

**Minimum evidence:** Need, make/buy alternatives, selection criteria,
candidate sources, cost/service/risk evidence, constraints, supplier data
permission, relationship model, and accountable owner.

**Output:** Supplier decision record with sourcing recommendation, rationale,
risks, relationship model, performance evidence, authority gates, and revisit
trigger.

**Non-goals:** Does not issue RFPs, contact suppliers, negotiate, award,
purchase, sign contracts, or perform legal/sanctions determinations.

**Authority gates:** Supplier contact, RFPs, negotiation, awards, purchase
orders, contracts, sanctions/compliance checks, shared data, and spend.

**Routes:** Spend viability -> finance; supplier-process integration -> process;
role ownership -> workforce; contractual/legal question -> gated human review.

**Overlap tests:**

- Pipeline: If the external party is a buyer opportunity, route to pipeline;
  supplier governance owns sell-side mirror decisions only when Work Studio is
  the buyer or partner of supply.
- Finance: If comparing total cost or cash effect is decisive, route to finance;
  sourcing owns qualification, governance, and supplier relationship evidence.
- Workforce: If the alternative is hiring or internal capacity, route to
  workforce for role evidence; sourcing owns make/buy and supplier path.
- Process: If supplier work changes operational flow, route to process;
  sourcing owns supplier selection and governance.

## Boundary Card 6: `business-direct-project-delivery`

**Trigger:** A Work Object needs delivery approach, scope/schedule/dependency
baseline, change control, or continue/recover/escalate decision for a bounded
business initiative.

**Governing question:** What delivery baseline and control decision should
govern this initiative now, and what evidence decides continue, recover,
escalate, or stop?

**Minimum evidence:** Objective, scope boundary, owner, dependencies, schedule,
delivery approach, constraints, risks, current status, change requests, and
acceptance or recovery criteria.

**Output:** Project-delivery decision record with baseline, dependencies,
change-control rule, delivery risks, recovery option, owner, and revisit trigger.

**Non-goals:** Does not implement code, allocate an initiative portfolio, approve
budget, change contracts, promise customer delivery, or manage people actions.

**Authority gates:** Baseline changes, resource commitments, vendor/customer
communications, contractual dates, spend, and live-system changes.

**Routes:** Code or repo implementation -> `engineering-implement-bounded-change`;
money consequence -> finance; role/capacity consequence -> workforce; recurring
flow redesign -> process.

**Overlap tests:**

- Pipeline: If the issue is a customer's buying progress or promise terms,
  route to pipeline; project delivery owns internal initiative control.
- Finance: If the issue is whether the initiative is worth funding, route to
  finance; project delivery owns delivery control once intent exists.
- Workforce: If delivery depends on role capacity, route to workforce; project
  delivery owns baseline, dependency, and recovery decisions.
- Process: If the initiative is a recurring process experiment, route to
  process for the future-state test; project delivery owns initiative control.

## Boundary Card 7: `business-manage-customer-success`

**Trigger:** A Work Object needs post-sale onboarding, adoption, realized
outcome, health, renewal risk, or intervention prioritization.

**Governing question:** What customer outcome evidence, adoption state, health
risk, and intervention should govern the post-sale relationship?

**Minimum evidence:** Customer/account identifier, sold outcome, onboarding
state, usage/adoption evidence, realized outcome evidence, health signals,
renewal/expansion risk, obligations, private-data boundary, and owner.

**Output:** Customer-success decision record with health basis, outcome gaps,
intervention recommendation, authority gates, customer-impact risks, and revisit
trigger.

**Non-goals:** Does not qualify new opportunities, promise concessions, contact
customers, edit CRM/CS tools, issue refunds, or decide product roadmap.

**Authority gates:** Customer contact, CRM/CS-tool writes, usage/private data,
concessions, refunds/credits, promised outcomes, renewal terms, and escalations.

**Routes:** New sale/expansion opportunity -> pipeline; concession economics ->
finance; delivery/process defect -> process; role/account coverage -> workforce.

**Overlap tests:**

- Pipeline: If the question is whether to close or forecast a buying decision,
  route to pipeline; customer success owns realized post-sale value and renewal
  risk.
- Finance: If the question is concession, refund, or margin effect, route to
  finance; customer success owns health evidence and intervention priority.
- Workforce: If account coverage or support capacity is the blocker, route to
  workforce; customer success owns customer outcome evidence.
- Process: If systemic onboarding/support flow is broken, route to process;
  customer success owns the account-level intervention decision.

## Exit Checklist

- [x] Seven accepted tranche candidates have boundary cards.
- [x] Every card includes trigger, governing question, minimum evidence, output,
      non-goals, authority gates, and routes.
- [x] Every card includes pairwise overlap tests against the four installed
      business skills.
- [x] Full skill implementation remains out of scope for this artifact.
- [x] A failed overlap test routes back to pressure-test-decision before
      implementation.
