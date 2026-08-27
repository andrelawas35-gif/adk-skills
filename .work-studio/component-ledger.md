# Component Ledger

<!--
  Canonical artifact accepted by ADR 0014 and owned by `track-components`.

  A derived index of realized capabilities (components) this project has shipped,
  each grillable toward its best-case. Entries point at where the component lives;
  the component's truth stays in code/ADRs. See WO 2026-07-18-001 for the design.

  Entry schema: status; component kind; governance domain; location(s);
  built-by Work Object(s); declared edges;
  applicable dimensions; owning skill/profile; last-grilled-SHA;
  Option-B-refined best-case anchor; status rationale/findings.
  Status values: active | settled | needs-regrill | retired. Entries are
  pointers, not component copies; retired entries are preserved, never deleted.
  Component kind values: skill | protocol | runtime | tooling | artifact-schema |
  integration. Governance domain values: business | design | engineering |
  governance | operations | production | research | thinking | cross-cutting. COMP-001 through
  COMP-024 are grandfathered legacy records; all new entries require both fields.
-->

## COMP-001 — Grilling engine (Agreement Loop)

- **status:** settled
- **location(s):** `references/AGREEMENT-LOOP.md` (canonical; copied into every skill's `references/` by `tools/generate-adapters.py`)
- **built-by Work Object(s):** pre-ledger backfill; recent shaping in WO `2026-07-16-004` (two-tier lenses); resolved in WO `2026-07-27-003`
- **depends-on:** none declared
- **depended-on-by:** COMP-002 through COMP-044 (every skill's Grilling Session plus the business operating pipeline; widest blast radius)
- **applicable dimensions:** personal fit, artifact value, novelty yield (recovery quality deferred — engine-level, not outcome-level)
- **owning skill/profile:** all skill profiles via `references/SKILL-AWARE-GRILLING.md`
- **last-grilled-SHA:** `0de476b`
- **best-case anchor:** Option-B-refined (WO 2026-07-18-001, 2026-07-18T05:00:00Z) — settled = no surviving finding against the applicable dimensions; auto-reopen on git-drift since `last-grilled-SHA`, owning-skill version change, or contrary govern-scorecards outcome evidence. No standing scorecard artifact.
- **status rationale / findings:** Re-grilled and re-stamped to HEAD (`0de476b`) on 2026-08-22 under the repair authorized after WO 2026-08-22-010. Drift added director-owned convergence authority and plain-language requirements; these strengthen personal fit, artifact value, and novelty-yield safeguards. No surviving finding; no component contract removal or dependent cascade required.
- **first grilled:** 2026-07-18 (tracer pass, WO 2026-07-18-001)
- **open findings:** none — all 4 findings resolved in WO `2026-07-27-003`

### Grilling pass — 2026-07-18 (against Grilling Profile + inline criteria)

- **F1 [artifact value / HIGH]** `AGREEMENT-LOOP.md:103` (*"Ask exactly one decision-bearing question and wait"*) vs `:129` (*"no numerical question cap: three, 200, or more turns are valid"*): the doc never states that the one-question limit is **per turn** while continuity is **per session**. A reader can read "continuous Grilling Session" as "many questions at once." This ambiguity **actively misled in this very session** — lived evidence, not hypothetical.
  - **Resolution (WO 2026-07-27-003):** `### Mode` subsection added to Decision Frontier defining `serial-depth` (per-turn, single-branch) and `breadth-sweep` (per-turn, rotating branches). Branch-rotation clause in turn contract clarifies "last answer" refers to the branch being rotated to. Cadence is now explicit per mode.

- **F2 [personal fit / HIGH]** The engine encodes only **depth-first serial** grilling. It has no **breadth/sweep mode** for covering many independent branches, which is exactly the coverage the component-sweep needs — the engine can't yet express the behavior the project it governs requires.
  - **Resolution (WO 2026-07-27-003):** `breadth-sweep` mode added alongside existing `serial-depth` default. Mode set by conductor at invocation time. Durable continuity template updated to list multiple active branches.

- **F3 [novelty yield / MED]** `:24` "*`do recommended` accepts only the recommendation currently in focus*" leaves **"in focus" undefined** when multiple recommendations were presented in one turn; caused real friction this session.
  - **Resolution (WO 2026-07-27-003):** Branch-rotation clause in turn contract names the active branch explicitly. In breadth-sweep mode, "in focus" is the branch named in the current question.

- **F4 [artifact value / MED]** Convergence (`:176` Coverage Proof) asserts branch-map completeness but gives **no test for whether the branch map is actually complete** — "no remaining question is likely to change the recommendation" is unfalsifiable as written.
  - **Resolution (WO 2026-07-27-003):** Coverage Proof replaced with **Convergence Checklist** — 4 falsifiable conditions: branch inventory with disposition, counterexample test, changed-condition trigger, and zero open branches required.

- **Verdict:** SETTLED. All 4 findings resolved by WO `2026-07-27-003`. Auto-reopen on git-drift since SHA `57d0412`, owning-skill version change, or contrary govern-scorecards outcome evidence.

## Backfilled components

The entries below are durable pre-ledger capabilities. They have not yet been
grilled under this mechanism, so they are `active` with
`last-grilled-SHA: not-yet-grilled`. Their canonical core locations remain the
source of truth; generated adapters are deliberately not listed.

## COMP-002 — Work Object conductor

- **status:** active
- **location(s):** `skills/core/governance-conduct-work-object/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001
- **depended-on-by:** COMP-003 through COMP-044
- **applicable dimensions:** recovery quality, artifact value, novelty yield
- **owning skill/profile:** `governance-conduct-work-object`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-003 — Decision pressure testing

- **status:** active
- **location(s):** `skills/core/thinking-pressure-test-decision/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** none declared
- **applicable dimensions:** personal fit, artifact value, novelty yield
- **owning skill/profile:** `thinking-pressure-test-decision`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-004 — Tracer-bullet design

- **status:** active
- **location(s):** `skills/core/design-design-tracer-bullet/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-005
- **applicable dimensions:** recovery quality, artifact value, novelty yield
- **owning skill/profile:** `design-design-tracer-bullet`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-005 — Bounded implementation

- **status:** active
- **location(s):** `skills/core/engineering-implement-bounded-change/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002, COMP-004
- **depended-on-by:** COMP-006
- **applicable dimensions:** recovery quality, artifact value, novelty yield
- **owning skill/profile:** `engineering-implement-bounded-change`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-006 — Release-evidence verification

- **status:** active
- **location(s):** `skills/core/engineering-verify-release-evidence/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002, COMP-005
- **depended-on-by:** COMP-007
- **applicable dimensions:** recovery quality, artifact value
- **owning skill/profile:** `engineering-verify-release-evidence`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-007 — Deployment with recovery

- **status:** active
- **location(s):** `skills/core/operations-deploy-with-recovery/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002, COMP-006
- **depended-on-by:** none declared
- **applicable dimensions:** recovery quality, artifact value
- **owning skill/profile:** `operations-deploy-with-recovery`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-008 — Outcome review and adaptation

- **status:** active
- **location(s):** `skills/core/governance-review-outcome-and-adapt/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-011, COMP-012
- **applicable dimensions:** recovery quality, personal fit, artifact value, novelty yield
- **owning skill/profile:** `governance-review-outcome-and-adapt`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-009 — Live-question investigation

- **status:** active
- **location(s):** `skills/core/research-investigate-live-question/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** none declared
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `research-investigate-live-question`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-010 — Production incident diagnosis

- **status:** active
- **location(s):** `skills/core/operations-diagnose-production-incident/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** none declared
- **applicable dimensions:** recovery quality, artifact value
- **owning skill/profile:** `operations-diagnose-production-incident`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-011 — Working-method governance

- **status:** active
- **location(s):** `skills/core/governance-maintain-working-method/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002, COMP-008
- **depended-on-by:** none declared
- **applicable dimensions:** personal fit, artifact value, novelty yield
- **owning skill/profile:** `governance-maintain-working-method`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-012 — Outcome scorecard governance

- **status:** active
- **location(s):** `skills/core/governance-govern-scorecards/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002, COMP-008
- **depended-on-by:** COMP-013, COMP-014
- **applicable dimensions:** recovery quality, personal fit, artifact value, novelty yield
- **owning skill/profile:** `governance-govern-scorecards`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-013 — Signal-to-work routing

- **status:** active
- **location(s):** `skills/core/thinking-turn-signal-into-work/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** none declared
- **applicable dimensions:** personal fit, artifact value, novelty yield
- **owning skill/profile:** `thinking-turn-signal-into-work`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-014 — Component tracking

- **status:** active
- **location(s):** `skills/core/design-track-components/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002, COMP-012
- **depended-on-by:** none declared
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `design-track-components`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## Design skills (Phase 1 — contract shells)

The entries below are the 9 design skill contract shells created in WO
`2026-07-22-006`. They are shells (structure and contracts defined, workflow
not yet implemented) and enter the ledger as `active` with `not-yet-grilled`.

## COMP-015 — Product interface audit

- **status:** active
- **location(s):** `skills/core/design-audit-product-interface/SKILL.md`
- **built-by Work Object(s):** `2026-07-22-006`, `2026-07-23-002`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-016, COMP-022
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `design-audit-product-interface`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** Contract amended per Grilling Session 13 Phase 1; Figma references removed, host→target project terminology. Pending implementation and first grilling pass.

## COMP-016 — Design foundation (token audit)

- **status:** active
- **location(s):** `skills/core/design-build-design-foundation/SKILL.md`
- **built-by Work Object(s):** `2026-07-22-006`, `2026-07-23-002`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-022
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `design-build-design-foundation`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** Contract amended per Grilling Session 13 Phase 1; Figma sync references removed, host→target project terminology. Pending implementation and first grilling pass.

## COMP-017 — User flow modeling

- **status:** retired
- **location(s):** removed from canonical skill set
- **built-by Work Object(s):** `2026-07-22-006`, `2026-07-23-002`
- **depends-on:** COMP-001, COMP-002, COMP-015
- **depended-on-by:** none (downstream deps also deferred)
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `model-user-flow`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** n/a (deferred)
- **status rationale / findings:** Deferred per Grilling Session 13 DEC-A11: all structure emerges from conversation. Revisit trigger: project complexity requires upfront flow planning.

## COMP-018 — Interface architecture definition

- **status:** retired
- **location(s):** removed from canonical skill set
- **built-by Work Object(s):** `2026-07-22-006`, `2026-07-23-002`
- **depends-on:** COMP-001, COMP-002, COMP-015, COMP-017
- **depended-on-by:** none (downstream deps also deferred)
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `define-interface-architecture`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** n/a (deferred)
- **status rationale / findings:** Deferred per Grilling Session 13 DEC-A11: all structure emerges from conversation. Revisit trigger: project complexity requires upfront architectural planning.

## COMP-019 — Interface specification definition

- **status:** retired
- **location(s):** removed from canonical skill set
- **built-by Work Object(s):** `2026-07-22-006`, `2026-07-23-002`
- **depends-on:** COMP-001, COMP-002, COMP-016, COMP-018
- **depended-on-by:** none (downstream deps also deferred)
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `define-interface-specification`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** n/a (deferred)
- **status rationale / findings:** Deferred per Grilling Session 13 DEC-A11/DEC-A13: specs extracted after the fact, not authored upfront. Revisit trigger: user needs to communicate design intent before implementation.

## COMP-020 — Figma rendering (governed Figwright wrapper)

- **status:** retired
- **location(s):** removed from canonical skill set
- **built-by Work Object(s):** `2026-07-22-006`, `2026-07-23-002`
- **depends-on:** COMP-001, COMP-002, COMP-019, COMP-021
- **depended-on-by:** none
- **applicable dimensions:** recovery quality, artifact value
- **owning skill/profile:** `render-to-figma`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** n/a (deferred)
- **status rationale / findings:** Deferred per Grilling Session 13 DEC-A5: Figma never used. Revisit trigger: collaboration with a designer who uses Figma.

## COMP-021 — Design-to-code connection (component registry)

- **status:** retired
- **location(s):** removed from canonical skill set
- **built-by Work Object(s):** `2026-07-22-006`, `2026-07-23-002`
- **depends-on:** COMP-001, COMP-002, COMP-015
- **depended-on-by:** none
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `connect-design-to-code`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** n/a (deferred)
- **status rationale / findings:** Deferred per Grilling Session 13 DEC-A5: no Figma component mapping needed. Revisit trigger: external design tool integration requires component mapping.

## COMP-022 — Design direction application (creative authority loop)

- **status:** active
- **location(s):** `skills/core/design-apply-design-direction/SKILL.md`
- **built-by Work Object(s):** `2026-07-22-006`, `2026-07-23-002`
- **depends-on:** COMP-001, COMP-002, COMP-015, COMP-016
- **depended-on-by:** COMP-023
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `design-apply-design-direction`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** Contract rewritten per Grilling Session 13 Phase 1; changed from revision-manifest producer to propose/confirm/execute creative authority loop. Now writes code after confirmation (meaningful consequence). Pending implementation and first grilling pass.

## COMP-023 — Design implementation verification

- **status:** active
- **location(s):** `skills/core/design-verify-design-implementation/SKILL.md`
- **built-by Work Object(s):** `2026-07-22-006`, `2026-07-23-002`
- **depends-on:** COMP-001, COMP-002, COMP-022
- **depended-on-by:** none declared
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `design-verify-design-implementation`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** Renamed from verify-design-code-parity per Grilling Session 13 Phase 1; contract rewritten for browser-only verification against confirmed proposals (no Figma parity, no specification parity). Pending implementation and first grilling pass.

## COMP-024 — Divergent idea development

- **status:** active
- **location(s):** `skills/core/thinking-develop-idea/SKILL.md`
- **built-by Work Object(s):** `2026-07-26-002`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** none declared
- **applicable dimensions:** personal fit, artifact value, novelty yield
- **owning skill/profile:** `thinking-develop-idea`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** First divergent exploration capability in the system. Skill contract created from Idea Development Grilling Session (17 decisions). Pending first tracer bullet run and grilling pass.

## Business management skills (governed components)

These accepted business capabilities use the canonical component-governance
taxonomy introduced by WO `2026-08-22-010`.

## COMP-025 — Commercial pipeline management

- **status:** active
- **component kind:** skill
- **governance domain:** business
- **location(s):** `skills/core/business-manage-commercial-pipeline/SKILL.md`
- **built-by Work Object(s):** `2026-08-22-004`, governed by `2026-08-22-010`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-036
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `business-manage-commercial-pipeline`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** pending first governed grilling pass
- **status rationale / findings:** Accepted business capability; registered with explicit business governance.

## COMP-026 — Operating process improvement

- **status:** active
- **component kind:** skill
- **governance domain:** business
- **location(s):** `skills/core/business-improve-operating-process/SKILL.md`
- **built-by Work Object(s):** `2026-08-22-004`, governed by `2026-08-22-010`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-036
- **applicable dimensions:** recovery quality, artifact value, novelty yield
- **owning skill/profile:** `business-improve-operating-process`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** pending first governed grilling pass
- **status rationale / findings:** Accepted business capability; registered with explicit business governance.

## COMP-027 — Financial decision assessment

- **status:** active
- **component kind:** skill
- **governance domain:** business
- **location(s):** `skills/core/business-assess-financial-decision/SKILL.md`
- **built-by Work Object(s):** `2026-08-22-004`, governed by `2026-08-22-010`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-036
- **applicable dimensions:** recovery quality, artifact value
- **owning skill/profile:** `business-assess-financial-decision`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** pending first governed grilling pass
- **status rationale / findings:** Accepted business capability; registered with explicit business governance.

## COMP-028 — Workforce accountability planning

- **status:** active
- **component kind:** skill
- **governance domain:** business
- **location(s):** `skills/core/business-plan-workforce-accountability/SKILL.md`
- **built-by Work Object(s):** `2026-08-22-004`, governed by `2026-08-22-010`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-036
- **applicable dimensions:** personal fit, artifact value, novelty yield
- **owning skill/profile:** `business-plan-workforce-accountability`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** pending first governed grilling pass
- **status rationale / findings:** Accepted business capability; registered with explicit business governance.

## COMP-029 — Strategy formulation

- **status:** active
- **component kind:** skill
- **governance domain:** business
- **location(s):** `skills/core/business-formulate-strategy/SKILL.md`
- **built-by Work Object(s):** `2026-08-22-008`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-036
- **applicable dimensions:** personal fit, artifact value, novelty yield
- **owning skill/profile:** `business-formulate-strategy`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** pending first governed grilling pass
- **status rationale / findings:** Accepted seven-skill business tranche capability; registered with explicit business governance.

## COMP-030 — Market intelligence management

- **status:** active
- **component kind:** skill
- **governance domain:** business
- **location(s):** `skills/core/business-manage-market-intelligence/SKILL.md`
- **built-by Work Object(s):** `2026-08-22-008`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-036
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `business-manage-market-intelligence`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** pending first governed grilling pass
- **status rationale / findings:** Accepted seven-skill business tranche capability; registered with explicit business governance.

## COMP-031 — Driver-based planning and forecast

- **status:** active
- **component kind:** skill
- **governance domain:** business
- **location(s):** `skills/core/business-build-driver-based-plan-and-forecast/SKILL.md`
- **built-by Work Object(s):** `2026-08-22-008`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-036
- **applicable dimensions:** recovery quality, artifact value
- **owning skill/profile:** `business-build-driver-based-plan-and-forecast`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** pending first governed grilling pass
- **status rationale / findings:** Accepted seven-skill business tranche capability; registered with explicit business governance.

## COMP-032 — Enterprise risk management

- **status:** active
- **component kind:** skill
- **governance domain:** business
- **location(s):** `skills/core/business-manage-enterprise-risk/SKILL.md`
- **built-by Work Object(s):** `2026-08-22-008`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-036
- **applicable dimensions:** recovery quality, artifact value, novelty yield
- **owning skill/profile:** `business-manage-enterprise-risk`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** pending first governed grilling pass
- **status rationale / findings:** Accepted seven-skill business tranche capability; registered with explicit business governance.

## COMP-033 — Supplier sourcing and governance

- **status:** active
- **component kind:** skill
- **governance domain:** business
- **location(s):** `skills/core/business-source-and-govern-suppliers/SKILL.md`
- **built-by Work Object(s):** `2026-08-22-008`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-036
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `business-source-and-govern-suppliers`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** pending first governed grilling pass
- **status rationale / findings:** Accepted seven-skill business tranche capability; registered with explicit business governance.

## COMP-034 — Project delivery direction

- **status:** active
- **component kind:** skill
- **governance domain:** business
- **location(s):** `skills/core/business-direct-project-delivery/SKILL.md`
- **built-by Work Object(s):** `2026-08-22-008`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-036
- **applicable dimensions:** recovery quality, artifact value, novelty yield
- **owning skill/profile:** `business-direct-project-delivery`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** pending first governed grilling pass
- **status rationale / findings:** Accepted seven-skill business tranche capability; registered with explicit business governance.

## COMP-035 — Customer success management

- **status:** active
- **component kind:** skill
- **governance domain:** business
- **location(s):** `skills/core/business-manage-customer-success/SKILL.md`
- **built-by Work Object(s):** `2026-08-22-008`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-036
- **applicable dimensions:** personal fit, artifact value, novelty yield
- **owning skill/profile:** `business-manage-customer-success`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** pending first governed grilling pass
- **status rationale / findings:** Accepted seven-skill business tranche capability; registered with explicit business governance.

## COMP-036 — Business operating pipeline

- **status:** active
- **component kind:** protocol
- **governance domain:** business
- **location(s):** `references/BUSINESS-OPERATING-PIPELINE.md`
- **built-by Work Object(s):** `2026-08-22-014`
- **depends-on:** COMP-001, COMP-002, COMP-025 through COMP-035, COMP-037 through COMP-040
- **depended-on-by:** none declared
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** business skill suite via `references/BUSINESS-OPERATING-PIPELINE.md`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** pending first governed grilling pass
- **status rationale / findings:** Accepted business routing protocol that distinguishes the Work Object lifecycle, commercial pipeline, and cross-business operating pipeline while preserving each business skill's authority boundary.

## COMP-037 — Initiative portfolio governance

- **status:** active
- **component kind:** skill
- **governance domain:** business
- **location(s):** `skills/core/business-govern-initiative-portfolio/SKILL.md`
- **built-by Work Object(s):** `2026-08-22-015`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-036
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `business-govern-initiative-portfolio`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** pending first governed grilling pass
- **status rationale / findings:** Accepted next-slice business capability; registered with explicit business governance.

## COMP-038 — Pricing and packaging design

- **status:** active
- **component kind:** skill
- **governance domain:** business
- **location(s):** `skills/core/business-design-pricing-and-packaging/SKILL.md`
- **built-by Work Object(s):** `2026-08-22-015`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-036
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `business-design-pricing-and-packaging`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** pending first governed grilling pass
- **status rationale / findings:** Accepted next-slice business capability; registered with explicit business governance.

## COMP-039 — Liquidity and cash runway management

- **status:** active
- **component kind:** skill
- **governance domain:** business
- **location(s):** `skills/core/business-manage-liquidity-and-cash-runway/SKILL.md`
- **built-by Work Object(s):** `2026-08-22-015`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-036
- **applicable dimensions:** recovery quality, artifact value
- **owning skill/profile:** `business-manage-liquidity-and-cash-runway`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** pending first governed grilling pass
- **status rationale / findings:** Accepted next-slice business capability; registered with explicit business governance.

## COMP-040 — Demand, supply, and capacity balancing

- **status:** active
- **component kind:** skill
- **governance domain:** business
- **location(s):** `skills/core/business-balance-demand-supply-capacity/SKILL.md`
- **built-by Work Object(s):** `2026-08-22-015`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-036
- **applicable dimensions:** recovery quality, artifact value, novelty yield
- **owning skill/profile:** `business-balance-demand-supply-capacity`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** pending first governed grilling pass
- **status rationale / findings:** Accepted next-slice business capability; registered with explicit business governance.

## COMP-041 — Production GPU orchestrator

- **status:** active
- **component kind:** runtime
- **governance domain:** production
- **location(s):** `tools/production/gpu_orchestrator/`
- **built-by Work Object(s):** `2026-08-24-013`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-042, COMP-043
- **applicable dimensions:** recovery quality, artifact value
- **owning skill/profile:** `production-orchestrate-gpu`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** pending first governed grilling pass
- **status rationale / findings:** Accepted production runtime for sequential VRAM discipline: file-backed GPU claim registry, at-most-one owner, stale-owner recovery, wrong-owner release protection, and downstream Blender/ComfyUI claim integration.

## COMP-042 — Production Blender operator

- **status:** active
- **component kind:** skill
- **governance domain:** production
- **location(s):** `skills/core/production-operate-blender/SKILL.md`; `tools/production/blender_operator/`
- **built-by Work Object(s):** `2026-08-24-014`
- **depends-on:** COMP-001, COMP-002, COMP-041
- **depended-on-by:** COMP-048, COMP-049, COMP-050
- **applicable dimensions:** artifact value, recovery quality
- **owning skill/profile:** `production-operate-blender`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** pending first governed grilling pass
- **status rationale / findings:** Accepted production capability for bounded Blender execution: crash-durable command queue, governed §4.2 operation surface, protect-field enforcement, arbitrary-Python escalation gate, and COMP-041 GPU claim discipline.

## COMP-043 — Production ComfyUI operator

- **status:** active
- **component kind:** skill
- **governance domain:** production
- **location(s):** `skills/core/production-operate-comfyui/SKILL.md`; `tools/production/comfyui_operator/`
- **built-by Work Object(s):** `2026-08-24-015`
- **depends-on:** COMP-001, COMP-002, COMP-041
- **depended-on-by:** COMP-048, COMP-049, COMP-050
- **applicable dimensions:** artifact value, recovery quality
- **owning skill/profile:** `production-operate-comfyui`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** pending first governed grilling pass
- **status rationale / findings:** Accepted production capability for bounded ComfyUI API execution: localhost workflow submission/polling surface, read-only model listing, and COMP-041 GPU claim discipline for Flux/Hunyuan queued work.

## COMP-044 — Production TTS operator

- **status:** active
- **component kind:** skill
- **governance domain:** production
- **location(s):** `skills/core/production-operate-tts/SKILL.md`; `tools/production/tts_operator/`
- **built-by Work Object(s):** `2026-08-24-016`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-052, COMP-053
- **applicable dimensions:** artifact value, recovery quality
- **owning skill/profile:** `production-operate-tts`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** pending first governed grilling pass
- **status rationale / findings:** Accepted production capability for Tier 1 local TTS execution: Piper-backed WAV take generation, deterministic A/B/C/D variation, structured take metadata, and explicit exclusion of performance judgment, take selection, cloud tiers, System.Speech, and GPU contention.
