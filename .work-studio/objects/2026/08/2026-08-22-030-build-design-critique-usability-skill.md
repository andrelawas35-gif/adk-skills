---
schema_version: 1
id: 2026-08-22-030
title: Build design-critique-usability skill
type: project
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
domain: [design, governance]
created_at: 2026-08-22T15:10:15Z
updated_at: 2026-08-22T15:18:02Z
next_action: Director decision: commit these changes, or continue working uncommitted. design-govern-interaction-motion remains the only un-advanced recommendation from WO 2026-08-22-027.






---
## Intent

Add `design-critique-usability` as a new skill in the design pipeline,
owning a frontier the pipeline currently has zero coverage for: heuristic
usability evaluation independent of a specific confirmed direction.

Grounded in `.work-studio/deliverables/2026-08-22-027-design-pipeline-enhancement-skills.md`
(produced by `alawas-research-produce-report`, WO `2026-08-22-027`), carried
forward as accepted source material. That report established, with
file-level evidence, that a grep across all 10 design SKILL.md files for
`heuristic | critique | usability evaluation | nielsen` returns zero
matches. `design-verify-design-implementation` checks whether an
implementation matches *what was confirmed* (parity to a specific
direction) -- a materially different question from whether the design is
*good* by usability heuristics. A design can pass verify's parity check and
still have real usability problems verify has no way to surface, because
it was never asked to look.

This is the second recommendation advanced from WO 2026-08-22-027's report
(after `design-audit-accessibility`, WO 2026-08-22-028, now built and
committed). The other two recommendations
(`design-govern-interaction-motion`, and the softer partial gaps) remain
un-advanced.

The report's proposed shape (not yet a binding decision, carried forward as
a starting point): a read-only evaluation skill that checks a real
interface against usability heuristics (visibility of system status, error
prevention, recognition over recall, consistency, etc.), producing ranked,
evidence-linked findings -- a critique of the design on its own terms, not
a pass/fail against a mock. Findings route to `design-apply-design-direction`
as candidate changes, never auto-applied; the skill holds no creative
authority of its own.

Not yet resolved, matching `design-audit-accessibility`'s own open
question: the exact authoring path for a new *studio* skill (this is not a
design asset flowing through the pipeline, it is a new pipeline member), and
the smallest real tracer-bullet slice to test before the full skill is
authored.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] A bounded tracer bullet tests the smallest real slice (e.g., a small
      fixed set of heuristics checked against one real rendered interface)
      before the full skill is authored
- [x] `design-audit-accessibility/SKILL.md`-equivalent structure exists for
      `design-critique-usability`: boundaries, capability mappings, and
      Grilling Profile matching the other 10+ design skills
- [x] The new `critique` frontier is registered in
      `tools/ws/design_asset_routing.py:FRONTIER_OWNERS` and
      `references/DESIGN-ASSET-PIPELINE.md`'s ownership map and canonical
      route
- [x] The skill never mutates code/assets, never auto-applies a finding as a
      fix, and never presents a heuristic judgment as an accepted creative
      decision


## Constraints and non-goals

**Constraints:**
- Read-only posture, matching every other audit/verify/critique-shaped
  skill in the pipeline -- reports findings, never fixes or mutates.
- Findings are evidence-linked to a named heuristic, not bare taste
  judgments -- each finding cites which heuristic it violates and why.
- New frontier must be added to both the routing map and the pipeline
  reference doc -- not left as an undeclared owner.

**Non-goals:**
- Fixing any finding it surfaces -- fixes route through
  `design-apply-design-direction` and
  `alawas-engineering-implement-bounded-change` like any other
  design-direction change.
- Replacing `design-verify-design-implementation`'s parity check -- this
  skill evaluates design quality independent of a confirmed direction;
  verify still checks whether a confirmed direction was correctly built.
