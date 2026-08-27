---
schema_version: 1
id: 2026-08-22-032
title: Build design-govern-interaction-motion skill
type: project
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
domain: [design, governance]
created_at: 2026-08-22T15:19:49Z
updated_at: 2026-08-22T15:26:15Z
next_action: Director decision: commit these changes, or continue working uncommitted.







---
## Intent

Add `design-govern-interaction-motion` as a new skill in the design
pipeline, owning a frontier the pipeline currently only discovers, never
governs: motion and interaction behavior as a reusable design asset.

Grounded in `.work-studio/deliverables/2026-08-22-027-design-pipeline-enhancement-skills.md`
(produced by `alawas-research-produce-report`, WO `2026-08-22-027`), carried
forward as accepted source material. That report established, with
file-level evidence, that motion/interaction exists in the pipeline only as
*discovered tokens*: `design-build-design-foundation` inventories
"animation/transition tokens" as read-only discovery of what already
exists in code, and `design-verify-design-implementation` checks "state
transitions" only as behavioral correctness -- explicitly not its focus.
No skill *composes or stewards* interaction behavior: timing curves, motion
choreography, per-state micro-interaction behavior, or
`prefers-reduced-motion` handling. The `FRONTIER_OWNERS` map had no
motion/interaction frontier at all before this Work Object.

This is the third and last recommendation from WO 2026-08-22-027's report.
The other two (`design-audit-accessibility`, WO 2026-08-22-028; and
`design-critique-usability`, WO 2026-08-22-030) are already built,
committed, and wired into the frontier map. This recommendation was the
report's weakest-confidence of the three ("MEDIUM-HIGH", vs. HIGHEST and
HIGH for the other two) -- the gap is real and structural, but less sharply
disowned than accessibility's explicit non-goal or critique's zero-mention
grep result.

The report's proposed shape (not yet a binding decision, carried forward as
a starting point): a composition/stewardship skill, sibling to
`design-compose-design-system` and `design-steward-experience-patterns`,
that governs motion and interaction as reusable assets -- named motion
recipes, timing/easing semantics, per-state interaction behavior, and
reduced-motion handling. New `interaction-motion` frontier, positioned
between system composition and experience-pattern stewardship in the
canonical route.

Not yet resolved: unlike the other two (which were read-only audit/critique
skills), this one *composes and stewards* assets -- closer in shape to
`design-compose-design-system` than to `design-audit-accessibility`. The
authoring pattern and tracer-bullet mechanism will look different: not "run
an inspection and report findings" but "can motion/interaction be
represented as a governed, reusable asset record the same way tokens and
themes already are?"

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] A bounded tracer bullet tests the smallest real slice -- e.g., can one
      real motion/interaction behavior already present in this repo (or a
      target project) be represented as a governed asset record, distinct
      from a bare CSS token -- before the full skill is authored
- [x] `design-govern-interaction-motion/SKILL.md` exists with boundaries,
      capability mappings, and Grilling Profile matching the other 12
      design skills
- [x] The new `interaction-motion` frontier is registered in
      `tools/ws/design_asset_routing.py:FRONTIER_OWNERS` and
      `references/DESIGN-ASSET-PIPELINE.md`'s ownership map and canonical
      route
- [x] The skill composes/stewards motion-asset truth without mutating
      canonical assets outside its own routed authority, mirroring
      `design-compose-design-system`'s and
      `design-steward-experience-patterns`'s own guardrails


## Constraints and non-goals

**Constraints:**
- Composition/stewardship posture, matching `design-compose-design-system`
  and `design-steward-experience-patterns` -- preserves director creative
  authority, never unilaterally mutates canonical assets.
