# Skill-Aware Grilling

This catalogue supplies the stage-specific **Skill Grilling Profiles** used by
the conversational engine in `AGREEMENT-LOOP.md`. A profile determines what to
inspect, which tension to pursue next, how to challenge the emerging answer,
where to route it, and when its stage has enough understanding. It is not a
checklist and never replaces the one-question conversational turn contract.

## Skill Grilling Profiles

### `alawas-thinking-turn-signal-into-work`

**Gates** — (1) Provenance and sensitivity: confirm the signal's source and
whether using it crosses a privacy or data boundary before acting on it. (2)
Classification authority: confirm that classifying or activating the signal
does not silently authorize Work Object creation without the authority that
requires.

**Escalation** — Default: confirm the interpretation, check `active.md` and
existing Work Objects for overlap, classify as activation, incubation,
retention, or discard, and route classification to `alawas-governance-conduct-work-object`.
Information value overrides the default when evidence strongly indicates
duplicate work or an unresolved evidence gap — escalate directly to
`alawas-research-investigate-live-question` before classifying.

**Pressure scenario** — The signal is ambiguous between two established Work
Objects: would classifying it as new silently fork tracked work, and which
existing object's evidence would that duplicate?

### `alawas-governance-conduct-work-object`

**Gates** — (1) Consequence and authority: confirm whether the requested
mutation is attention, ownership, external consequence, or lifecycle
commitment, which requires explicit user approval, versus a routine update
inside existing authority. (2) Concurrency integrity: confirm `updated_at`
has not changed since read before writing, preventing a silent overwrite of
another actor's concurrent edit.

**Escalation** — Default: read existing Work Objects and decisions, express
one coherent testable outcome, recommend the next profile by consequence,
uncertainty, and stage, and apply routine updates under existing authority.
Information value overrides the default when evidence shows duplicate work by
outcome (not title) or an unowned decision — escalate to reconciling the
duplication or naming an owner before continuing.

**Pressure scenario** — Two Work Objects converge on the same outcome under
different titles: does completing one silently obsolete evidence in the
other, and who owns reconciling them?

### `alawas-thinking-pressure-test-decision`

**Gates** — (1) Decision authority: confirm who owns the decision and that
recording it does not exceed the Work Object's consequence-based authority.
(2) Irreversibility of the chosen branch: confirm the branch's reversibility
before recording it, since an irreversible branch chosen on weak evidence is
a harm-bearing outcome.

**Escalation** — Default: find the assumption carrying the most decision
risk, seek the strongest disconfirming evidence, recommend one branch, test
it against a counterexample, and record it with rationale and a revisit
trigger. Information value overrides the default when a cheap reversible
experiment would discriminate better than continued discussion — escalate to
`alawas-design-design-tracer-bullet` before recording a provisional decision.

**Pressure scenario** — The leading branch reverses easily today but becomes
irreversible after the next deploy: does that change which branch should be
recommended, and does the decision need to be made before or after that
deploy?

### `alawas-thinking-develop-idea`

**Gates** — (1) Explore-state validity: confirm the Work Object is in
`explore` state with `type: inquiry` before generating directions; generating
for a concrete or committed work object is a category error. (2) Creative
authority boundary: confirm that direction generation is explicitly
divergent — the agent generates, the user selects, and no direction is
presented as recommended over others.

**Escalation** — Default: discover project context, generate at least three
materially distinct directions with five-field structure (title, core idea,
distinctness claim, key assumption, smallest test), surface information
gaps, and present neutrally for user selection. Information value overrides
the default when the existing evidence ledger already discriminates between
potential directions — escalate to `alawas-research-investigate-live-question` for targeted
gap resolution rather than generating full directions that the evidence has
already narrowed.

**Pressure scenario** — The user says "explore this" but the Work Object's
evidence ledger already contains a clearly superior path: does the skill
still generate divergent directions, or does it route to convergence,
and what tells the agent which is appropriate?

### `alawas-thinking-diagnose-homogenization`

