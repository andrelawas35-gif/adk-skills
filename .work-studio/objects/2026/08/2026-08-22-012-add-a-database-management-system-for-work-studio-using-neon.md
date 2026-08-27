---
schema_version: 1
id: 2026-08-22-012
title: Add a database management system for Work Studio using Neon
type: inquiry
status: closed
state: close
consequence: high
sensitivity: ordinary
domain: [engineering, architecture]
created_at: 2026-08-22T11:43:13Z
updated_at: 2026-08-22T12:59:16Z
next_action: Director completes the hand-test judgment on fixtures/pipeline-tracer.xlsx (3 sheets, 4 hypothetical deals): record where the spreadsheet stays clean and where it strains, as evidence; clean test closes/advances the inquiry, awkward test reopens Directions 7/8 via pressure-test-decision.






















---
## Intent

Explore what role a database (specifically Neon, a hosted Postgres) could
play in Work Studio, currently a flat-Markdown-file, CLI-mediated,
git-tracked system with no database of any kind for canonical state.
Genuinely open: this could mean anything from a narrow read-only mirror for
querying, to replacing the canonical store outright -- a decision ADR 0025
explicitly names as hard-to-reverse and warns against accepting on
assertion rather than demonstrated need.

This is exploration only. No direction is selected; four are recorded below
for the director to choose from, diverging along the one axis that actually
matters here: how much of the existing markdown-canonical-CLI model a given
direction disturbs.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [ ] At least three materially distinct directions generated and presented
- [ ] Director has selected a direction (or explicitly declined to select)
- [ ] The consequence-4 (canonical-store-replacement) direction, if
      selected, is explicitly flagged as needing pressure-test-decision
      before any design work — not routed straight to design-tracer-bullet


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

<!-- BUILD GATE (high consequence): requires a decision record
     with decision_type: decision before transitioning to build state.
     Example entry below. -->
### Decision 1 — Direction 5 selected: spreadsheet-first, no database

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Direction selection for WO 2026-08-22-012 — spreadsheet + dashboard capability for the four business skills |
| **Authorization** | director (human), confirmed 2026-08-22 |
| **Confidence** | high for 3 of 4 skills (single-instance decision documents); medium for commercial-pipeline (relational shape untested) — basis: skills/core/business-*/SKILL.md inspection |
| **Actor** | human (director) |
| **Revisit trigger** | smallest hand-test (3–4 deals across pipeline stages in one spreadsheet) gets awkward, or a stated cross-machine/sharing need emerges |
| **Rationale** | Three of four business skills are single-instance decision documents, not ongoing record sets; zero existing spreadsheet/dashboard/DB code (re-verified by grep 2026-08-22); Local-first is a named studio value (CONTEXT.md); cheapest correct first step. Database directions deferred pending the smallest test. |

- **Branch chosen**: Direction 5 — build spreadsheet + dashboard capability on flat files (e.g. `pipeline.xlsx` per skill); no database added.
- **Alternatives considered**: Direction 7 (Neon for commercial-pipeline only) — matches data shape but premise untested; Direction 8 (local SQLite) — local-first but still a DB for data that may fit a sheet; Direction 6 (Neon for all four) — ranked lowest on evidence, highest on cost; Direction 3 (canonical-store replacement) — hard-to-reverse per ADR 0025, explicitly not selected.
- **Trade-offs accepted**: Betting commercial-pipeline's relational shape fits a spreadsheet; any database revisit deferred until the smallest test or a stated cross-machine/sharing need.
- **Edge cases noted**: Stage-transition history and forecast math may get awkward in a sheet; spreadsheets remain local-only (no cross-machine access).

### Decision 2 — Tracer bullet accepted: 3-sheet pipeline-tracer.xlsx hand-test

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Direction 5 smallest test — build and judge the spreadsheet hand-test for commercial-pipeline |
| **Authorization** | director (human), confirmed 2026-08-22 |
| **Confidence** | medium — the assumption (spreadsheet suffices for pipeline) is untested until the workbook is completed and judged |
| **Actor** | human (director) |
| **Revisit trigger** | completed workbook shows stage history requiring duplicate rows, or forecast math not expressible in formulas |
| **Rationale** | The accepted direction (Decision 1) names this hand-test as the smallest discriminating evidence; the design was pressure-tested and accepted. |

