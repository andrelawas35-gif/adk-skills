# Comprehensive Business-Skill Portfolio for Work Studio

**Work Object:** `2026-08-22-008`  
**Deliverable type:** research report  
**Scope:** additional reusable business-management skills beyond the four
currently installed business skills  
**Confidence:** high that the named decision frontiers are distinct; medium on
implementation order because Work Studio has no observed usage-frequency data
for these candidates

## Executive conclusion

[system] Work Studio currently owns four business frontiers: commercial
pipeline decisions, bounded financial decisions, workforce/accountability
planning, and recurring operating-process improvement. Its general lifecycle,
research, design, implementation, verification, deployment, incident, outcome,
and scorecard skills are not substitutes for missing business-domain judgment.

[inference] A comprehensive but coherent portfolio should add **24 standalone
skills in three waves** and keep **7 narrower candidates as profiles or
compositions until repeated use proves they need their own contract**. The
design unit is one recurring decision frontier with its own evidence, output,
authority boundary, and downstream route—not one department and not one
framework.

The highest-leverage next implementation wave is:

1. `alawas-business-formulate-strategy`
2. `alawas-business-govern-initiative-portfolio`
3. `alawas-business-manage-market-intelligence`
4. `alawas-business-design-pricing-and-packaging`
5. `alawas-business-manage-customer-success`
6. `alawas-business-build-driver-based-plan-and-forecast`
7. `alawas-business-manage-liquidity-and-cash-runway`
8. `alawas-business-manage-enterprise-risk`
9. `alawas-business-source-and-govern-suppliers`
10. `alawas-business-direct-project-delivery`
11. `alawas-business-balance-demand-supply-capacity`
12. `alawas-business-manage-quality-and-corrective-action`
13. `alawas-business-lead-organizational-change`
14. `alawas-business-establish-data-governance`
15. `alawas-business-plan-and-exercise-continuity`

These fifteen cover the largest upstream, cross-functional, and resilience
gaps without duplicating the existing four.

## How the portfolio was bounded