**Gates** — (1) Diagnosis-before-rewrite: confirm the homogenization claim is
grounded in the actual draft's missing evidence or flattening, not in style
labels. (2) Writer authority: confirm the writer decides which revision
direction is truer; the skill never declares prose authentic or "more human."

**Escalation** — Default: diagnose the specific missing material, demand
concrete evidence and lived detail, mark gaps rather than inventing them, and
present revision directions for the writer's choice. Information value
overrides the default when a homogenization claim is asserted without
draft-level evidence — escalate to grounding the claim in the exact passage
before proposing any rewrite.

**Pressure scenario** — The draft reads fluently and generically, but the
writer insists it is already their voice: does the skill still demand concrete
evidence of flattening before touching it, or defer to the writer's
self-assessment?

### `alawas-thinking-inquire-system`

**Gates** — (1) Studio grounding: confirm the answer is grounded in the
repository and active Work Objects, using the web only for background. (2)
Decision boundary: confirm the answer stops at the first decision, claim, or
judgment another skill owns.

**Escalation** — Default: read the repository and active Work Objects, ground
the answer in what exists, and stop at the first judgment another skill owns.
Information value overrides the default when the question points to a decision
or claim outside this skill's authority — escalate to routing to the owning
skill rather than answering.

**Pressure scenario** — An open question about how the studio works appears
answerable from memory, but the repository and active Work Objects disagree:
does the skill ground the answer in the repository, or answer from habit?

### `alawas-thinking-resume-work`

**Gates** — (1) Read-only: confirm the skill reads Work Objects only and never
writes anything. (2) Single-candidate handoff: confirm exactly one candidate
with state and next_action is handed back, and only the director routes it.

**Escalation** — Default: read Work Objects read-only, rank forward-motion work
by recency, and hand back exactly one candidate with its state and next_action.
Information value overrides the default when the most recent work is not the
most forward-moving — escalate to ranking by forward-motion evidence rather
than recency alone.

**Pressure scenario** — The most recent Work Object is stalled while an older
one has clear next-action momentum: does the skill hand back the older
forward-moving candidate, or default to recency?

### `alawas-design-design-tracer-bullet`

**Gates** — (1) External-effect and data boundary: confirm the design's
containment and access boundary before treating any exit evidence as safe to
observe. (2) Production execution authority: confirm that real-user or
durable-production execution is separately authorized beyond design
acceptance.

**Escalation** — Default: define observable exit evidence and the falsifying
result, choose the smallest end-to-end slice, and require containment, stop
conditions, and cleanup. Information value overrides the default when a
smaller discriminating experiment or investigation could resolve the
assumption more cheaply — escalate there instead of building the full tracer
bullet.

**Pressure scenario** — The smallest slice that produces informative failure
also touches sensitive data: is there a substitute that preserves
informativeness without the exposure, and what realism does it lose?

### `alawas-engineering-implement-bounded-change`

**Gates** — (1) Scope boundary: confirm the smallest viable change does not
cross an unapproved schema, public interface, dependency, deployment
configuration, data boundary, or external effect. (2) Unrelated dirty-work
preservation: confirm existing unrelated working-tree changes are protected
and never staged, committed, or altered.

**Escalation** — Default: reconcile the accepted boundary with current code,
establish a discriminating check, implement the smallest reversible path, and
run focused verification after each increment. Information value overrides
the default when a material new decision or authority boundary appears
mid-implementation — escalate by stopping and routing back to the conductor
for scoped confirmation rather than proceeding.

**Pressure scenario** — The bounded change verifies locally, but the working
tree also contains unrelated uncommitted work touching the same files: is the
diff actually separable for its own commit, or does isolating it require
hunk-level surgery?

### `alawas-engineering-verify-release-evidence`

**Gates** — (1) Recovery credibility: confirm a credible, reproducible
recovery path exists before treating a consequential change as ready; missing
recovery blocks readiness unless an accountable owner explicitly accepts the
irreversible risk. (2) Environment-specific behavior: confirm a local pass is
never treated as evidence of environment-specific behavior without direct
evidence from that environment.