- Reopening `design-audit-accessibility` (already built, WO 2026-08-22-028)
  or advancing `design-govern-interaction-motion` -- that remains a
  separate, un-advanced recommendation unless the director opens its own
  Work Object.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Accept tracer bullet: three statically-checkable heuristics against a real repo HTML file

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | A one-off inspection of `.work-studio/asset-workbench.html` against three heuristics checkable without live interaction: visibility of system status, consistency and standards, recognition rather than recall. Each finding cites the specific element and quotes/describes exactly what violates the heuristic -- no bare taste judgment. Read-only: no mutation of the target file, no browser automation, no network. Explicitly excludes: full `design-critique-usability/SKILL.md`, frontier registration, heuristics requiring live interaction (error recovery, undo, help/documentation), user testing, and fixing anything found. |
| **Authorization** | Director: "Yes, go with that tracer" |
| **Confidence** | high that inspection-based checking is the right first mechanism for statically-checkable heuristics -- the riskiest assumption (can heuristic evaluation produce evidence-linked findings, not vague taste judgments) is falsifiable cheaply this way; the choice to exclude live-interaction heuristics from v1 scope is deliberate, not a limitation discovered after the fact |
| **Actor** | director |
| **Revisit trigger** | Result of running the inspection against the real `asset-workbench.html`. At least one concrete, evidence-linked finding -> proceed to authoring the full skill using this mechanism. Findings stay vague/taste-based with nothing concrete to cite -> stop, heuristic evaluation needs a different mechanism (e.g. comparison against a specific pattern library) before authoring. |
| **Rationale** | Building the full skill before verifying whether heuristic evaluation can be evidence-linked (vs. vague taste judgment) risks authoring a skill that produces unusable, unchallengeable findings. Testing against a real file already in this workspace is the cheapest way to know before further design or implementation investment. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | grep across all 10 design SKILL.md files (report WO 2026-08-22-027) | Zero matches for heuristic/critique/usability-evaluation -- confirmed structurally, not just by absence of a mention. |
| [system] | design-verify-design-implementation/SKILL.md:20 | Verify checks parity to the confirmed proposal or implementation brief -- a materially different question from whether the design is good on its own terms. |
| [system] | .work-studio/deliverables/2026-08-22-027-design-pipeline-enhancement-skills.md | Full report carried forward as source material; this Work Object advances its second-ranked recommendation (design-critique-usability), following design-audit-accessibility (WO 2026-08-22-028, built and committed). design-govern-interaction-motion remains un-advanced. |
| [decision] | director: "Advance the next report recommendation" | Director selected design-critique-usability (ranked #2, HIGH confidence in the report) to advance next, following the same ranking discipline used for design-audit-accessibility. |
| [gap] | ws transition audit (build) | No decision record with result: pass found at build transition. An accepted decision record is expected before entering build state. |
| [system] | manual inspection of real .work-studio/asset-workbench.html against 3 heuristics | Tracer bullet result: 4 evidence-linked findings produced (1 pass, 3 fail), each citing exact markup, none a vague taste judgment. Visibility of system status: PASS on the page's top .meta line (generation timestamp + concrete counts); FAIL on 'Lifecycle owners: 10' showing a bare count with no way to inspect who the owners are. Consistency and standards: FAIL -- the same page mixes an explicit dt/dd labeled pattern for some metadata (Source of truth, Record) with an unlabeled middot-separated line for other conceptually equivalent metadata (asset kind, status, Work Object: 'ux-pattern . draft . Work Object 2026-08-22-017'), no signal for which convention applies where. Recognition rather than recall: FAIL (2 instances) -- the same middot line requires knowing the schema's field order to parse it (recall, not recognition); the Frontier Ownership table lists raw internal frontier tokens (component-family, ux-pattern, theme) with no glossary. Assumption holds: heuristic evaluation by inspection alone produced concrete, citable, challengeable findings rather than vague taste judgments -- the riskiest assumption for this tracer. |
| [gap] | ws transition audit (verify) | Unresolved [gap] entries exist in the Evidence ledger. Residual uncertainty should be reviewed before proceeding. |
| [system] | skills/core/design-critique-usability/SKILL.md, tools/generate-adapters.py --check | Authored the full skill matching design-audit-accessibility's structure: Governing principle, Boundaries/non-goals, Inputs/preconditions, Required capabilities, Consequence/authority rules (low, read-only), Grilling Profile entry added to SKILL-AWARE-GRILLING.md, 6-stage workflow, [system:usability-critique] output contract, Final self-check. Registered the new 'critique' frontier in tools/ws/design_asset_routing.py:FRONTIER_OWNERS and references/DESIGN-ASSET-PIPELINE.md. All three platform adapters regenerated with zero drift. Separately fixed all 4 findings from the tracer in tools/ws/asset_workbench.py (the generator, not the generated HTML): Lifecycle owners now lists real owning-skill names instead of a bare count (visibility of system status); the unlabeled middot line (kind . status . Work Object) folded into the same labeled dt/dd pattern used elsewhere on the page (consistency and standards, and recognition rather than recall); the Frontier Ownership table gained a 'What it covers' column with plain-language descriptions for every frontier including the two new ones (recognition rather than recall). Regenerated asset-workbench.html and re-inspected: all 4 findings resolved. |
## Open questions

- **Heuristic set for v1.** Nielsen's 10 heuristics are the most established
  starting point, but the report didn't commit to a specific list -- which
  subset (or all 10) belongs in the first real slice is a tracer-bullet
  question, not yet decided.
- **Authoring path for a new studio skill.** Same open question as
  `design-audit-accessibility` faced: SKILL.md structure, adapter
  generation, Grilling Profile authoring, capability mapping table, all
  following the studio's existing convention.
- **Tracer scope.** What is the smallest real slice to test first -- one
  heuristic against one real rendered page, or a small fixed set? Not yet
  decided.

## Next move

Route to `alawas-design-design-tracer-bullet`: design the smallest bounded,
observable, reversible tracer for the usability critique -- e.g., verify
that a small, named subset of usability heuristics can be checked read-only
against one real rendered interface and produce ranked, evidence-linked
findings, before the full `design-critique-usability/SKILL.md` is authored
and wired into the frontier map. Carry forward the three Evidence ledger
entries above (zero-coverage evidence, verify's different question, the
report's ranking) as given context, not re-derived.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T15:10:57Z — Classified and staged for design-tracer-bullet

- **State:** design
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Director advanced design-critique-usability (report's #2 ranked recommendation, HIGH confidence) from WO 2026-08-22-027, following the same route already run for design-audit-accessibility (WO 2026-08-22-028). Intent, Success evidence, Constraints/non-goals, and Evidence entries carried forward from the report. Skipping explore -- the report already resolved which frontier is uncovered and why. Remaining open questions (heuristic set, tracer scope, studio skill-authoring path) are design-tracer-bullet's remit.
### 2026-08-22T15:13:13Z — Tracer bullet accepted, running usability inspection

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director accepted: three statically-checkable heuristics against .work-studio/asset-workbench.html as the smallest real slice.
### 2026-08-22T15:14:13Z — Tracer bullet passed -- heuristic inspection produced evidence-linked findings

- **State:** verify
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Manual inspection against asset-workbench.html produced 4 concrete findings (1 pass, 3 fail) across 3 statically-checkable heuristics, each citing exact markup rather than vague taste judgment. Assumption confirmed: heuristic evaluation by inspection alone can be evidence-linked. Per Decision 1's exit criteria, proceeding to author the full skill is warranted.
### 2026-08-22T15:18:02Z — Skill authored, findings fixed -- all four success-evidence criteria met

- **State:** verify
- **Status:** active
- **Actor:** claude-code
- **Rationale:** design-critique-usability/SKILL.md authored matching the pipeline's structure; critique frontier registered in routing map and pipeline doc; all three platform adapters regenerated with zero drift. Separately fixed all 4 tracer findings in tools/ws/asset_workbench.py (the generator): lifecycle owners now list real names, metadata fields consistently labeled, frontier table gained plain-language descriptions. Re-inspected regenerated asset-workbench.html: all 4 findings resolved. Nothing committed yet.
