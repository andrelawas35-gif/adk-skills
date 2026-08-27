---
schema_version: 1
id: 2026-08-22-013
title: Integrate business artifacts (spreadsheets, dashboards, reports, presentations) into the skill portfolio
type: inquiry
status: active
state: explore
consequence: meaningful
sensitivity: ordinary
domain: [business, asset]
created_at: 2026-08-22T11:50:31Z
updated_at: 2026-08-22T13:02:19Z
next_action: Director selects a direction among Round 2 5/6/7 or Round 1 1/2/3; Direction 4 is moot (backing store resolved).











---
## Intent

Explore how the business skills (the four installed, and the portfolio in
`deliverables/2026-08-22-008-comprehensive-business-skill-portfolio.md`)
could produce real business artifacts -- spreadsheets, dashboards, reports,
presentations -- instead of only a Work Object decision record. Grounded in
two facts (Evidence ledger): a full artifact toolset already exists as
installed platform skills (xlsx, pptx, pdf, docx, dataviz), and Work Studio
already has a standalone-artifact pattern (`.work-studio/deliverables/`).
So this is largely a *wiring/governance* question, not a build-from-scratch
one.

Exploration only; directions below diverge on how artifact production
attaches to the skill contracts and how it relates to the backing-store
question (WO `2026-08-22-012`), which is its dependency.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [ ] At least three materially distinct directions generated and presented
- [ ] Director has selected a direction (or explicitly declined to select)
- [ ] The dependency on WO `2026-08-22-012` (backing store) is explicitly
      resolved or sequenced, not left implicit


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
| [system] | skills/core/business-*/SKILL.md | The four business skills currently produce only a Work Object decision record plus structured_output -- no spreadsheet, dashboard, report, or presentation artifact of any kind is produced by any of them today. |
| [system] | available platform skills (docx, pptx, pdf, xlsx, dataviz, theme-factory, brand-guidelines) | A full artifact-production toolset already exists as installed platform skills: xlsx (spreadsheets), pptx (presentations), pdf, docx (reports/documents), dataviz (charts), theme-factory + brand-guidelines (styling). None is currently wired into any Work Studio business skill. 'Integrate artifacts' may therefore be mostly a COMPOSITION/wiring question, not a build-from-scratch one. |
| [system] | .work-studio/deliverables/ (5 existing files); alawas-research-produce-report | Work Studio already has a real standalone-artifact pattern: produce-report writes durable markdown documents to .work-studio/deliverables/<wo-id>-<slug>.md, linked (not duplicated) from the Work Object. This is the existing precedent any artifact-integration model would either extend or diverge from. |
| [system] | references/EVIDENCE-MODEL.md:75 | Governing constraint: any view over Work Objects -- report, summary, graph, dashboard, spreadsheet, deck -- is a read-only projection, never a source. Any integrated artifact must be generated FROM canonical Work Object / structured data, never hand-edited as a parallel source of truth. |
| [gap] | WO 2026-08-22-012 (Neon database, open/explore) | This artifact question and the database question are two layers of one system: artifacts are OUTPUTS, the database/spreadsheet/file is the BACKING STORE those outputs render from. 012's directions (Neon vs SQLite vs flat spreadsheet) largely determine what a dashboard/report here reads FROM. The two Work Objects should resolve in dependency order (store first, or at least jointly), not independently. |
| [decision] | WO 2026-08-22-012 close, 2026-08-22 | Backing store resolved: 2026-08-22-012 closed with Direction 5 (spreadsheet-first, flat files, no database). Artifacts render FROM flat-file/spreadsheet data, not a hosted database. Dependency recorded in 013's success evidence is now resolved. |
| [system] | grep skills/core/business-*/SKILL.md, 2026-08-22 | 15 business skills now installed (11 new beyond the original four: balance-demand-supply-capacity, build-driver-based-plan-and-forecast, design-pricing-and-packaging, direct-project-delivery, formulate-strategy, govern-initiative-portfolio, manage-customer-success, manage-enterprise-risk, manage-liquidity-and-cash-runway, manage-market-intelligence, source-and-govern-suppliers). Grep confirms ALL 15 produce only structured_output (a Work Object decision record) - no spreadsheet, dashboard, report, or deck artifact from any. |
| [gap] | deliverables/2026-08-22-008-comprehensive-business-skill-portfolio.md (registered in 013 Intent) | Portfolio deliverable referenced by 013's Intent is not found at its registered path (Missing Artifact Gap). Artifact mapping in Round 2 is grounded directly from skills/core/business-*/SKILL.md output shapes instead; the deliverable, if it exists elsewhere, remains unread. |
## Open questions

