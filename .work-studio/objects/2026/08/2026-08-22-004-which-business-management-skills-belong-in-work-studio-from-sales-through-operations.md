---
schema_version: 1
id: 2026-08-22-004
title: Which business management skills belong in Work Studio from sales through operations
type: inquiry
status: closed
state: close
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-22T10:56:28Z
updated_at: 2026-08-22T11:07:14Z
next_action: Verify the four-skill package and classify unrelated repository-wide failures
























---
## Intent

Determine which business-management skills, spanning commercial work through
operations, fill material gaps in Work Studio without duplicating existing
skills; use attributable primary-source evidence to recommend a bounded first
set for implementation.

## Success evidence

- [x] Existing Work Studio coverage and gaps are mapped.
- [x] Candidate business skills are supported by attributable primary sources.
- [x] The strongest alternative to adding new skills is tested.
- [x] A bounded skill set is recommended with clear ownership and non-goals.
- [x] Accepted additions are implemented and pass focused adapter/conformance checks; unrelated checkout-wide gaps are recorded.


## Constraints and non-goals

**Constraints:**
- Preserve Work Studio's Work Object lifecycle, evidence, authority, and
  conductor routing model.
- Prefer reusable management decisions over vendor-specific playbooks.
- Keep external communications, financial commitments, hiring, and production
  actions behind explicit authority gates.

**Non-goals:**
- Building a generic library of every business framework.
- Duplicating current scorecard, deployment, incident, or implementation skills.
- Contacting customers, employees, vendors, or live business systems.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Add four bounded business-management skills

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | First set: commercial pipeline management, financial decision analysis, workforce/accountability planning, and operational process improvement. |
| **Authorization** | User explicitly requested research and additions in this conversation. |
| **Confidence** | high for distinct coverage; medium for exact first-version procedure — basis: primary frameworks corroborate the four domains, while real-use evidence is not yet available. |
| **Actor** | user and Codex |
| **Revisit trigger** | Verification shows a skill duplicates an existing decision frontier, or three real uses consistently route across two proposed boundaries. |
| **Rationale** | APQC separates commercial, financial, human-capital, and operational processes; local inspection found no existing skill owns those decisions. Each proposed skill has different required evidence and authority risks, so combining them would create an unfocused manager omnibus. |

### Decision 2 — Accept four-skill tracer implementation