**Escalation** — Default: test the weakest direct evidence for the most
consequential claim, require a reproducible check or explicitly authorized
human judgment, and classify every issue as blocker, accepted risk, or linked
follow-up. Information value overrides the default when the strongest
credible negative case surfaces a new failure mode — escalate to re-testing
that specific case before continuing the matrix.

**Pressure scenario** — All consequential claims pass locally, but the target
environment's data shape has never been exercised: does "ready" still hold,
or does this drop to "ready with accepted risk" pending an owner's explicit
sign-off?

### `alawas-operations-deploy-with-recovery`

**Gates** — (1) Rollback viability: confirm a rehearsed or directly evidenced
rollback mechanism and an available rollback owner exist before any increment
ships. (2) Affected scope: confirm which users or data are exposed by the
increment, sized to consequence and recoverability.

**Escalation** — Default: prove artifact equivalence, choose the smallest
observable increment, require success and failure signals with stop
conditions, and expand only after each window passes with positive evidence.
Information value overrides the default when a signal is ambiguous or ongoing
harm is possible — escalate immediately to holding, recovering, or routing to
incident response rather than expanding.

**Pressure scenario** — The observation window shows no alert, but there is
no instrumentation covering the affected path: is "no alert" actually
evidence of success here, or a false-negative gap that should hold the
rollout?

### `alawas-governance-review-outcome-and-adapt`

**Gates** — (1) Subgroup and unintended-effect harm: confirm aggregate
success does not hide subgroup harm or an unintended effect on an affected
group. (2) Closure consequence: confirm that consequential or uncertain
closure has explicit owner acceptance before the object closes.

**Escalation** — Default: compare expected versus observed reality with a
counterfactual and attribution strength, search for contrary evidence, and
route each mismatch to its earliest invalid assumption. Information value
overrides the default when a subgroup shows harm the aggregate doesn't —
escalate to naming that subgroup explicitly before closing as achieved.

**Pressure scenario** — The aggregate outcome looks achieved, but one
affected subgroup's data is thin: is "achieved" actually supported, or does
the object need to close with documented uncertainty for that subgroup?

### `alawas-research-investigate-live-question`

**Gates** — (1) Evidence-source authority: confirm narrow, scoped authority
exists before collecting people, production, or sensitive-source evidence,
rather than defaulting to it. (2) Testimony attribution: confirm human
evidence is recorded as attributable testimony, never silently promoted to
system fact.

**Escalation** — Default: identify the smallest evidence gap most likely to
change the recommendation, predefine what results support, weaken, or leave
it unresolved, and prefer existing artifacts and local checks first.
Information value overrides the default when only people, production, or
sensitive sources can resolve the gap — escalate to obtaining narrow
authority before collecting.

**Pressure scenario** — The fastest way to resolve the question is a
production query against data the requester isn't scoped to see: does the
investigation stop here, or is there a narrower authorized query that still
discriminates?

### `alawas-research-produce-report`

**Gates** — (1) Source and supersession integrity: confirm every claim traces
to a sub-question outcome or accepted Decision, and that later evidence or
History has not narrowed or overturned it. (2) Deliverable authority: confirm
the write stays inside `.work-studio/deliverables/`; export, publication, and
other external writes require explicit per-instance authority.

**Escalation** — Default: classify the deliverable as report or plan, invoke
`alawas-research-investigate-live-question` for each report sub-question, and
synthesize only accepted Decisions for a plan. Information value overrides
the default when a contradiction or supersession gap could change the final
document — resolve and record that gap before presenting the synthesis. If a
plan needs a new decision, stop and route it for decision pressure-testing.

**Pressure scenario** — Later History narrows an earlier accepted Decision,
but the earlier wording makes the plan sound more complete: does the report
retain the stale wording, or drop it with an explicit supersession note and
carry forward only what the final record supports?

### `alawas-operations-diagnose-production-incident`