Need director input:

- **Backing-store dependency.** These directions assume a data source to
  render artifacts from. WO `2026-08-22-012` is deciding what that source
  is (Neon / SQLite / flat spreadsheet / none). A dashboard reading from a
  Neon table (012 Direction 6/7) is a different build than one reading from
  flat spreadsheets (012 Direction 5). Which resolves first?
- **Who edits vs. who generates.** EVIDENCE-MODEL's read-only-projection
  rule means artifacts should be *generated*, never hand-edited as a
  parallel truth. But a spreadsheet the director wants to *edit by hand*
  (e.g. tweak forecast assumptions) breaks that rule. Is the spreadsheet an
  input the director edits, or an output the skill generates? These need
  different homes.
- **Presentation styling.** Reports/decks imply a house style. `theme-
  factory` and `brand-guidelines` exist as platform skills but no Work
  Studio brand/theme is defined anywhere. Out of scope for direction
  selection, but real before any deck ships.

## Next move

Awaiting director selection among the four directions below. Each is
grounded in the existing artifact toolset and the deliverables/ precedent
(Evidence ledger), and each states its relationship to the backing-store
question (WO `2026-08-22-012`).

### Direction 1: Thin composition — skills call existing artifact skills, output to deliverables/

- **Core idea**: No new infrastructure. Each business skill, at its output
  step, optionally composes an existing platform skill (xlsx / pptx / pdf /
  docx / dataviz) to render its decision record into the requested artifact,
  written to `.work-studio/deliverables/<wo-id>-<slug>.{xlsx,pptx,pdf}` --
  exactly the pattern `produce-report` already uses for markdown.
- **Distinctness claim**: The only direction adding zero new machinery --
  it reuses both the existing artifact skills and the existing deliverables/
  pattern wholesale. No dependency on the database question at all.
- **Key assumption**: A one-shot generated artifact per Work Object (a deck
  for this decision, a spreadsheet for this analysis) is what's actually
  wanted -- not a living, continuously-updated workbook spanning many Work
  Objects.
- **Smallest test**: Take one real business-assess-financial-decision Work
  Object and hand-run the xlsx skill on its numbers to produce one
  spreadsheet in deliverables/. If that's useful as-is, this direction
  suffices.

### Direction 2: Artifact contract — a shared reference every business skill imports

- **Core idea**: Define one `references/BUSINESS-ARTIFACTS.md` contract
  specifying, per artifact type, what each business skill emits (columns for
  a pipeline spreadsheet, sections for a decision report, slide structure
  for a deck) and its provenance/read-only rules. Every business skill's
  Output section points at it, so artifacts are consistent across the whole
  portfolio (including the 24 planned skills).