- **Riskiest assumption**: A single flat spreadsheet can represent 3–4 pipeline deals with stage history and a changing forecast, and produce the aggregate views, without duplicate-row workarounds or manual forecast math.
- **Bounded path**: one throwaway workbook `fixtures/pipeline-tracer.xlsx` — Deals (one row per deal), Stage history (one row per transition), Forecast (formula-based aggregates), with 3–4 clearly-labeled hypothetical deals.
- **Failure behavior**: if stage history forces duplicated deal rows or forecast totals cannot be expressed as formulas, record the finding as evidence and reopen the database decision (Directions 7/8); do not claim the spreadsheet suffices from an unrun plan.
- **Observability**: a completed workbook where each deal's history is readable transition-by-transition and forecast totals are checkable by formula.
- **Non-goals**: no Neon/SQLite/dashboard provisioning, no command-center integration, no real business data, no library installs.
- **Rollback**: delete the single workbook; no durable state.
- **Exit criteria**: clean → confirm spreadsheet-first (close inquiry or spawn successor); awkward → route to pressure-test-decision to reopen Directions 7/8.

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | grep across whole repo for neon/postgres/psycopg/sqlalchemy | Zero existing references to Neon, Postgres, or any SQL database anywhere in this repo. This is a genuinely new capability, not an extension of anything already started. |
| [system] | docs/adr/0025-canonical-runtime-truth-boundary-and-single-writer-rule.md lines 23, 89, 99-101 | The canonical truth boundary (what counts as canonical Work Object state, who may write it) is explicitly named as expensive/hard-to-reverse; storage TECHNOLOGY (currently SQLite for runtime checkpoints only) is deliberately kept separate and reversible. The ADR explicitly warns against accepting infrastructure 'on a plan's assertion' rather than demonstrated load: it names four prior Work Objects that did exactly that and were later declined. |
| [system] | runtime/graph.py:9-10,26,35; runtime/checkpoints/ | The only existing database usage anywhere is SQLite (SqliteSaver) for ephemeral LangGraph checkpoints -- gitignored, non-canonical, ADR-scoped as ephemeral runtime plane only. Canonical Work Object state remains flat Markdown files under .work-studio/objects/, mutated only via the ws CLI (append-only History, optimistic concurrency). |
| [gap] | WO 2026-08-21-005 (multi-repo registry, currently open/verify) | A live, concrete candidate consumer already exists: WO 2026-08-21-005 plans a flat .work-studio/repos.yaml file to register multiple target repos -- a real place a database COULD replace a flat file, if that WO's actual need (small, single-user, low query complexity) justified it. No stated need for SQL querying, concurrent multi-writer access, or hosted infrastructure has been identified anywhere yet. |
| [system] | skills/core/business-*/SKILL.md | Director named the real consumer: the four business skills (assess-financial-decision, improve-operating-process, manage-commercial-pipeline, plan-workforce-accountability). Checked each: all four currently store only a one-off summary inside a single Work Object -- no structured, ongoing record-keeping across multiple decisions/deals/cycles exists anywhere. business-manage-commercial-pipeline is the only one whose real-world subject (deals across pipeline stages) is naturally repeated/relational data; the other three (financial-decision, operating-process, workforce-accountability) are each single-instance decision documents, not ongoing record sets. No spreadsheet or dashboard capability is wired into any of them today. |
| [decision] | director conversation | Director accepted Direction 5 (spreadsheet-first, no database) on 2026-08-22; alternatives 6/7/8 ranked below it, revisit trigger recorded in Decision 1. |
| [testimony] | director conversation (Round 2) | Director resolved the consumer as the four business skills (assess-financial-decision, improve-operating-process, manage-commercial-pipeline, plan-workforce-accountability) wanting spreadsheet and dashboard capability. |
| [decision] | director conversation | Director accepted the tracer-bullet design for the Direction 5 smallest test (3-sheet pipeline-tracer.xlsx hand-test) on 2026-08-22; recorded as Decision 2. |
| [system] | implementation of Decision 2, 2026-08-22 (stdlib-only generator) | Built fixtures/pipeline-tracer.xlsx: sheets Deals / Stage history / Forecast; 4 hypothetical deals (DEAL-001..004); 8 per-deal formulas (qualified_value, weighted_value) + 7 forecast formulas (gross, qualified, weighted point, low/high band, concentration, stale count). Verified: valid xlsx zip, all 8 XML parts well-formed; no library installs. |
| [testimony] | director judgment, 2026-08-22 | Director judged the Direction 5 hand-test clean: fixtures/pipeline-tracer.xlsx represents 4 deals across stages without duplicate-row workarounds, and the forecast math is formula-expressible. Exit criteria met - spreadsheet-first confirmed, no database needed now. |
## Open questions