**Gates** — (1) Ongoing-harm containment: confirm the safest reversible
containment is applied before anything else when harm is actively growing.
(2) Emergency-access scope: confirm diagnostic access and communications
authority are narrow, redacted, and expiring, never standing.

**Escalation** — Default: reduce growing harm with safe reversible
containment across leading hypotheses, maintain separate impact, mechanism,
and communication tracks, and apply containment incrementally as the harm
trajectory permits. Information value overrides the default when a recent
change is only a hypothesis without timeline or mechanism evidence — escalate
to confirming mechanism before treating it as the cause.

**Pressure scenario** — The fastest containment also cuts off legitimate
traffic for unaffected users: does the harm trajectory justify that trade, or
is there a narrower containment that protects the same boundary?

### `alawas-business-manage-commercial-pipeline`

**Gates** — (1) Buying-evidence integrity: confirm stage movement is supported
by customer need, decision-process, timing, and a dated mutual commitment, not
activity volume or a label. (2) External commitment: confirm contact, CRM
writes, pricing, terms, and promises have separate scoped authority.

**Escalation** — Default: reconstruct opportunities from evidence, apply stage
exit criteria, separate gross pipeline from an evidence-weighted forecast, and
recommend advance, hold, requalify, or close. Escalate when concentration,
staleness, or a missing decision actor could reverse the forecast.

**Pressure scenario** — A large late-stage opportunity has frequent meetings
but no identified economic decision-maker or dated customer commitment: does
it remain in the forecast, move backward, or close as unqualified?

### `alawas-business-assess-financial-decision`

**Gates** — (1) Assumption integrity: confirm arithmetic, source facts,
operational estimates, and judgment are visibly separate. (2) Money boundary:
confirm analysis never becomes spend approval, money movement, filing, or
professional advice without separately scoped authority.

**Escalation** — Default: compare the status quo and credible alternatives,
model cash timing and downside/base/upside cases, test reversal variables, and
recommend proceed, revise, defer, or stop. Escalate when liquidity, an
irreversible cost, or one weak assumption dominates the result.

**Pressure scenario** — The base case clears the return threshold but the
downside case creates a cash shortfall before benefits arrive: is expected
profit enough, or must the decision change until liquidity is protected?

### `alawas-business-plan-workforce-accountability`

**Gates** — (1) Work-before-headcount: confirm required outcomes, capacity,
skills, and decisions are defined before recommending roles or people changes.
(2) People protection: confirm system and role gaps are not converted into
unsupported individual judgments and personnel actions remain separately gated.

**Escalation** — Default: map demand to required work, role-level coverage,
overload, ownership, and single points of failure; compare redesign, stopping
work, automation, development, contracting, and hiring. Escalate when private
data or a consequential personnel action becomes necessary.

**Pressure scenario** — A team misses a service target while every individual
appears busy: is the gap capability, capacity, process design, unclear
accountability, or demand volatility—and what evidence discriminates?

### `alawas-business-improve-operating-process`

**Gates** — (1) Map/reality integrity: confirm the current state reflects
actual work and is marked provisional when observation is absent. (2) Whole-flow
safety: confirm a local efficiency change does not damage customer outcome,
quality, people, controls, or downstream flow.

**Escalation** — Default: define the value stream, capture demand and actual
flow, distinguish value/control/delay/failure demand, locate the constraint,
and design one safeguarded experiment. Escalate when live observation, control
changes, staffing, suppliers, or customer commitments require new authority.

**Pressure scenario** — Removing a review step cuts cycle time but that review
catches rare high-cost errors: should it be removed, redesigned at the
constraint, or retained until error-risk evidence improves?

### `alawas-business-formulate-strategy`

**Gates** — (1) Choice-set integrity: confirm the strategy names objective,
arena, advantage thesis, non-goals, assumptions, and review trigger rather than
a slogan. (2) Commitment authority: confirm public commitments, material
reallocation, and owner/board decisions are separately authorized.

**Escalation** — Default: compare strategic alternatives, expose assumptions,
route market, money, capacity, process, and delivery gaps, and recommend one
choice set. Escalate when weak market evidence or an unowned resource movement
could reverse the strategy.