- Must be independent of and distinct from
  `design-build-design-foundation`'s token *discovery* -- this skill governs
  motion as a composed asset, it does not re-discover raw CSS
  animation/transition tokens (that remains build-design-foundation's job).
- New frontier must be added to both the routing map and the pipeline
  reference doc -- not left as an undeclared owner.

**Non-goals:**
- Discovering existing animation/transition tokens from code -- that
  remains `design-build-design-foundation`'s domain; this skill consumes
  discovered tokens, it does not re-scan for them.
- Checking behavioral correctness (does the interaction actually fire
  correctly in a running app) -- that remains
  `design-verify-design-implementation`'s domain.
- Implementing any motion/interaction in code -- composition produces a
  governed asset record; implementation routes through
  `alawas-engineering-implement-bounded-change` like any other accepted
  change.
- Reopening `design-audit-accessibility` or `design-critique-usability`
  (both already built and committed) -- this Work Object advances only the
  third, last-remaining recommendation from WO 2026-08-22-027.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Accept tracer bullet: schema-capacity test for a motion asset kind, not a content audit

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | A three-step schema-level test: (1) confirm compose_draft_asset_record(asset_kind="motion", ...) fails today with the expected ValueError from the VALID_ASSET_KINDS enum gate; (2) add "motion" to VALID_ASSET_KINDS and re-run the same call; (3) check the resulting draft record against validate_asset_record()'s REQUIRED_FIELDS/REQUIRED_SECTIONS to see whether the existing generic record shape is sufficient for a motion asset, or whether it's missing something (e.g. timing/easing has nowhere structured to live). No real motion behavior exists in this repo yet, so the draft's content is a placeholder -- the tracer tests schema capacity, not a real design decision. Explicitly excludes: full design-govern-interaction-motion/SKILL.md, frontier registration, inventing a fictional real motion behavior, any CSS/motion implementation. |
| **Authorization** | Director: "Yes, go with that tracer" |
| **Confidence** | high that the enum gate is the correct first blocker to test (it's a hard ValueError in code, not a soft convention); lower confidence on whether one enum value is sufficient vs. the record shape needing new fields -- that uncertainty is exactly what step 3 is designed to resolve, not a weakness in the tracer's design |
| **Actor** | director |
| **Revisit trigger** | Result of running all three steps. Enum change alone is sufficient (record shape passes structurally) -> proceed to authoring the full skill, folding the enum change into that work. Existing record shape can't express something motion assets need -> stop, design the needed schema addition before authoring. |
| **Rationale** | This skill composes governed assets, unlike the two read-only audits already built -- the risk is schema capacity, not "can inspection find a problem." Testing the schema mechanically, against the real compose/validate functions, is cheaper than authoring a full skill around an assumption about the schema that might be wrong. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | design-build-design-foundation/SKILL.md:93,125 | Inventories "animation/transition tokens" as read-only discovery of what already exists in code -- confirmed this is discovery, not composition or stewardship of motion behavior. |
| [system] | design-verify-design-implementation/SKILL.md:20,43 | Checks "state transitions" only as behavioral correctness; behavioral dimensions are explicitly not verify's focus. |
| [system] | tools/ws/design_assets.py:VALID_ASSET_KINDS | The current asset-kind enum is {foundation, token-set, theme, component-family, ux-pattern, flow, projection} -- no motion/interaction kind exists. A governed motion asset record cannot be created under the current schema without this enum changing, a concrete structural question the tracer must resolve, not assume away. |
| [system] | .work-studio/deliverables/2026-08-22-027-design-pipeline-enhancement-skills.md | Full report carried forward; this is the third and last recommendation advanced, and the report's own weakest-confidence one (MEDIUM-HIGH vs. HIGH/HIGHEST for the other two). |
| [decision] | director: "Advance design-govern-interaction-motion into its own Work Object" | Director selected the report's third and final recommendation to advance, completing the set. |
| [gap] | ws transition audit (build) | No decision record with result: pass found at build transition. An accepted decision record is expected before entering build state. |
| [system] | python -c compose_draft_asset_record/validate_asset_record trace, tools/ws/design_assets.py | Tracer bullet result: step 1 confirmed the expected failure -- compose_draft_asset_record(asset_kind='motion', ...) raised ValueError against the pre-change enum, listing the 7 existing kinds with no 'motion'. Step 2: added 'motion' to VALID_ASSET_KINDS in tools/ws/design_assets.py; the same compose call then succeeded, producing a well-formed draft record. Step 3: validate_asset_record() against the resulting record returned zero errors -- all REQUIRED_FIELDS and REQUIRED_SECTIONS present. Assumption holds mechanically: one enum addition is sufficient for a motion asset to pass structural validation. Honest caveat carried forward, not smoothed over: passing validate_asset_record only proves the record *shape* accepts a motion kind -- motion-specific properties (timing curve, easing, duration, trigger, reduced-motion behavior) have no structured field of their own and would live as free prose inside 'Asset Summary', identical to every other asset kind. Whether that's sufficient for real composition work, or whether the full skill should add an optional structured 'Motion Properties' subsection (comparable to Lifecycle's table), is an open authoring question, not resolved by this tracer. |
| [gap] | ws transition audit (verify) | Unresolved [gap] entries exist in the Evidence ledger. Residual uncertainty should be reviewed before proceeding. |
| [decision] | director: 'Recommend one and proceed' | Recommended and adopted: keep motion properties as prose in Asset Summary rather than adding a structured 'Motion Properties' subsection, since no existing asset kind has a kind-specific structural carve-out and no real motion asset yet exists to prove prose is inadequate. Recorded as a Revisit trigger in the authored skill (skills/core/design-govern-interaction-motion/SKILL.md), not a permanent foreclosure -- reopens if real motion assets show prose can't clearly carry timing/easing/trigger information. |
| [system] | skills/core/design-govern-interaction-motion/SKILL.md, references/DESIGN-ASSET-REGISTRY.md, tools/generate-adapters.py --check | Authored the full skill, shaped like design-compose-design-system (composition/stewardship, not a read-only audit): Governing principle, Boundaries/non-goals, Inputs/preconditions, Required capabilities, Consequence/authority rules, Grilling Profile entry added to SKILL-AWARE-GRILLING.md, 6-stage workflow mirroring compose-design-system's stages, Output template, and a Revisit trigger recording the prose-vs-structured-fields decision. Registered the new 'interaction-motion' frontier in tools/ws/design_asset_routing.py:FRONTIER_OWNERS and references/DESIGN-ASSET-PIPELINE.md's ownership map and canonical route (positioned after design-compose-design-system, before design-steward-experience-patterns, per Intent). Also updated references/DESIGN-ASSET-REGISTRY.md's documented Asset kind enum to include 'motion', matching the code change from the tracer. Found and fixed a second copy of the same enum in tools/ws/__main__.py's asset-ingest CLI argparse choices -- the tracer's direct Python-function test bypassed this CLI layer entirely and would not have caught this drift on its own; the CLI would have silently rejected --asset-kind motion even after the design_assets.py enum change. All three platform adapters regenerated with zero drift. asset-workbench.html's FRONTIER_DESCRIPTIONS also updated and regenerated to include the new frontier. |
## Open questions

- **Asset-kind schema change.** Representing a motion/interaction asset as a
  governed record likely requires adding a new value to
  `VALID_ASSET_KINDS` in `tools/ws/design_assets.py` (e.g. `"motion"`) --
  a schema change other design-asset consumers (asset-workbench,
  design-manage-assets) would need to tolerate. Not yet decided whether
  this Work Object or a follow-on makes that change.
- **Authoring path for a new studio skill.** Same open question the other
  two recommendations faced: SKILL.md structure, adapter generation,
  Grilling Profile authoring, capability mapping table.
- **Tracer scope.** Unlike the two read-only audit/critique tracers already
  run, this skill composes/stewards -- the tracer needs to test whether a
  real motion/interaction behavior can become a governed asset record, not
  whether an inspection can produce findings. What's the smallest real
  motion/interaction behavior in this repo (or absence of one) to test
  against?

## Next move

Route to `alawas-design-design-tracer-bullet`: design the smallest bounded,
observable, reversible tracer for motion/interaction governance -- e.g.,
verify that one real motion/interaction behavior can be represented as a
draft governed asset record (testing the asset-kind schema question
directly) before the full `design-govern-interaction-motion/SKILL.md` is
authored and wired into the frontier map. Carry forward the Evidence ledger
entries above (discovery-only precedent, verify's narrower focus, the
asset-kind schema gap) as given context, not re-derived.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T15:20:42Z — Classified and staged for design-tracer-bullet

- **State:** design
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Director advanced design-govern-interaction-motion, the third and last recommendation from WO 2026-08-22-027's report, completing the set alongside design-audit-accessibility (2026-08-22-028) and design-critique-usability (2026-08-22-030). Intent, Success evidence, Constraints/non-goals, and Evidence entries carried forward from the report, plus one new concrete finding: the current asset-kind enum has no motion/interaction value, a schema question the tracer must resolve. Skipping explore -- the report already resolved which frontier is uncovered and why. Remaining open questions (asset-kind schema change, tracer scope, studio skill-authoring path) are design-tracer-bullet's remit.
### 2026-08-22T15:22:07Z — Tracer bullet accepted, running schema-capacity test

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director accepted: schema-capacity test (enum gate + record-shape check) as the smallest real slice, since no real motion behavior exists in this repo to audit.
### 2026-08-22T15:23:03Z — Tracer bullet passed -- schema mechanically holds, with an honest structured-fields caveat

- **State:** verify
- **Status:** active
- **Actor:** claude-code
- **Rationale:** All 3 steps of the schema-capacity test passed: enum gate failed as expected before the change, succeeded after adding 'motion' to VALID_ASSET_KINDS, and the resulting draft record passed validate_asset_record structurally. Per Decision 1's exit criteria, proceeding to author the full skill is warranted -- the enum change is folded into that work already. Open authoring question carried forward, not resolved: whether motion-specific properties need a structured subsection rather than living as free prose in Asset Summary.
### 2026-08-22T15:26:15Z — Skill authored and wired -- all four success-evidence criteria met; all three report recommendations now complete

- **State:** verify
- **Status:** active
- **Actor:** claude-code
- **Rationale:** design-govern-interaction-motion/SKILL.md authored, mirroring design-compose-design-system's composition/stewardship shape. Frontier registered in routing map and pipeline doc; registry doc and CLI enum both updated for consistency (a second copy of the enum was found in tools/ws/__main__.py's argparse choices, missed by the tracer's direct-function test). All three platform adapters regenerated with zero drift. This completes all three recommendations from WO 2026-08-22-027's report: design-audit-accessibility, design-critique-usability, and design-govern-interaction-motion. Nothing committed yet.