- **Distinctness claim**: The only direction that scales to the *portfolio*
  (2026-08-22-008's 24 skills), not just the four installed -- it makes
  artifact production a governed, uniform contract rather than per-skill
  ad hoc composition.
- **Key assumption**: The portfolio actually grows enough that per-skill
  consistency matters -- if only the four current skills ever produce
  artifacts, this contract is overhead over Direction 1.
- **Smallest test**: Draft the contract for just two artifact types
  (pipeline spreadsheet, financial-decision report) and check whether two
  different business skills can point at it without contradiction.

### Direction 3: Live dashboard extension — one dashboard over structured business data

- **Core idea**: Extend the already-built command center (WO
  `2026-08-22-006`) to also read structured business data (from whatever
  store 012 picks) and render an ongoing business dashboard -- pipeline
  health, cash runway, portfolio status -- regenerated on demand alongside
  the Work Object view. Spreadsheets/reports/decks are separate (Direction
  1); this is specifically the *dashboard* half.
- **Distinctness claim**: The only direction producing a *living,
  cross-Work-Object* view rather than per-decision one-shot artifacts --
  and the only one directly dependent on 012's store decision.
- **Key assumption**: Business data worth a standing dashboard actually
  accumulates across many Work Objects -- true for pipeline (many deals),
  weaker for one-off decisions (per 012's evidence).
- **Smallest test**: Add one business section to the command center reading
  a hand-made sample of pipeline rows; see if a standing dashboard tells
  the director something the per-Work-Object view doesn't.

### Direction 4: Do the store first — defer artifacts until 012 resolves

- **Core idea**: Don't decide the artifact layer yet. Resolve WO
  `2026-08-22-012` (backing store) first, because the store decision
  materially changes what every artifact direction here looks like. Once
  the store is known, revisit this Work Object with the option space
  narrowed.
- **Distinctness claim**: The only direction that sequences rather than
  builds -- it treats the dependency (Evidence ledger) as the thing to
  resolve first, avoiding designing artifacts against an undecided source.
- **Key assumption**: The store decision genuinely constrains the artifact
  design enough to be worth waiting for -- true for dashboards (Direction
  3) and living spreadsheets, less true for one-shot generated deliverables
  (Direction 1, which works regardless of store).
- **Smallest test**: None -- this is a sequencing choice. Its only action
  is pausing this Work Object with a dependency link to 012.

## Round 2 — refined against 15 installed skills and the resolved backing store

Round 1's four directions stand as the general framing. Round 2 narrows the
same decision space by two changes since Round 1 (Evidence ledger):

1. **The backing-store dependency is resolved.** WO `2026-08-22-012` closed
   with Direction 5: flat files / spreadsheets, no database. Direction 4
   ("do the store first") is therefore **moot** — the store is no longer an
   open question. Artifacts render from flat-file/spreadsheet data.
2. **The operative scope is now 15 installed skills, not 4.** Eleven new
   business skills are installed; all 15 produce only `structured_output`
   today. The "24 planned skills" from WO 008's portfolio are not installed,
   so the contract question is about the 15 that exist, not a hypothetical 24.

### Per-skill artifact map (grounded in each skill's output shape)

| Skill | Natural artifact(s) | Shape |
|-------|--------------------|-------|
| manage-commercial-pipeline | pipeline spreadsheet + dashboard | spreadsheet + dashboard (recurring — validated by 012's tracer) |
| build-driver-based-plan-and-forecast | driver-based plan .xlsx (drivers → P&L/cash/BS) | spreadsheet |
| manage-liquidity-and-cash-runway | cash-runway .xlsx | spreadsheet |
| design-pricing-and-packaging | pricing model .xlsx | spreadsheet |
| balance-demand-supply-capacity | capacity model .xlsx | spreadsheet |
| plan-workforce-accountability | workforce plan .xlsx | spreadsheet |
| source-and-govern-suppliers | supplier scorecard .xlsx | spreadsheet |
| manage-enterprise-risk | risk register .xlsx + report | spreadsheet + report |
| assess-financial-decision | financial analysis .xlsx + report | spreadsheet + report |
| formulate-strategy | strategy doc + deck (.docx/.pptx) | report/deck |
| manage-market-intelligence | market report + dataviz | report + chart |
| direct-project-delivery | schedule .xlsx + status report | spreadsheet + report |
| improve-operating-process | process map + experiment report | report |
| manage-customer-success | customer-health scorecard/dashboard | dashboard (recurring) |
| govern-initiative-portfolio | portfolio dashboard | dashboard (recurring) |

Pattern: **9 spreadsheet-shaped, 4 report/deck-shaped, 3 dashboard-shaped**
(enterprise-risk and assess-financial overlap spreadsheet + report). The
majority are naturally spreadsheet-shaped — consistent with 012's
spreadsheet-first resolution. Only commercial-pipeline, customer-success, and
initiative-portfolio have genuinely recurring, dashboard-shaped data.

### Direction 5: Spreadsheet-first composition — one-shot per-decision artifacts

- **Core idea**: Each business skill, at its output step, composes the
  existing xlsx skill to write a one-shot spreadsheet to
  `.work-studio/deliverables/<wo-id>-<slug>.xlsx` — the produce-report
  pattern applied to the 9 spreadsheet-shaped skills first. Decks/reports
  (strategy, market-intelligence, project-delivery) stay docx/pptx
  composition. No new machinery, no shared contract yet.
- **Distinctness claim**: The only direction that starts from the majority
  shape (spreadsheets) and defers both the portfolio-wide contract and the
  dashboard to later slices.
- **Key assumption**: One-shot generated spreadsheets per decision are
  actually wanted — not living workbooks spanning decisions.
- **Smallest test**: Take one build-driver-based-plan-and-forecast (or
  commercial-pipeline) output and hand-run the xlsx skill to produce one
  deliverable spreadsheet; check it is useful as-is.

### Direction 6: Artifact contract over the 15 installed skills

- **Core idea**: Define `references/BUSINESS-ARTIFACTS.md` — per artifact
  type, what each business skill emits (columns for pipeline/cash/risk
  spreadsheets, sections for reports, slide structure for decks), plus
  provenance/read-only rules. Every business skill's Output section points
  at it.
- **Distinctness claim**: With 15 installed skills the shared-contract
  overhead is now justified (Round 1 judged it overhead at 4 skills); the
  only direction that makes artifact output uniform across the portfolio.
- **Key assumption**: The 15 skills genuinely share enough artifact shape
  that a contract reduces duplication rather than adding indirection.
- **Smallest test**: Draft the contract for two artifact types (pipeline
  spreadsheet, strategy deck) and check two different skills can point at it
  without contradiction.

### Direction 7: Dashboard extension over flat-file business data

- **Core idea**: Extend the command center (WO 2026-08-22-006) to read
  flat-file/spreadsheet business data and render a standing business
  dashboard — scoped to the three recurring-data skills (commercial-
  pipeline, customer-success, initiative-portfolio). Spreadsheets/reports/
  decks remain the per-decision one-shot path.
- **Distinctness claim**: The only direction producing a living,
  cross-decision view; the only one whose source is the flat-file store 012
  chose. Scoped narrowly because only 3 of 15 skills have recurring data.
- **Key assumption**: A standing dashboard over pipeline/customer/portfolio
  rows tells the director something the per-Work-Object view doesn't.
- **Smallest test**: Add one business section to the command center reading
  a hand-made sample of pipeline rows; see if it adds insight.

### Information gaps surfaced (Round 2)

- **Who edits vs. who generates** (still open): EVIDENCE-MODEL's
  read-only-projection rule says artifacts are generated, never hand-edited
  as a parallel truth. But 012's resolution implies the director may
  hand-edit forecast assumptions in a pipeline spreadsheet. These need
  different homes (input vs output). Needs director decision.
- **Deck/report styling**: theme-factory + brand-guidelines exist as
  platform skills but no studio brand/theme is defined. Real before any deck
  ships; out of scope for direction selection.
- **Portfolio deliverable**: `deliverables/2026-08-22-008-...` is missing
  (gap); the artifact map above is grounded in the installed skills
  directly.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T11:50:43Z — Created

- **State:** notice
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Director invoked develop-idea referring to deliverables/2026-08-22-008-comprehensive-business-skill-portfolio.md, asking how to integrate spreadsheets, dashboards, reporting, presentations, and other business artifacts into the skills. Broader than the Neon-database WO 2026-08-22-012 (which concerns a backing STORE); this concerns the output ARTIFACT layer across the whole business portfolio.
### 2026-08-22T11:50:43Z — Activated for direction generation

- **State:** explore
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Type inquiry, explore state satisfies develop-idea's precondition.
### 2026-08-22T13:02:19Z — Next slice run: 15-skill artifact map; backing-store dependency resolved

- **State:** explore
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** Ran the next exploration slice: mapped natural artifacts for all 15 installed business skills; resolved 013's dependency on 012 (backing store = flat files/spreadsheets, no database, Direction 4 moot); added Round 2 directions 5-7.