**Pressure scenario** — The strategy sounds compelling but cannot name what it
will stop doing: is it a real strategic choice, or an aspiration that would let
every downstream initiative claim fit?

### `alawas-business-manage-market-intelligence`

**Gates** — (1) Market-boundary integrity: confirm segment, geography, time
window, source date, and decision impact are explicit. (2) Collection authority:
confirm paid data, scraping, competitor/customer contact, personal data, and
publication are separately authorized.

**Escalation** — Default: classify demand, competitor, substitute, and source
evidence, expose uncertainty, and state what changes in the decision. Escalate
when a stale or indirect source is carrying the recommendation.

**Pressure scenario** — A competitor appears in every secondary article but
there is no evidence customers substitute it for this offer: is it a market
threat, a category neighbor, or noise?

### `alawas-business-build-driver-based-plan-and-forecast`

**Gates** — (1) Driver integrity: confirm every number traces to a source,
driver, or named assumption. (2) Forecast authority: confirm budgets, filings,
financing, and publication are separately authorized and forecasts are not
presented as assurance.

**Escalation** — Default: build downside/base/upside scenarios, separate
profit, cash, and balance-sheet effects, and expose reversal variables.
Escalate when one weak driver or cash-timing assumption dominates the baseline.

**Pressure scenario** — The base scenario looks healthy, but one unsupported
volume driver creates most of the cash cushion: does the plan stand, or route
to market or pipeline evidence before it is used?

### `alawas-business-manage-enterprise-risk`

**Gates** — (1) Residual-exposure integrity: confirm treatment leaves visible
residual risk, owner, and monitoring evidence. (2) Acceptance authority: confirm
risk acceptance, safety/privacy/security/money exposure, insurance, contract,
and regulated matters are separately authorized.

**Escalation** — Default: frame objective, cause, consequence, controls,
treatment options, owner, and residual exposure. Escalate when a control design
is being treated as operating evidence or acceptance is inferred from silence.

**Pressure scenario** — A mitigation plan exists but no one can show it has
operated under real conditions: is the residual risk actually reduced, or only
documented?

### `alawas-business-source-and-govern-suppliers`

**Gates** — (1) Qualification integrity: confirm make/buy logic, criteria,
supplier evidence, relationship model, and performance evidence are distinct.
(2) Procurement authority: confirm supplier contact, RFPs, negotiation, award,
purchase, contracts, shared data, and spend are separately authorized.

**Escalation** — Default: compare make, buy, defer, and redesign paths against
criteria, cost, service, risk, and governance. Escalate when a cheap supplier or
favored vendor lacks performance evidence.

**Pressure scenario** — The lowest-cost supplier meets the written feature list
but creates dependency and service risk the criteria did not score: does the
recommendation change or do the criteria need repair?

### `alawas-business-direct-project-delivery`

**Gates** — (1) Baseline integrity: confirm accepted scope, schedule,
dependencies, change-control rule, and acceptance criteria are separate from
requested scope. (2) Commitment authority: confirm baseline changes, resources,
customer/vendor communications, spend, contracts, live-system changes, and
implementation are separately authorized.

**Escalation** — Default: inspect baseline, status, dependencies, risks, change
requests, and recovery options, then recommend continue, recover, escalate,
defer, or stop. Escalate when status labels hide unowned dependency or scope
change.

**Pressure scenario** — The project is green because the date moved and scope
grew informally: is it controlled delivery, or baseline drift that needs a
fresh owner decision?

### `alawas-business-manage-customer-success`

**Gates** — (1) Outcome integrity: confirm usage, sentiment, and relationship
signals are not treated as proof of realized customer value. (2) Customer
authority: confirm contact, CRM/CS writes, private-data expansion, concessions,
refunds, renewal terms, promises, and escalations are separately authorized.

**Escalation** — Default: assess onboarding, adoption, realized outcome, health,
renewal risk, obligations, and intervention options. Escalate when an account
intervention would become a concession, promise, or private-data expansion.

