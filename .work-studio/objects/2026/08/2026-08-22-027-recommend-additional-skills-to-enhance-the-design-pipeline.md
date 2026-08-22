---
schema_version: 1
id: 2026-08-22-027
title: Recommend additional skills to enhance the design pipeline
type: inquiry
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-22T14:50:22Z
updated_at: 2026-08-22T14:53:28Z
next_action: Director selects which recommendation(s), if any, to advance into their own Work Object. Highest-confidence candidate: design-audit-accessibility.



---
## Intent

Recommend additional skills that would enhance the existing 10-skill design
pipeline. Grounded in a structural investigation of the pipeline's frontier
map (`tools/ws/design_asset_routing.py`) and `references/DESIGN-ASSET-PIPELINE.md`:
a candidate skill is recommended only where a design-asset frontier exists that
no current skill owns. Produced by `alawas-research-produce-report` as a
report-type deliverable.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] Standalone report deliverable produced under `.work-studio/deliverables/`,
      each recommendation attributed to a verified pipeline gap
- [x] Hard gaps distinguished from partial gaps; declined recommendations
      recorded with rationale
- [ ] Director selects which recommendation(s), if any, to advance into their
      own Work Object(s)


## Constraints and non-goals

**Constraints:**
- Report synthesizes structural evidence only; authors no new architecture and
  accepts no recommendation on the director's behalf.

**Non-goals:**
- Building any of the recommended skills — each is a pending recommendation, not
  an accepted decision.
- Ranking by observed user harm; recommendations rest on structural absence, not
  usability evidence (recorded as a carried gap in the deliverable).

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
| [system] | design-steward-experience-patterns/SKILL.md:37; design-verify-design-implementation/SKILL.md:146 | Accessibility conformance is owned by no skill: steward lists "claim accessibility compliance" as a non-goal, and verify marks WCAG/keyboard/screen-reader "deferred". Basis for the highest-confidence recommendation (design-audit-accessibility). |
| [system] | grep across all 10 design SKILL.md files | Zero matches for heuristic/critique/usability-evaluation. verify checks only parity-to-confirmed-direction, not design quality on its own terms. Basis for design-critique-usability. |
| [system] | design-build-design-foundation/SKILL.md:93,125; design-verify-design-implementation/SKILL.md:20,43 | Motion/interaction exists only as discovered tokens and behavioral-correctness checks (behavior explicitly not verify's focus); no frontier owns motion design. Basis for design-govern-interaction-motion. |
| [inference] | this investigation | Ranking, hard-vs-partial gap distinction, and each proposed skill's shape are synthesis, not accepted decisions. Partial gaps (visual comps, token drift, content craft) are better served by reusing/extending thinking-develop-idea, track-components, and steward respectively. |
| [system] | .work-studio/deliverables/2026-08-22-027-design-pipeline-enhancement-skills.md | Full report deliverable (linked via Artifacts). |
| [gap] | ws transition audit (verify) | No decision record with result: pass and populated scope found. Requirement coverage evidence is expected before verify transition. |
| [decision] | director | Advanced design-audit-accessibility into its own Work Object: 2026-08-22-028. The other two recommendations (design-critique-usability, design-govern-interaction-motion) remain un-advanced. |
## Open questions

- Which recommendation(s), if any, does the director advance into their own
  Work Object? (design-audit-accessibility is the highest-confidence candidate.)
- Should any gap be re-ranked by impact evidence (observed user harm) rather
  than structural absence? That is a separate investigation if wanted.

## Next move

Director selection. No skill is built from this report; each recommendation
advances only if the director opens a Work Object for it. The strongest
candidate to advance first is `design-audit-accessibility`.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T14:51:21Z — Report deliverable produced and linked; awaiting director selection

- **State:** verify
- **Status:** active
- **Actor:** claude-code
- **Rationale:** alawas-research-produce-report produced a report-type deliverable recommending three hard-gap skills (design-audit-accessibility, design-critique-usability, design-govern-interaction-motion) plus three partial gaps, each attributed to a verified frontier gap in the design pipeline. Nothing built; each recommendation advances only on director selection.
## artifacts

- `.work-studio/deliverables/2026-08-22-027-design-pipeline-enhancement-skills.md` (fingerprint: `dcf36e721b44`, commit: uncommitted at record time) — Report: recommended additional design-pipeline skills, each grounded in a verified frontier gap