Not discoverable from the workspace — need director input:

- **What actual problem is this solving?** No stated need for SQL querying,
  concurrent multi-writer access, cross-machine sync, or hosted
  infrastructure has surfaced anywhere in this workspace. "Add a database"
  as a standalone goal, with no named consumer, is exactly the pattern
  ADR 0025 names four prior Work Objects for and says was later declined
  each time.
- **Is there a specific consumer in mind?** The command center (WO
  `2026-08-22-006`) and the multi-repo registry (WO `2026-08-21-005`) are
  the two closest candidates already in flight, both currently designed
  around flat files. If Neon is meant to serve one of these, the smallest
  test differs sharply from a generic "DB management system."
- **Local-first tension.** `CONTEXT.md` defines "Local-first" as a named
  studio value ("records stored on the user's own machine by default; sync
  and sharing require explicit later choices"). A hosted Postgres service
  is a real departure from that default — worth naming explicitly, not
  discovering later.

## Next move

Awaiting director selection among the four directions below. Each is
grounded in the real absence of any existing database code, and in ADR
0025's explicit governance boundary (Evidence ledger above).

### Direction 1: Read-only mirror for querying (canonical stays Markdown)

- **Core idea**: Sync `.work-studio/objects/**` into Neon as a queryable
  read-only index — regenerated on demand or on a schedule, the same
  read-only-projection pattern EVIDENCE-MODEL.md already establishes for
  any dashboard/report/graph. Canonical state, the CLI, and git history are
  completely untouched.
- **Distinctness claim**: The only direction that changes nothing about how
  Work Objects are written, mutated, or governed — pure additive
  read-side capability.
- **Key assumption**: The command center (or a future feature) actually
  needs SQL query power that grep/glob over Markdown files cannot provide —
  not yet established anywhere.
- **Smallest test**: Write one Work Object's frontmatter to a scratch Neon
  table by hand and run one real query against it (e.g. "all Work Objects
  with consequence: high and status: active") that would be awkward with
  today's `ws` CLI/grep tooling.

### Direction 2: Targeted store for one named consumer, not a general "DB"

- **Core idea**: Instead of "add a database" as a standalone goal, give
  Neon to one specific, already-identified need — e.g. WO
  `2026-08-21-005`'s multi-repo registry, replacing its planned
  `.work-studio/repos.yaml` with a Neon table if that WO's actual
  requirements (concurrent access across repos, structured queries) turn
  out to justify it.
- **Distinctness claim**: The only direction with a named, real consumer
  from day one — success is defined by that consumer's need, not by "the
  database exists."
- **Key assumption**: WO `2026-08-21-005`'s registry actually needs more
  than a flat YAML file can give it — not yet tested; that WO's own
  smallest test doesn't currently mention a database at all.
- **Smallest test**: Re-open WO `2026-08-21-005`'s design and ask whether
  its accepted registry design has a concrete requirement a flat file
  can't satisfy. If none exists, this direction has no target yet either.

### Direction 3: Canonical-store replacement (Markdown → Postgres)

- **Core idea**: Replace `.work-studio/objects/**/*.md` as the canonical
  Work Object store with Neon tables — the `ws` CLI would read/write
  Postgres instead of files, and Markdown files (if kept at all) would
  become a generated, read-only export.
- **Distinctness claim**: The only direction that touches the canonical
  truth boundary ADR 0025 explicitly calls hard-to-reverse — every other
  direction is additive or narrowly scoped.
- **Key assumption**: The current file-based, git-tracked, append-only
  model is genuinely insufficient for real use — no evidence of this
  anywhere; ADR 0025 explicitly warns this exact move was accepted on
  assertion, not evidence, in four prior instances, and was later declined
  each time.
- **Smallest test**: This is disproportionate to test cheaply — by design,
  a canonical-store change isn't reversible the way the other directions
  are. If selected, route to `pressure-test-decision` before any design
  work, not directly to `design-tracer-bullet` (see Success evidence).

### Direction 4: Do nothing yet — name the real trigger condition instead

- **Core idea**: Don't build anything now. Record what concrete signal
  (e.g. grep/CLI queries becoming a genuine bottleneck, a real multi-writer
  need emerging, the command center needing cross-workspace aggregation)
  would justify revisiting this, and close the idea until that signal
  actually appears.
- **Distinctness claim**: The only direction costing nothing today —
  directly mirrors this session's own established pattern (the epistemic-
  loop Work Object, `2026-08-22-001`) of rejecting infrastructure that adds
  no demonstrated capability yet.
- **Key assumption**: The idea is speculative rather than triggered by a
  real, current friction — consistent with the evidence (zero existing DB
  code, no named consumer), but only the director can confirm this against
  what actually prompted the idea.
- **Smallest test**: None needed — this direction is the absence of a
  build. Its only action is recording the revisit trigger.

## Round 2 — refined against the named consumer (business skills, spreadsheets, dashboards)

Director resolved Open question 2: the consumer is the four business
skills, wanting spreadsheet and dashboard capability. This is new evidence
(Evidence ledger above), not a discarded round — Directions 1-4 above still
stand as the general-purpose framing; these four are the same decision
space narrowed to the actual named need.

### Direction 5: Spreadsheet-first, no database at all

- **Core idea**: Each business skill appends structured rows to its own
  spreadsheet (e.g. `pipeline.xlsx`, `financial-decisions.xlsx`) instead of
  only a Work Object summary. The command center's existing pattern (WO
  `2026-08-22-006` — read `.work-studio/`, render static HTML, regenerate
  on demand) extends to read these spreadsheets and render a dashboard.