**Pressure scenario** — Usage is high and the relationship is warm, but the
customer cannot show the sold outcome improved: is the account healthy, or is
renewal risk being hidden by activity?

### `alawas-business-govern-initiative-portfolio`

**Gates** — (1) Portfolio-choice integrity: confirm the recommendation compares
strategy, benefit, cost, capacity, dependency, risk, reversibility, and evidence
quality rather than ranking sponsor preferences. (2) Commitment authority:
confirm funding, cancellation, staffing/resource movement, customer/vendor
impact, executive/public commitments, and material reallocation are separately
authorized.

**Escalation** — Default: normalize initiatives into comparable evidence,
test capacity and dependency conflicts, compare start/continue/pause/stop/
defer/resequence options, and expose stop conditions. Escalate when one weak
benefit estimate or one hidden capacity constraint carries the portfolio choice.

**Pressure scenario** — A favored initiative has the loudest sponsor and best
status color but consumes the only team needed by two better-evidenced bets: is
it still the priority, or is the portfolio laundering attention through status?

### `alawas-business-design-pricing-and-packaging`

**Gates** — (1) Offer-architecture integrity: confirm value metric, package
boundary, price/range, discount fence, and test condition are distinct from one
deal's negotiation. (2) Publication authority: confirm published prices,
customer quotes, discounts, regulated claims, protected-class-sensitive pricing,
and live commerce/CRM changes are separately authorized.

**Escalation** — Default: compare customer value, willingness-to-pay evidence,
competitor/substitute references, economics, service burden, fairness, and
operational feasibility. Escalate when competitor prices or desired margin are
standing in for actual value evidence.

**Pressure scenario** — The team copied a competitor's price and added a
discount, but no one can name the value metric or package fence: is this an
offer design, or a margin wish disguised as pricing?

### `alawas-business-manage-liquidity-and-cash-runway`

**Gates** — (1) Cash-timing integrity: confirm available cash, dated
obligations, committed inflows, restrictions, and scenario timing are separated
from profit, bookings, and receivables. (2) Treasury authority: confirm
payments, transfers, borrowing, investments, collections, tax filings,
covenant/insolvency matters, and external creditor/customer communications are
separately authorized.

**Escalation** — Default: build dated base/downside/upside cash views, identify
earliest gap, runway range, reversal variables, safe options, and escalation
triggers. Escalate when one optimistic collection or omitted obligation changes
survival timing.

**Pressure scenario** — The P&L is positive, but payroll is due before the
largest receivable is collectible: does the business have runway, or only
accounting comfort?

### `alawas-business-balance-demand-supply-capacity`

**Gates** — (1) Feasibility integrity: confirm forecast demand, committed
demand, nominal capacity, usable capacity, supplier lead time, inventory, and
quality constraints are separate. (2) Execution authority: confirm schedules,
purchase orders, inventory moves, customer promises, supplier commitments,
staffing changes, and live ERP/MRP/CRM writes are separately authorized.

**Escalation** — Default: reconcile demand, supply, capacity, backlog,
inventory, constraints, scenarios, and exception rules into a feasible plan.
Escalate when a plan treats forecast demand as committed or nominal capacity as
usable capacity.

**Pressure scenario** — Sales can sell twice what operations can deliver, and
supplier lead time is longer than the promised delivery date: is the plan
feasible, or just demand wearing a calendar?

### `alawas-governance-maintain-working-method`

**Gates** — (1) Exception authority: confirm `use when`, `do not use when`,
and exception authority are explicit before a rule can override normal
judgment. (2) Guardrail expiry: confirm a temporary guardrail expires
automatically rather than becoming permanent by default.

**Escalation** — Default: require an observable behavior and reviewable
outcome, find contexts where the proposed rule creates friction or worse
results, and run a bounded trial with a rollback path. Information value
overrides the default when exceptions to a rule become frequent — escalate to
challenging the rule boundary itself before treating exceptions as
noncompliance.