| Field | Value |
|-------|-------|
| **Decision type** | authority |
| **Result** | pass |
| **Scope** | Add four canonical business skill contracts, their grilling profiles, focused behavioral fixtures/tests, kernel and skill-map registration, and deterministically generated adapters. |
| **Authorization** | User explicitly accepted the immediately preceding four-skill implementation recommendation in conversation. |
| **Confidence** | high for repository fit; no claim about practical usefulness until real use — basis: bounded reversible files and executable conformance checks. |
| **Actor** | user |
| **Revisit trigger** | A skill cannot own one decision frontier, duplicates an existing skill, or three real uses consistently cross two proposed boundaries. |
| **Rationale** | This is the smallest complete package spanning commercial, financial, people, and operating management while preserving distinct evidence and authority boundaries. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | work-studio/skill-map.yaml | Current Work Studio skills own lifecycle, evidence, design, implementation, verification, release, incidents, scorecards, and outcomes; none owns a sales opportunity, financial business case, workforce plan, or operating-process design. |
| [system] | APQC, Process Classification Framework Cross-Industry v7.4, 2024-08-21, https://www.apqc.org/resource-library/resource-listing/apqc-process-classification-framework-pcf-cross-industry-pdf-12 | APQC treats business work as nonredundant process domains and distinguishes market/sell, delivery, customer service, human capital, financial resources, and other management/support work. |
| [system] | Salesforce, Pipeline Forecasting and Sales Pipeline Basics, accessed 2026-08-22, https://trailhead.salesforce.com/content/learn/modules/sales-pipeline-basics/build-a-healthy-sales-pipeline | Sales pipeline management requires qualification, stage movement, removal of stagnant leads, conversion/velocity measures, and regularly refreshed opportunity evidence for forecasting. |
| [system] | U.S. Small Business Administration, Manage Your Business and Plan Your Business, accessed 2026-08-22, https://www.sba.gov/counseling/manage-your-business/ | Business financial management depends on balance-sheet, income, cash-flow, cost/benefit, and projection evidence; these are distinct inputs from generic decision pressure-testing. |
| [system] | CIPD, Workforce Planning factsheet, accessed 2026-08-22, https://www.cipd.org/en/knowledge/factsheets/workforce-planning-factsheet/ | Workforce planning balances future demand with current people and skill supply, identifies gaps, links them to organizational goals, and requires clear allocation of responsibilities. |
| [system] | ISO, Quality management principles and ISO 9001 process approach, accessed 2026-08-22, https://www.iso.org/quality-management/principles | The process approach connects defined objectives, responsibilities, process interactions, measurement, risk-based thinking, and continual improvement. |
| [system] | Lean Enterprise Institute, Value Stream Mapping, accessed 2026-08-22, https://www.lean.org/lexicon-terms/value-stream-mapping/ | Operational improvement should capture current material/information flow, design a future state, optimize the whole rather than isolated steps, and form an implementation plan. |
| [inference] | Synthesis of local coverage and primary sources | The smallest coherent first set is four separate skills: commercial pipeline management, financial decision analysis, workforce/accountability planning, and operational process improvement. Confidence is high that the coverage is distinct and medium that the initial procedures will fit real use without revision. |
| [inference] | Strongest alternative test | Embedding all four as lenses in pressure-test-decision or govern-scorecards would reduce file count but collapse four different evidence models and authority boundaries into generic skills; this would obscure routing and increase scope creep. |
| [system] | skills/core/business-*/SKILL.md and tests/test_business_management_skills.py | Implemented four canonical business skill contracts with distinct commercial, financial, workforce, and operating-process decision frontiers and explicit external-effect gates. |
| [system] | uv run pytest focused suite, 2026-08-22 | Five focused business and adapter tests passed. |
| [system] | python tools/generate-adapters.py --check, 2026-08-22 | All generated adapters, manifests, checksums, authority blocks, and capability classifications matched with no drift. |
| [system] | tools/install.ps1 -Platform codex -Project -Dir ., 2026-08-22 | Project-pinned Codex installation succeeded; all four installed SKILL.md files exist and have recorded SHA-256 hashes. |
| [inference] | Implementation boundary review | No lifecycle state, schema, dependency, integration, external contact, money movement, personnel action, or live operational change was added. Rollback remains deletion of the four canonical directories/profiles/tests followed by regeneration. |
| [system] | Focused verification commands, 2026-08-22 | tests/test_business_management_skills.py plus generated-reference and cross-platform core-identity checks passed 5/5; generator drift check passed; project Codex installation completed with four verified skill hashes. |
| [inference] | Verification assessment | The accepted four-skill exit criteria are met within repository-local scope. Retries, duplicate delivery, live dependencies, artifact rendering, deployment, and production recovery are not applicable because the change is static skill packaging with no runtime side effects. |
| [inference] | Repository-wide gap | Kernel and full-suite cleanliness remain blocked by pre-existing untracked research-produce-report work: it is undeclared in the kernel and lacks the required grilling profile/fixture and exact high-consequence authority wording. This is outside Decision 2 scope and was not modified. |
| [inference] | Outcome gap | No real business Work Object has yet exercised the new skills; system fit is verified, practical usefulness remains unverified until observed use. |
## Open questions

- What exact invocation boundaries and output records keep the four skills narrow?
- Which shared business vocabulary belongs in `CONTEXT.md`, if any, after the skills prove useful?

## Next move

Use the four installed skills on real business Work Objects and review their
boundaries if three uses consistently cross two skills or expose missing evidence.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T10:57:03Z — Created and framed inquiry

- **State:** notice
- **Status:** active
- **Actor:** codex
- **Rationale:** Consequence assessment: reversible=yes (skills can be revised or removed); affects beyond workspace=no (repository-only); failure affects safety/privacy/money=no for this research and local implementation. Assigned consequence=meaningful because it changes durable system behavior and requires decision plus verification evidence.
### 2026-08-22T10:57:03Z — Activated business-skill coverage inquiry

- **State:** explore
- **Status:** active
- **Actor:** codex
- **Rationale:** The user explicitly activated the inquiry and requested research before additions.
### 2026-08-22T10:58:38Z — Research outcome: prototype-ready

- **State:** design
- **Status:** active
- **Actor:** codex
- **Rationale:** Primary sources and local coverage inspection support four distinct skills; real-use evidence remains a post-implementation gap, so the route is prototype-ready rather than answered as proven in use.
### 2026-08-22T11:00:02Z — Accepted tracer design recorded

- **State:** build
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted the four-skill implementation scope; implementation remains repository-local and excludes all external business actions.
### 2026-08-22T11:06:40Z — Bounded implementation completed

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** The accepted repository-local package is implemented and focused checks pass; broader verification remains required before treating the Work Object as complete.
### 2026-08-22T11:07:14Z — Closed: The accepted four-skill package is implemented, generated, installed, and verified within scope. Unrelated research-produce-report failures and the absence of real-use outcome evidence are recorded as explicit gaps, not hidden or repaired outside authority.

- **State:** close
- **Status:** closed
- **Actor:** system
- **Rationale:** The accepted four-skill package is implemented, generated, installed, and verified within scope. Unrelated research-produce-report failures and the absence of real-use outcome evidence are recorded as explicit gaps, not hidden or repaired outside authority.
