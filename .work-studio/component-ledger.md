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

- **status:** needs-regrill
- **location(s):** `references/AGREEMENT-LOOP.md` (canonical; copied into every skill's `references/` by `tools/generate-adapters.py`)
- **built-by Work Object(s):** pre-ledger backfill; recent shaping in WO `2026-07-16-004` (two-tier lenses)
- **depends-on:** none declared
- **depended-on-by:** COMP-002 through COMP-013 (every skill's Grilling Session; widest blast radius)
- **applicable dimensions:** personal fit, artifact value, novelty yield (recovery quality deferred — engine-level, not outcome-level)
- **owning skill/profile:** all skill profiles via `references/SKILL-AWARE-GRILLING.md`
- **last-grilled-SHA:** `d0cb044`
- **best-case anchor:** Option-B-refined (WO 2026-07-18-001, 2026-07-18T05:00:00Z) — settled = no surviving finding against the applicable dimensions; auto-reopen on git-drift since `last-grilled-SHA`, owning-skill version change, or contrary govern-scorecards outcome evidence. No standing scorecard artifact.
- **first grilled:** 2026-07-18 (tracer pass, WO 2026-07-18-001)
- **open findings:** SIG-1 (see `.work-studio/inbox.md`) — cadence ambiguity, plus 3 secondary findings recorded in the pass below

### Grilling pass — 2026-07-18 (against Grilling Profile + inline criteria)

- **F1 [artifact value / HIGH]** `AGREEMENT-LOOP.md:103` (*"Ask exactly one decision-bearing question and wait"*) vs `:129` (*"no numerical question cap: three, 200, or more turns are valid"*): the doc never states that the one-question limit is **per turn** while continuity is **per session**. A reader can read "continuous Grilling Session" as "many questions at once." This ambiguity **actively misled in this very session** — lived evidence, not hypothetical.
- **F2 [personal fit / HIGH]** The engine encodes only **depth-first serial** grilling. It has no **breadth/sweep mode** for covering many independent branches, which is exactly the coverage the component-sweep needs — the engine can't yet express the behavior the project it governs requires.
- **F3 [novelty yield / MED]** `:24` "*`do recommended` accepts only the recommendation currently in focus*" leaves **"in focus" undefined** when multiple recommendations were presented in one turn; caused real friction this session.
- **F4 [artifact value / MED]** Convergence (`:176` Coverage Proof) asserts branch-map completeness but gives **no test for whether the branch map is actually complete** — "no remaining question is likely to change the recommendation" is unfalsifiable as written.
- **Verdict:** NOT settled. ≥1 concrete, file-grounded, actionable finding → the mechanism produces real signal. Highest-value finding (F1) queued as `SIG-1`.

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