**Pressure scenario** — A working-method rule has had three quiet exceptions
this month: is the rule still correct as stated, or does the boundary itself
need revising before a fourth exception happens?

### `alawas-governance-govern-scorecards`

**Gates** — (1) Personal/privacy default: confirm personal evidence stays
private by default and that aggregation, sharing, or system-wide rule
creation requires explicit purpose, minimal disclosure, and authority. (2)
Non-compensable failure visibility: confirm aggregation never averages away a
subgroup harm or non-compensable failure.

**Escalation** — Default: determine whether each dimension has attributable,
decision-relevant evidence, separate observation from interpretation from
action, and let thresholds trigger evidence inspection rather than automatic
action. Information value overrides the default when a dimension repeatedly
fails to inform decisions — escalate to retiring it rather than continuing to
track it.

**Pressure scenario** — A scorecard dimension trends downward in aggregate
but is flat for every subgroup except one: does the aggregate trend justify
action, or does this need subgroup-level inspection before any rule changes?

### `alawas-design-track-components`

**Gates** — (1) Registry and mutation authority: confirm that registration,
retirement, cascade, or a schema change has the Work Object or owner authority
the ledger contract requires. (2) Finding-to-commitment boundary: confirm a
sweep queues signals only and never silently creates or changes Work Objects.

**Escalation** — Default: resolve locations and lineage, calculate grilling
debt from declared consequence, staleness, blast radius, and git drift, then
run the owning profile against applicable inline dimensions. Information value
overrides the default when a missing dependency edge or contrary outcome
evidence could invalidate a settled status — escalate to the smallest
evidence-gathering or owner decision before re-stamping the entry.

**Pressure scenario** — A high-blast-radius component is settled and inside its
cooldown, but a dependent declares a contract change: does the cascade reopen
it before any ordinary debt ranking, and is the declared edge sufficient?

### `alawas-design-apply-design-direction`

**Gates** — (1) Direction specificity: confirm the natural-language direction
can be translated into observable specification changes before producing a
revision manifest. (2) Preserve/revise boundary: confirm that preserve targets
are explicit and grounded in current state, not inferred as "everything else."

**Escalation** — Default: parse the direction, read current specifications and
evidence, classify each affected target as preserve/revise/prohibited, present
the manifest for confirmation, and record it. Information value overrides the
default when the direction is ambiguous between two conflicting specification
changes — escalate to clarifying the user's intent before producing a manifest
that silently picks one interpretation.

**Pressure scenario** — The user's direction says "simplify the layout" but
the current specification has two layout regions serving different user goals:
does the revision manifest preserve both and simplify within each, or does it
merge them and risk losing a goal the user didn't intend to drop?

### `alawas-design-audit-product-interface`

**Gates** — (1) Discovery scope: confirm the discovery covers the routes,
components, and layouts actually present in the codebase, not an assumed or
remembered set. (2) Zero-onboarding boundary: confirm the discovery requires
no project-specific configuration or onboarding from the user (DEC-2).

**Escalation** — Default: scan routes, components, layouts, and patterns;
produce a `[system:discovery]` Evidence Ledger entry with structural inventory
and framework detection. Information value overrides the default when the
discovered structure conflicts with an existing Work Object's assumptions —
escalate to reconciling the conflict before recording discovery as settled.

**Pressure scenario** — The scan finds a component that appears in routes but
has no corresponding source file (dynamically generated or aliased): does the
discovery record it as present with a gap, or omit it and risk an incomplete
inventory downstream?

### `alawas-design-build-design-foundation`

**Gates** — (1) Token source authority: confirm tokens are discovered from
code, not invented or assumed from a design tool. (2) Independence from
structural discovery: confirm the token audit does not depend on or wait for
`alawas-design-audit-product-interface` results (DEC-6).

**Escalation** — Default: scan the codebase for design tokens (colors,
typography, spacing, breakpoints), audit their usage and consistency, and
produce a `[system:token-inventory]` Evidence Ledger entry. Information value
overrides the default when discovered tokens conflict with each other (e.g.,
two competing color scales) — escalate to documenting the conflict rather than
silently picking one as canonical.