[system] APQC's Process Classification Framework describes organizational work
comprehensively and without redundancy across strategy, products/services,
market/sell, delivery, customer service, human capital, technology, finance,
assets, risk/compliance/resilience, external relationships, and business
capabilities. [APQC PCF overview](https://www.apqc.org/sites/default/files/files/PCF%20One-Pager%20March%202016.pdf)

[inference] APQC was used as a breadth check, not copied into skills. A
candidate qualified only when:

- it owns a repeated management decision that could change a Work Object's
  recommendation or route;
- its minimum evidence and output differ from existing skills;
- its authority risks need an explicit gate; and
- composition of current skills would otherwise omit material domain rules.

[system] The project `work-studio-mcp` server was invoked through its stdio MCP
protocol. Discovery returned exactly one authorized tool, `ws_validate`. The
first call correctly rejected the Inquiry because its Evidence Ledger was
empty; after the MCP result was recorded through the conductor, a later MCP
validation returned `exit_code=0` and all default checks passed. The server
also warned that no `.bak-*` baseline exists, so append-only verification is
unavailable for this new object.

## Wave 1 — Core management system

| Candidate skill | Decision it owns | Boundary with current Work Studio | Principal authority gate |
|---|---|---|---|
| `formulate-strategy` | Choose strategic objectives, arenas, advantage thesis, explicit non-goals, assumptions, and review triggers. | `pressure-test-decision` tests one choice; this skill creates a coherent strategic choice set. | Owner/board approval, public commitments, material reallocation. |
| `govern-initiative-portfolio` | Start, sequence, fund, pause, or stop initiatives under strategic fit, capacity, dependency, risk, and expected benefit. | `govern-scorecards` judges outcomes; it does not allocate the portfolio. | Funding, cancellation, staffing, executive commitments. |
| `manage-market-intelligence` | Maintain market boundaries, demand, competitors/substitutes, drivers, signals, confidence, and refresh cadence tied to decisions. | `investigate-live-question` answers one inquiry; pipeline manages named opportunities. | Paid/licensed data, scraping, competitor/customer contact, personal data. |
| `design-pricing-and-packaging` | Choose value metric, package structure, prices/ranges, fences, discount rules, and test design. | Pipeline explicitly excludes pricing; financial assessment tests economics after the offer assumptions exist. | Published prices, discounts, discrimination, regulated-market claims. |
| `manage-customer-success` | Prioritize onboarding, adoption, realized outcomes, health evidence, renewal risk, and intervention across the post-sale lifecycle. | Pipeline owns buying progression; process improvement does not own customer outcome realization. | Customer contact, CRM writes, private usage data, concessions and promises. |
| `build-driver-based-plan-and-forecast` | Translate operating drivers and scenarios into an integrated profit, cash, and balance-sheet planning baseline. | Financial assessment evaluates one choice; this maintains the baseline against which choices are tested. | Private financial data; forecasts cannot be presented as accounting or assurance. |
| `manage-liquidity-and-cash-runway` | Determine whether obligations can be met when due, expose timing gaps, and recommend escalation or financing options. | One-off financial assessment is not a recurring short-horizon cash-control loop. | Payments, transfers, borrowing, investments, insolvency/covenant matters. |
| `manage-enterprise-risk` | Establish appetite/tolerance, assess the cross-enterprise risk portfolio, select treatment, assign ownership, and monitor residual exposure. | Decision pressure-testing handles one decision; incident diagnosis starts after harm. | Risk acceptance stays with accountable humans; no legal, actuarial, safety, or insurance assurance. |
| `source-and-govern-suppliers` | Decide make/buy, sourcing strategy, supplier selection/award recommendation, relationship model, and performance response. | Pipeline is sell-side; financial analysis compares economics but does not qualify or govern suppliers. | RFPs, supplier contact/data, award, purchase order, negotiation, contract and sanctions decisions. |
| `direct-project-delivery` | Select delivery approach, baseline scope/schedule/dependencies, control change, and decide continue/recover/escalate. | Work Objects govern durable intent; bounded implementation executes one accepted change. Neither is integrated project control. | Baseline changes, resource commitments, vendor/customer communications. |
| `balance-demand-supply-capacity` | Reconcile forecast demand, constraints, inventory policy, supply, capacity, and exception actions into a feasible operating plan. | Process improvement redesigns flow; it does not own periodic planning under uncertainty. | Production schedules, purchase orders, inventory actions, ERP/MRP changes. |
| `manage-quality-and-corrective-action` | Set quality controls, classify nonconformity, determine root cause, choose containment/correction, and verify CAPA effectiveness. | Process improvement optimizes flow; quality owns conformance, disposition, control integrity, and auditability. | Holds/releases, recalls, regulatory reports, safety dispositions, customer notice. |
| `lead-organizational-change` | Assess impacts/readiness, choose adoption interventions and sequencing, set adoption gates, and reinforce or stop. | Project delivery manages the initiative; workforce planning assigns work but does not own human adoption. | Employee monitoring, communications, role changes, labor consultation, personal data. |
| `establish-data-governance` | Assign data ownership and decision rights; define critical data, quality, metadata, access, lifecycle, and remediation. | Scorecards consume measures; this skill governs whether the underlying data is fit and appropriately controlled. | Access grants, personal/confidential data, privacy, retention, security and legal decisions. |
| `plan-and-exercise-continuity` | Conduct business-impact analysis, set essential functions and recovery priorities, design continuity strategies, and test them. | Deployment rollback is change-specific; production incident diagnosis is reactive and technical. | Safety, emergency command, regulated recovery targets, exercises and public communications. |

## Wave 2 — Growth, control, and organizational capability

| Candidate skill | Decision it owns | Why it remains distinct | Principal authority gate |
|---|---|---|---|
| `plan-marketing-and-demand` | Choose target segment, positioning, substantiated message, channels, campaign hypothesis, spend ceiling, measures, and stop rules. | Pipeline begins with opportunities; it does not create demand or authorize claims. | Publication, ad spend, consent/tracking, endorsements, personal data. |
| `manage-product-portfolio` | Invest, continue, pivot, pause, or retire products/services as a mix. | Initiative portfolio allocates change work; this manages the market offering portfolio and lifecycle obligations. | Retirement/customer harm, support obligations, staffing and budget shifts. |
| `manage-product-opportunities-and-roadmap` | Validate customer/market problems, choose opportunity bets, sequence roadmap options, and set pre-build gates. | Thinking/design skills shape accepted work; they do not own the business product decision. | Customer research, roadmap promises, experiments, confidential strategy. |
| `manage-partnerships-and-alliances` | Select partners, define mutual value/contributions, establish governance and performance, escalate, renew, or exit. | Customer pipeline and supplier sourcing do not cover reciprocal collaborative relationships. | Contact, negotiation, IP/data sharing, exclusivity, joint commitments, contracts. |
| `govern-revenue-operations` | Govern commercial lifecycle definitions, source-of-truth data, handoffs, capacity assumptions, and forecast calibration across marketing, sales, success, and finance. | Pipeline decides opportunity actions; this owns cross-functional commercial semantics and controls. | CRM/schema changes, bulk customer data, automated scoring, access and compensation effects. |
| `manage-customer-service-recovery` | Triage complaints, choose a fair remedy/escalation, communicate and verify closure, and route systemic learning. | Process improvement redesigns the system; this owns one complaint's remedy and fairness lifecycle. | Contact, refunds/credits, admissions, disputes, sensitive case data. |
| `control-budget-and-reforecast` | Reconcile actuals with budget, explain material variances, update forecasts, and recommend corrective reallocations. | Scorecards reveal variance; this changes the forward resource plan. | Journal entries, transfers, spend, headcount or operational commitments. |
| `design-and-test-internal-controls` | Convert operational/reporting/fraud/compliance risk into controls, test design and operation, and track remediation. | Process improvement asks whether flow improves; controls ask whether objectives remain protected and evidenced. | No audit certification; preserve independence and segregation of duties. |
| `operate-compliance-program` | Run risk assessment, policies, training, reporting channels, investigation routing, remediation, testing, and refresh. | Enterprise risk chooses treatment; this operationalizes obligations. | No legal conclusions, privileged investigation, retaliation, confidentiality promise, or self-disclosure. |
| `build-workforce-capability` | Choose competence priorities, learning/development interventions, succession coverage, and evidence of competence. | Workforce/accountability plans roles and capacity, not learning systems or succession readiness. | Assessments, personnel records, promotion readiness, protected data. |
| `steward-organizational-knowledge` | Identify critical knowledge, loss/exposure risk, validation, sharing, retention, and evidence of reuse. | `maintain-working-method` governs Work Studio's own method, not enterprise knowledge. | Confidentiality, IP, retention, access, personal archives and source reliability. |
| `manage-assets-and-lifecycle-value` | Balance asset performance, risk, expenditure, maintenance, renewal, and disposal against organizational objectives. | Financial analysis tests a choice; process improvement maps work; neither owns the asset lifecycle system. | Purchase/disposal, safety, environmental, accounting and regulated-maintenance decisions. |
| `manage-environmental-sustainability` | Identify material environmental aspects/obligations, set objectives, choose lifecycle interventions, and govern credible measures. | Financial, process, and scorecard skills supply evidence but do not own environmental materiality or claims. | Regulatory interpretation, public claims, measured/estimated data, certification and supplier requirements. |

## Wave 3 — Add only after observed need

These frontiers are real, but composition or a profile should be tested before
creating another standalone skill.

| Candidate | Initial home | Split trigger |
|---|---|---|
| Strategic review and reallocation | Profile composing `formulate-strategy`, `govern-initiative-portfolio`, scorecards, and outcome review. | Three uses show the review cadence loses decisions between those skills. |
| Working-capital management | Profile under liquidity plus supplier/customer routes. | Recurring receivable/payable/inventory interventions require their own evidence record. |
| Third-party due diligence | Gate/profile shared by sourcing and compliance. | Volume or risk tiering becomes a recurring standalone decision queue. |
| Contract intake and obligation management | Profile shared by sourcing, partnerships, pipeline, and compliance. | Missed approvals/renewals or obligation volume proves a separate lifecycle is needed. |
| Supply-chain resilience | Profile under continuity plus demand/supply planning. | Network-specific disruption scenarios repeatedly exceed enterprise continuity scope. |
| Programme and benefits realization | Composition of project delivery and initiative portfolio. | Multiple coordinated projects share benefits and dependencies that cannot be governed separately. |
| Performance and rewards | High-consequence extension of workforce accountability, initially disabled by default. | A governed HR environment demonstrates repeated need, lawful policy, fairness controls, and qualified human ownership. |

`govern-go-to-market-launch`, `manage-crisis-command`, `manage-insurance-and-risk-transfer`,
and policy lifecycle management are also credible profiles. They should not be
standalone until use shows that composition loses evidence or authority.

## Important exclusions

[inference] The following should not become generic Work Studio skills:

- legal advice, tax advice, audit opinions, investment advice, clinical or
  safety certification;
- automatic hiring, firing, promotion, pay, discipline, credit, pricing, or
  risk-acceptance decisions;
- vendor-specific CRM, ERP, accounting, advertising, or HRIS operating playbooks;
- a generic `manage-business` omnibus; or
- a generic `ESG` skill that collapses governance, people, risk, suppliers,
  environmental evidence, and public reporting into one authority boundary.

## Cross-skill routing model

[inference] Every new business skill should retain the same Work Studio shape:

1. The conductor owns the Work Object and lifecycle mutation.
2. The business skill owns one domain decision record.
3. `investigate-live-question` resolves material evidence gaps.
4. `assess-financial-decision` tests money consequences where relevant.
5. `plan-workforce-accountability` tests role/capacity consequences.
6. `improve-operating-process` designs recurring-flow experiments.
7. `pressure-test-decision` challenges a material recommendation.
8. `implement-bounded-change` executes only an accepted reversible change.
9. External communications, money, personnel action, contracts, live-system
   writes, regulated claims, and high-consequence acceptance remain explicitly gated.

## Primary-source evidence ledger

- [system] APQC separates the major operating and management/support domains
  used as the breadth check. [APQC PCF](https://www.apqc.org/resource-library/resource-listing/apqc-process-classification-framework-pcf-cross-industry-pdf-7)
- [system] ISO 37000 treats purpose, strategy, value generation, oversight,
  accountability, stakeholders, data, risk, and long-term viability as
  governance concerns. [ISO 37000](https://www.iso.org/standard/65036.html)
- [system] PMI distinguishes project, programme, portfolio, and organizational
  project management; portfolio management groups work to meet strategic
  objectives. [PMI standards](https://www.pmi.org/standards/),
  [Portfolio standard](https://www.pmi.org/standards/for-portfolio-management)
- [system] ISO 56006 defines strategic-intelligence management, while ISO
  56007 separates opportunity identification, concepts, validation, and
  development decisions. [ISO 56006](https://www.iso.org/standard/72621.html),
  [ISO 56007](https://www.iso.org/standard/75068.html)
- [system] FTC policy requires objective advertising claims to have a
  reasonable evidentiary basis before dissemination. [FTC substantiation policy](https://www.ftc.gov/legal-library/browse/ftc-policy-statement-regarding-advertising-substantiation)
- [system] ISO 10002 covers the complete complaints-handling process and its
  improvement; ISO 10004 covers monitoring and measuring customer satisfaction.
  [ISO 10002](https://www.iso.org/standard/71580.html),
  [ISO 10004](https://www.iso.org/standard/71582.html)
- [system] SBA guidance separates market/competitive research from sales and
  describes balance-sheet and cash-flow projections as foundational financial
  management evidence. [SBA market research](https://www.sba.gov/business-guide/plan-your-business/market-research-competitive-analysis),
  [SBA financial management](https://www.sba.gov/counseling/manage-your-business/)
- [system] COSO integrates enterprise risk with strategy and performance.
  [COSO ERM](https://www.coso.org/enterprise-risk-management)
- [system] GAO's Green Book defines internal control as an integrated
  management process serving operations, reporting, and compliance.
  [GAO Green Book](https://www.gao.gov/greenbook)
- [system] DOJ evaluates whether compliance programs are well designed,
  resourced/empowered, and effective in practice. [DOJ compliance guidance](https://www.justice.gov/criminal/criminal-fraud/page/file/937501)
- [system] ISO 20400 covers sustainable procurement; ISO 44001 covers the
  identification, development, and management of collaborative relationships.
  [ISO 20400](https://www.iso.org/standard/63026.html),
  [ISO 44001](https://www.iso.org/standard/72798.html)
- [system] ASCM's SCOR standard separates Plan and Source and treats balancing
  requirements/resources and supplier-facing orchestration as explicit
  processes. [ASCM SCOR](https://www.ascm.org/corporate-solutions/standards-tools/scor-ds/)
- [system] ISO 9001 and the quality-management principles distinguish customer
  focus, process approach, conformance, evidence-based decisions, correction,
  and continual improvement. [ISO 9001](https://www.iso.org/standard/62085.html),
  [ISO quality principles](https://www.iso.org/quality-management/principles)
- [system] ISO/TS 10020 specifies processes to govern, manage, and implement
  organizational change. [ISO/TS 10020](https://www.iso.org/standard/82213.html)
- [system] ISO 30401 defines an organizational knowledge-management system;
  ISO 10015 addresses competence management and people development.
  [ISO 30401](https://www.iso.org/standard/68683.html),
  [ISO 10015](https://www.iso.org/standard/69459.html)
- [system] ISO 55001 balances asset performance, risk, and expenditure;
  ISO 14001 establishes an environmental management system.
  [ISO 55001](https://www.iso.org/standard/83054.html),
  [ISO 14001](https://www.iso.org/standard/14001)
- [system] ISO 22301 requires continuity capability to protect against,
  prepare for, respond to, and recover from disruption at predefined capacity.
  [ISO 22301](https://www.iso.org/standard/75106.html)
- [system] Federal Data Strategy practices call for explicit data authorities,
  roles, quality, responsible access, lifecycle management, and evidence use.
  [Federal Data Strategy](https://strategy.data.gov/practices/)

## Contradictions, limitations, and supersession

- [gap] No real-use telemetry ranks candidate frequency or pain. Priority is an
  architectural inference based on breadth, dependency leverage, and distinct
  authority—not observed demand.
- [gap] Industry-specific regulated obligations cannot be generalized into
  reusable skill mechanics; they require qualified specialists and local law.
- [gap] Formal individual performance/reward management has unusually high
  people consequences and immature general standards; it remains deferred.
- [inference] The earlier four-skill recommendation is not superseded. Those
  four remain the correct bounded first package; this report expands the
  portfolio beyond that first tranche.
- [inference] Some investigations proposed separate sourcing, supplier
  performance, contract, and third-party-risk skills. They are consolidated
  initially into `source-and-govern-suppliers` plus compliance profiles to
  reduce boundary fragmentation. Split only on observed use.
- [inference] Some investigations proposed separate strategy and project
  portfolios. This report preserves both `formulate-strategy` and one
  `govern-initiative-portfolio`; product portfolio remains separate because
  it governs market offerings rather than change initiatives.

## Recommended next move

Create boundary cards—not full skills—for the fifteen Wave 1 candidates. Each
card should include trigger, governing question, minimum evidence, output,
non-goals, authority gates, routes, and one pairwise overlap test against every
existing business skill. Implement only the smallest first tranche that passes
those tests; a practical starting tranche is strategy, market intelligence,
driver-based planning, enterprise risk, supplier governance, project delivery,
and customer success.