- **Distinctness claim**: The only direction with zero new infrastructure —
  no Neon account, no hosted service, no network dependency. Fully
  consistent with `CONTEXT.md`'s "Local-first" value.
- **Key assumption**: A spreadsheet is sufficient structure for what these
  four skills actually need to track — true today for financial-decision/
  operating-process/workforce-accountability (single-instance documents),
  more doubtful for commercial-pipeline (many deals, many stages, real
  relational shape).
- **Smallest test**: Take one real business-manage-commercial-pipeline
  Work Object's output and try to represent 3-4 hypothetical deals across
  stages in a single spreadsheet by hand. If it stays clean, spreadsheets
  suffice; if stage-transition history or cross-deal queries get awkward,
  that's evidence for Direction 6/7 instead.

### Direction 6: Neon-backed, spreadsheet and dashboard as generated views

- **Core idea**: All four business skills write structured rows to Neon
  tables (one per skill, or one shared schema with a `skill` column).
  Spreadsheets (via an XLSX export) and the dashboard are both *generated
  views* over Neon — always consistent with each other, never hand-edited
  separately.
- **Distinctness claim**: The only direction giving genuinely live,
  multi-view consistency (spreadsheet and dashboard never drift apart) —
  at the cost of real new infrastructure (a hosted Postgres account,
  credentials, network dependency) for all four skills, not just the one
  that clearly needs it.
- **Key assumption**: All four skills benefit equally from a database, not
  just commercial-pipeline — contradicted by the evidence above (three of
  four are single-instance documents, not repeated records).
- **Smallest test**: Same as Direction 1 — one real query against one
  scratch Neon table that a spreadsheet/grep genuinely couldn't answer
  cleanly.

### Direction 7: Neon for commercial-pipeline only, spreadsheets for the rest

- **Core idea**: Give Neon only to `business-manage-commercial-pipeline` —
  the one skill whose real-world subject (deals across stages, over time)
  is genuinely relational. The other three business skills get the
  spreadsheet-first treatment from Direction 5. One shared dashboard reads
  both sources.
- **Distinctness claim**: The only direction matching infrastructure to
  each skill's actual data shape instead of applying one solution
  uniformly across all four.
- **Key assumption**: Commercial-pipeline's data genuinely outgrows a
  spreadsheet (multiple deals, stage-transition history, forecasting
  queries) in a way the other three skills' one-off decisions do not — the
  most evidence-grounded assumption of the three DB-touching directions,
  but still untested against real pipeline volume.
- **Smallest test**: Same hand-test as Direction 5, but specifically for
  commercial-pipeline: if 3-4 hypothetical deals in a spreadsheet start
  needing awkward workarounds (duplicate rows for stage history, manual
  forecast math), that confirms this direction's premise directly.

### Direction 8: Local SQLite instead of hosted Neon