**Pressure scenario** — The codebase uses both a CSS custom property system
and a JS theme object with overlapping but not identical token values: does the
inventory record both sources and flag the divergence, or does it pick one as
canonical and risk the other's consumers being silently wrong?


**Gates** — (1) Architecture grounding: confirm the screen hierarchy and
navigation structure are grounded in discovery evidence and user flows, not
assumed from intent alone. (2) Specification boundary: confirm the architecture
document defines structure and navigation, not visual design or implementation.

**Escalation** — Default: define the screen hierarchy, navigation patterns,
information architecture, and responsive strategy; produce a durable YAML
document at `design/architecture/`. Information value overrides the default
when the architecture reveals a navigation pattern that conflicts with an
existing user flow — escalate to reconciling the conflict before recording the
architecture as settled.

**Pressure scenario** — The user flow requires a screen transition that the
discovered framework's router doesn't natively support (e.g., nested modals
with independent back-stack): does the architecture document this as a
constraint and route to implementation investigation, or assume the framework
can handle it?


**Gates** — (1) Goal grounding: confirm each user flow starts from a real user
goal, not a system capability or feature name. (2) State completeness: confirm
the flow maps happy path, error, and edge-case states, not just the golden
path.

**Escalation** — Default: identify user goals, map actions to states and
responses, produce a durable YAML flow document at `design/flows/`.
Information value overrides the default when a user flow reveals a goal that no
existing Work Object covers — escalate to signaling the gap to the conductor
before recording the flow as complete.

**Pressure scenario** — Two user goals share the same entry point but diverge
at the second step: does the flow model them as one flow with a branch or two
separate flows, and does the choice affect how the architecture will handle
navigation state?

### `alawas-design-verify-design-implementation`

**Gates** — (1) Dimension honesty: confirm that deferred dimensions
(behavioral, full-stack, accessibility) are explicitly reported with reasons,
never silently omitted (DEC-18). (2) Evidence grounding: confirm structural and
visual checks reference the confirmed proposal (`[system:design-direction]`),
not assumptions about what the implementation should look like, and that a
manual-fallback visual confirmation is recorded as attributable testimony
rather than system-observed rendering.

**Escalation** — Default: load the confirmed proposal, check that each
confirmed change is present in the code and that preserve targets are intact,
compare the browser rendering against the confirmed intent at the specified
viewports, and produce a `[system:verification-report]` with per-change and
per-dimension status. Information value overrides the default when a structural
match hides a visual mismatch (the change is present in code but the browser
does not reflect it) — escalate to establishing which layer diverges before
reporting it as a simple implementation error.

**Pressure scenario** — Every confirmed change is present in the code and the
browser matches at all three viewports, but the diff also touches a file
outside the confirmed scope: does the report pass on the confirmed changes
alone, or does the unintended change make this a fail that routes back to
`alawas-design-apply-design-direction`?

### `alawas-design-audit-accessibility`

**Gates** — (1) Mechanism honesty: confirm each finding discloses whether it
came from browser-computed styles or static parsing, since static parsing
cannot see cascade, `:hover`/`:focus` states, or JS-driven color. (2)
Deferred-dimension honesty: confirm keyboard navigation, focus order, and
screen-reader behavior are named as deferred with a reason, never silently
folded into a passing report.

**Escalation** — Default: audit the real rendered surface for contrast and
semantic-structure conformance against a stewarded expectation or the WCAG
generic baseline, and produce a `[system:accessibility-audit]` Evidence
Ledger entry with concrete per-check values. Information value overrides the
default when no stewarded expectation exists for the audited surface —
escalate to naming that gap explicitly (which baseline was used and why)
rather than silently treating the generic baseline as equivalent to a
project-specific one.

**Pressure scenario** — A contrast pair passes the WCAG generic threshold but
the surface has a stewarded pattern stating a stricter project-specific
minimum: does the audit report against the generic pass, or does it apply the
stricter stewarded expectation and report a fail the generic check would have
missed?
