# Component Ledger

<!--
  Canonical artifact accepted by ADR 0014 and owned by `track-components`.

  A derived index of realized capabilities (components) this project has shipped,
  each grillable toward its best-case. Entries point at where the component lives;
  the component's truth stays in code/ADRs. See WO 2026-07-18-001 for the design.

  Entry schema: status; location(s); built-by Work Object(s); declared edges;
  applicable dimensions; owning skill/profile; last-grilled-SHA;
  Option-B-refined best-case anchor; status rationale/findings.
  Status values: active | settled | needs-regrill | retired. Entries are
  pointers, not component copies; retired entries are preserved, never deleted.
-->

## COMP-001 — Grilling engine (Agreement Loop)

- **status:** settled
- **location(s):** `references/AGREEMENT-LOOP.md` (canonical; copied into every skill's `references/` by `tools/generate-adapters.py`)
- **built-by Work Object(s):** pre-ledger backfill; recent shaping in WO `2026-07-16-004` (two-tier lenses); resolved in WO `2026-07-27-003`
- **depends-on:** none declared
- **depended-on-by:** COMP-002 through COMP-013 (every skill's Grilling Session; widest blast radius)
- **applicable dimensions:** personal fit, artifact value, novelty yield (recovery quality deferred — engine-level, not outcome-level)
- **owning skill/profile:** all skill profiles via `references/SKILL-AWARE-GRILLING.md`
- **last-grilled-SHA:** `57d0412`
- **best-case anchor:** Option-B-refined (WO 2026-07-18-001, 2026-07-18T05:00:00Z) — settled = no surviving finding against the applicable dimensions; auto-reopen on git-drift since `last-grilled-SHA`, owning-skill version change, or contrary govern-scorecards outcome evidence. No standing scorecard artifact.
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
- **location(s):** `skills/core/conduct-work-object/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001
- **depended-on-by:** COMP-003 through COMP-013
- **applicable dimensions:** recovery quality, artifact value, novelty yield
- **owning skill/profile:** `conduct-work-object`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-003 — Decision pressure testing

- **status:** active
- **location(s):** `skills/core/pressure-test-decision/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** none declared
- **applicable dimensions:** personal fit, artifact value, novelty yield
- **owning skill/profile:** `pressure-test-decision`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-004 — Tracer-bullet design

- **status:** active
- **location(s):** `skills/core/design-tracer-bullet/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-005
- **applicable dimensions:** recovery quality, artifact value, novelty yield
- **owning skill/profile:** `design-tracer-bullet`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-005 — Bounded implementation

- **status:** active
- **location(s):** `skills/core/implement-bounded-change/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002, COMP-004
- **depended-on-by:** COMP-006
- **applicable dimensions:** recovery quality, artifact value, novelty yield
- **owning skill/profile:** `implement-bounded-change`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-006 — Release-evidence verification

- **status:** active
- **location(s):** `skills/core/verify-release-evidence/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002, COMP-005
- **depended-on-by:** none declared
- **applicable dimensions:** recovery quality, artifact value
- **owning skill/profile:** `verify-release-evidence`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-007 — Deployment with recovery

- **status:** active
- **location(s):** `skills/core/deploy-with-recovery/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002, COMP-006
- **depended-on-by:** none declared
- **applicable dimensions:** recovery quality, artifact value
- **owning skill/profile:** `deploy-with-recovery`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-008 — Outcome review and adaptation

- **status:** active
- **location(s):** `skills/core/review-outcome-and-adapt/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-011, COMP-012
- **applicable dimensions:** recovery quality, personal fit, artifact value, novelty yield
- **owning skill/profile:** `review-outcome-and-adapt`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-009 — Live-question investigation

- **status:** active
- **location(s):** `skills/core/investigate-live-question/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** none declared
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `investigate-live-question`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-010 — Production incident diagnosis

- **status:** active
- **location(s):** `skills/core/diagnose-production-incident/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** none declared
- **applicable dimensions:** recovery quality, artifact value
- **owning skill/profile:** `diagnose-production-incident`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-011 — Working-method governance

- **status:** active
- **location(s):** `skills/core/maintain-working-method/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002, COMP-008
- **depended-on-by:** none declared
- **applicable dimensions:** personal fit, artifact value, novelty yield
- **owning skill/profile:** `maintain-working-method`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-012 — Outcome scorecard governance

- **status:** active
- **location(s):** `skills/core/govern-scorecards/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002, COMP-008
- **depended-on-by:** COMP-013
- **applicable dimensions:** recovery quality, personal fit, artifact value, novelty yield
- **owning skill/profile:** `govern-scorecards`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-013 — Signal-to-work routing

- **status:** active
- **location(s):** `skills/core/turn-signal-into-work/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** none declared
- **applicable dimensions:** personal fit, artifact value, novelty yield
- **owning skill/profile:** `turn-signal-into-work`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## COMP-014 — Component tracking

- **status:** active
- **location(s):** `skills/core/track-components/SKILL.md`
- **built-by Work Object(s):** pre-ledger backfill
- **depends-on:** COMP-001, COMP-002, COMP-012
- **depended-on-by:** none declared
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `track-components`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** backfill pending first pass

## Design skills (Phase 1 — contract shells)

The entries below are the 9 design skill contract shells created in WO
`2026-07-22-006`. They are shells (structure and contracts defined, workflow
not yet implemented) and enter the ledger as `active` with `not-yet-grilled`.

## COMP-015 — Product interface audit

- **status:** active
- **location(s):** `skills/core/audit-product-interface/SKILL.md`
- **built-by Work Object(s):** `2026-07-22-006`, `2026-07-23-002`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-016, COMP-022
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `audit-product-interface`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** Contract amended per Grilling Session 13 Phase 1; Figma references removed, host→target project terminology. Pending implementation and first grilling pass.

## COMP-016 — Design foundation (token audit)

- **status:** active
- **location(s):** `skills/core/build-design-foundation/SKILL.md`
- **built-by Work Object(s):** `2026-07-22-006`, `2026-07-23-002`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** COMP-022
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `build-design-foundation`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** Contract amended per Grilling Session 13 Phase 1; Figma sync references removed, host→target project terminology. Pending implementation and first grilling pass.

## COMP-017 — User flow modeling

- **status:** retired
- **location(s):** `skills/core/model-user-flow/SKILL.md`
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
- **location(s):** `skills/core/define-interface-architecture/SKILL.md`
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
- **location(s):** `skills/core/define-interface-specification/SKILL.md`
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
- **location(s):** `skills/core/render-to-figma/SKILL.md`
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
- **location(s):** `skills/core/connect-design-to-code/SKILL.md`
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
- **location(s):** `skills/core/apply-design-direction/SKILL.md`
- **built-by Work Object(s):** `2026-07-22-006`, `2026-07-23-002`
- **depends-on:** COMP-001, COMP-002, COMP-015, COMP-016
- **depended-on-by:** COMP-023
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `apply-design-direction`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** Contract rewritten per Grilling Session 13 Phase 1; changed from revision-manifest producer to propose/confirm/execute creative authority loop. Now writes code after confirmation (meaningful consequence). Pending implementation and first grilling pass.

## COMP-023 — Design implementation verification

- **status:** active
- **location(s):** `skills/core/verify-design-implementation/SKILL.md`
- **built-by Work Object(s):** `2026-07-22-006`, `2026-07-23-002`
- **depends-on:** COMP-001, COMP-002, COMP-022
- **depended-on-by:** none declared
- **applicable dimensions:** artifact value, novelty yield
- **owning skill/profile:** `verify-design-implementation`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** Renamed from verify-design-code-parity per Grilling Session 13 Phase 1; contract rewritten for browser-only verification against confirmed proposals (no Figma parity, no specification parity). Pending implementation and first grilling pass.

## COMP-024 — Divergent idea development

- **status:** active
- **location(s):** `skills/core/develop-idea/SKILL.md`
- **built-by Work Object(s):** `2026-07-26-002`
- **depends-on:** COMP-001, COMP-002
- **depended-on-by:** none declared
- **applicable dimensions:** personal fit, artifact value, novelty yield
- **owning skill/profile:** `develop-idea`
- **last-grilled-SHA:** not-yet-grilled
- **best-case anchor:** Option-B-refined; no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** First divergent exploration capability in the system. Skill contract created from Idea Development Grilling Session (17 decisions). Pending first tracer bullet run and grilling pass.