- **Core idea**: Same structured-data-plus-generated-views idea as
  Direction 6 or 7, but using SQLite (already a real dependency in this
  repo, for LangGraph checkpoints) instead of a hosted Postgres service.
- **Distinctness claim**: The only DB-backed direction preserving
  "local-first" — no account, no credentials, no network dependency — at
  the cost of no cross-machine access if that ever matters.
- **Key assumption**: Cross-machine/cross-device access to business data is
  not currently needed — true today (single-user, single-machine studio),
  but worth naming since it's the actual trade-off Neon would buy over
  this direction.
- **Smallest test**: Same relational-need test as Direction 5/7, plus one
  explicit question: does the director ever need this data from a second
  machine or wants to share it with someone else? If genuinely no, SQLite
  gets everything Neon offers here at zero hosting cost or local-first
  compromise.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T11:43:25Z — Created

- **State:** notice
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Director invoked alawas-thinking-develop-idea directly: add a database management system for Work Studio, utilizing Neon. Rough idea, genuinely ambiguous (what role would Neon play relative to the existing markdown-canonical-state model?) -- develop-idea's precondition.
### 2026-08-22T11:43:25Z — Activated for direction generation

- **State:** explore
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Type inquiry, explore state satisfies develop-idea's precondition.
### 2026-08-22T12:41:42Z — Authority: AUTH-002 record Decision 1 (Direction 5) and transition explore to design

- **State:** explore
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** High-consequence object; director confirmed the specific write set on 2026-08-22 ('route to design'). Scope: WO 2026-08-22-012 decision record + evidence rows + state transition. Constraints: none.
### 2026-08-22T12:41:47Z — Decision recorded: Direction 5 selected - spreadsheet-first, no database

- **State:** explore
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** Director accepted the pressure-test recommendation; alternatives and revisit trigger recorded in Decision 1.
### 2026-08-22T12:41:52Z — State to design for smallest test

- **State:** design
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** Direction 5 selected; next step is the spreadsheet hand-test for commercial-pipeline.
### 2026-08-22T12:47:02Z — Authority: AUTH-003 record accepted design (Decision 2) and implement the Direction 5 tracer bullet

- **State:** design
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** High-consequence object; director confirmed the specific write set on 2026-08-22 ('record and implement'). Scope: record Decision 2 + evidence + transition to build, then build fixtures/pipeline-tracer.xlsx. Constraints: stdlib only, no library installs, no real business data.
### 2026-08-22T12:47:07Z — Design accepted and recorded: Direction 5 tracer bullet

- **State:** design
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** Director accepted the 3-sheet pipeline-tracer.xlsx hand-test design; assumption, bounded path, safeguards, exit criteria, and rollback recorded in Decision 2.
### 2026-08-22T12:47:13Z — State to build for tracer implementation

- **State:** build
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** Tracer bullet accepted (Decision 2); building the bounded workbook artifact now.
### 2026-08-22T12:54:39Z — Tracer bullet implemented and verified

- **State:** build
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** Built and verified fixtures/pipeline-tracer.xlsx (stdlib-only, no installs) per Decision 2; implementation evidence appended.
### 2026-08-22T12:56:47Z — Hand-test verdict: clean - Direction 5 confirmed

- **State:** build
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** Director judged the pipeline-tracer.xlsx hand-test clean; spreadsheet-first holds and no database is needed now. Verdict recorded as testimony; Decision 2 exit criteria met.
### 2026-08-22T12:59:10Z — State to close: inquiry resolved

- **State:** close
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** Hand-test clean; Direction 5 confirmed; no database; successor 2026-08-22-013 tracks the artifact build.
### 2026-08-22T12:59:16Z — Closed: Inquiry resolved: Direction 5 (spreadsheet-first, no database) confirmed by clean hand-test (fixtures/pipeline-tracer.xlsx). Successor 2026-08-22-013 tracks the spreadsheet/artifact-capability build. Revisit trigger: spreadsheet representation gets awkward at real volume, or a cross-machine/sharing need emerges.

- **State:** close
- **Status:** closed
- **Actor:** system
- **Rationale:** Inquiry resolved: Direction 5 (spreadsheet-first, no database) confirmed by clean hand-test (fixtures/pipeline-tracer.xlsx). Successor 2026-08-22-013 tracks the spreadsheet/artifact-capability build. Revisit trigger: spreadsheet representation gets awkward at real volume, or a cross-machine/sharing need emerges.
