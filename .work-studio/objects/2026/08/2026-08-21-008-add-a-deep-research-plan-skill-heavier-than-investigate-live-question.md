---
schema_version: 1
id: 2026-08-21-008
title: Add a deep-research/plan skill, heavier than investigate-live-question
type: inquiry
status: closed
state: close
consequence: meaningful
sensitivity: ordinary
domain: [governance, research]
created_at: 2026-08-21T14:47:57Z
updated_at: 2026-08-21T18:44:14Z
next_action: Route to alawas-engineering-implement-bounded-change (or director may want a further design-tracer-bullet pass specifically for the sub-question composition loop -- how many investigate-live-question calls, how they're sequenced/parallelized -- before the full skill file is authored) to write the actual research-produce-report SKILL.md












---
## Intent

Director's signal: "add deep research capabilities to live question skill
like the one from claude. skill will produce a large document providing
research or implementation plan. kind of a research/plan skill." Develop
directions for how this studio should get a capability comparable to
Claude's own "deep research" mode -- an agent that runs an extended,
multi-step investigation and produces one large, structured document (a
research report or an implementation plan), as distinct from
`investigate-live-question`'s current shape (answer one falsifiable
question with attributable evidence, update a Work Object, no standalone
artifact).

Two framings the director's wording leaves open, both worth exploring as
distinct directions rather than assumed: (1) extend/modify
`investigate-live-question` itself to grow this heavier mode; (2) add a new,
separate skill for it, leaving `investigate-live-question` as-is. The
signal names the first ("add... to live question skill") but the second is
a materially different, still-live option this Work Object should surface
rather than foreclose.

**Deliverable (Decision 4):** `.work-studio/deliverables/2026-08-21-008-phase7-plan-demo.md` -- the Decision 3 tracer-bullet draft, relocated per the accepted file-structure design.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] Four materially distinct directions generated and presented, each grounded in this studio's actual conventions (skill file structure, Work Object model, existing investigate-live-question boundaries)
- [x] Information gap surfaced: the anti-roadmap tension (Direction 4), resolved by Decision 1
- [x] Director selected Direction 2; recorded as Decision 2. Tracer bullet (Decision 3) confirmed its key assumption: producing a synthesized deliverable requires supersession-resolution across a whole trail and a distinct standalone-document identity, neither of which investigate-live-question's exit contract provides -- assumption holds, not just plausible
- [x] `skills/core/research-produce-report/SKILL.md` authored, adapters regenerated (23 skills, no drift), installed to `~/.claude/skills/` after explicit confirmation, verified invocable in this session


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

### Decision 1 — Implementation-plan output synthesizes already-accepted decisions; it does not author prospective architecture

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Resolves the Direction 4 tension before any of the four directions are selected. Whatever direction is chosen for this deep-research/plan capability, its "implementation plan" output mode is scoped as: synthesize only already-accepted Decisions and History entries from a Work Object (or a chain of successor Work Objects) into one structured document. It never authors new speculative architecture, roadmap items, or unaccepted future decisions. This does not select among Directions 1-3 -- it constrains what any of them may build for the "plan" half of the ask. |
| **Authorization** | Director: "Do recommended" -- consequence is `meaningful`, generic acceptance is sufficient authority at this level |
| **Confidence** | medium -- best branch given discoverable evidence (`design-tracer-bullet`'s explicit non-goal against roadmaps/frameworks, `develop-idea`'s anti-premature-convergence principle), but genuinely revisable: the missing fact is who actually reads this plan, which was not resolved, only named as a gap |
| **Actor** | director |
| **Revisit trigger** | If the plan's real audience turns out to be outside the Work Object trail entirely -- a stakeholder, collaborator, or team who will never read Decisions/History sections -- this decision should be revisited toward the rejected Branch C (a genuine prospective plan document, built as an explicit, governed departure from the anti-roadmap principle, likely warranting its own ADR at that point since it would be hard-to-reverse as a habit, surprising, and a real trade-off) |
| **Rationale** | The only branch of three that produces an implementation-plan deliverable without quietly violating a principle this studio's other skills (`design-tracer-bullet`, `develop-idea`) already enforce. Rejected Branch A (drop "plan" from scope) because it unilaterally narrows the director's actual request without evidence that narrowing is correct. Rejected Branch C (genuine prospective plan) because it directly conflicts with an existing deliberate design principle and would need its own separately-scoped governance decision, not bundled into this one. |

**Edge case noted:** a Work Object chain with many messy or superseded decisions (some reversed, some abandoned mid-course) may synthesize into a confusing document rather than a clean plan -- the synthesis logic, when designed, needs to handle supersession explicitly, not just concatenate every Decision record in order.

**Assumption that would invalidate this choice if wrong:** that Decisions/History sections across this studio's Work Objects contain enough forward-looking framing (next_action, revisit triggers, open questions) to read as a usable plan rather than only a backward-looking justification log. Untested.

### Decision 2 — Selected Direction 2: a new sibling skill with a deliverable exit contract

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Build a new, separate skill (working name: `research-produce-report`) rather than extending `investigate-live-question` in place (Direction 1) or solving this purely at the orchestration/Artifact layer (Direction 3). The new skill composes `investigate-live-question` internally -- calling it per sub-question -- but has its own exit condition: a deliverable produced (a research report or, per Decision 1, a decisions-synthesis implementation plan), not a single falsifiable question answered/reframed/prototype-ready/unresolved. Still anchored to a Work Object for evidence and provenance, consistent with every other skill in this studio. |
| **Authorization** | Director: "Direction 2" |
| **Confidence** | medium -- Direction 2's own key assumption (that the studio genuinely needs a second exit contract, not just a longer version of the first) has not yet been reality-tested; that is exactly what routes next to design-tracer-bullet |
| **Actor** | director |
| **Revisit trigger** | If design-tracer-bullet's reality test shows this new skill's "done" state collapses into "a very long answered outcome" with no genuine structural difference from investigate-live-question, revisit toward Direction 1 (extend in place) instead |
| **Rationale** | Director's direct selection among the three neutrally-presented directions; no additional rationale was volunteered beyond the selection itself. |

### Decision 3 — Accepted tracer bullet: hand-draft a synthesis-only implementation plan from 2026-08-21-004's trail

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Test Decision 2's riskiest assumption by hand, without writing any skill code: draft one deliverable document in the scratchpad -- a synthesis-only "implementation plan" built from `2026-08-21-004`'s (Phase 7) existing Decisions and History sections, following Decision 1's constraint (synthesis only, no prospective authoring). No new skill file, no Work Object mutation, no orchestration, no published Artifact. |
| **Authorization** | Director: "Yes, use 2026-08-21-004" |
| **Confidence** | medium -- the exercise itself is low-risk and cheap to run; what's uncertain is the *result*, which is exactly what this tracer bullet exists to find out |
| **Actor** | director |
| **Revisit trigger** | If the finished draft is indistinguishable in content/structure from what could already be written as one long `answered` outcome inside a Work Object body, Decision 2's assumption fails and this Work Object revisits toward Direction 1 instead of proceeding to build a new skill |
| **Rationale** | Cheapest possible reality test for "is a deliverable-produced exit contract genuinely distinct" -- reuses real material already in this session (`2026-08-21-004`'s rich Decisions/History trail) rather than inventing a synthetic test case, and costs nothing to roll back (delete the scratch draft). |

### Decision 4 — Accepted tracer bullet: deliverable documents live at .work-studio/deliverables/<id>-<slug>.md, linked not duplicated

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Relocate the Decision 3 draft into `.work-studio/deliverables/2026-08-21-008-phase7-plan-demo.md`, linked from this Work Object's body by one line rather than embedded inline. Tests whether a deliverable living inside `.work-studio/` (no export, no Artifact publish, no new studio-wide convention formalized yet) is sufficient, versus needing something shareable outside the repo. No full `SKILL.md` authored at this step. |
| **Authorization** | Director: "Yes, that's sufficient" |
| **Confidence** | high that the file-identity mechanics work (this is a plain file write inside the conductor's existing write authority); the open question was audience/sufficiency, which the director just resolved directly rather than needing the file relocated first |
| **Actor** | director |
| **Revisit trigger** | If a future real use of this skill needs the deliverable handed to someone outside the Work Object trail entirely (a stakeholder, external collaborator), revisit toward export/Artifact-publishing as an explicit, separately-authorized addition -- not assumed to already be covered by this decision |
| **Rationale** | Director confirmed directly that a `.work-studio/`-resident file satisfies "a large document" for their purposes, without needing the relocation actually run first -- accepted as sufficient evidence given the question was about audience/sufficiency, not file-write mechanics (which carry no real uncertainty). |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | this session: Read 2026-08-21-004 in full; Write scratchpad/phase7-synthesis-plan-draft.md; compare draft against source Decisions/History for traceability | Decision 3's tracer bullet executed: hand-drafted a synthesis-only implementation-plan document from 2026-08-21-004's full Decisions (1-3) and History (7 entries) in the scratchpad, per Decision 1's constraint. Producing a correct draft required two things investigate-live-question's exit contract (answered/reframed/prototype-ready/unresolved, one hypothesis against one evidence body) does not do: (1) supersession resolution across an entire time-ordered trail -- 2026-08-21-004's own stale ## Next move section (written mid-session, describing a schema-change-first plan later overturned by Decisions 2 and 3) had to be actively detected and dropped, keeping only what the final Decisions/History arc actually supports, rather than surfaced as a single contradiction between one hypothesis and one evidence body; (2) a distinct deliverable identity -- a document meant to be read start-to-finish by someone who never opens the Work Object, versus content living inside a Work Object body. Both gaps are genuine and were not designed-in to justify Decision 2 -- they emerged from actually doing the exercise. |
| [system] | this session: mkdir .work-studio/deliverables; cp scratchpad draft into it; ls -la; direct edit to 2026-08-21-008 Intent section | Decision 4 implemented: created .work-studio/deliverables/ (new directory, first entry), copied the Decision 3 draft to .work-studio/deliverables/2026-08-21-008-phase7-plan-demo.md (3008 bytes), linked from this Work Object's Intent section with one line rather than embedding the content inline. Scratchpad original left in place as the pre-relocation record. git status will show .work-studio/deliverables/ as a new untracked path -- not yet committed, consistent with this session's pattern of leaving commits to explicit director request. |
| [system] | this session: Write skills/core/research-produce-report/SKILL.md; python3.13 tools/generate-adapters.py --check (before and after); python3.13 tools/generate-adapters.py; bash tools/install.sh --platform claude-code --global --dry-run; bash tools/install.sh --platform claude-code --global; ls ~/.claude/skills/alawas-research-produce-report/ | Wrote skills/core/research-produce-report/SKILL.md (canonical core, ~200 lines), implementing Decisions 1-4: composes investigate-live-question per sub-question for report-type deliverables, reads a source Work Object's Decisions/History directly for plan-type deliverables (no re-investigation), resolves supersession explicitly, writes to .work-studio/deliverables/<id>-<slug>.md, links rather than duplicates. Ran python3 tools/generate-adapters.py --check first (confirmed drift: MISSING for the new skill, matching expectation), then python3 tools/generate-adapters.py (regenerated claude-code and github-copilot adapters, 22 -> 23 skills), then --check again (All generated files match, no drift). Ran tools/install.sh --platform claude-code --global --dry-run first, then for real after explicit director confirmation (this is a write outside the repo, to the home-directory global skill location -- flagged and confirmed before running, not done silently). Verified: ~/.claude/skills/alawas-research-produce-report/ now exists with SKILL.md, capabilities/, references/, and the skill is listed as invocable in this session's available-skills. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

<!-- The single next action this Work Object routes to. -->

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-21T14:48:19Z — create-and-activate

- **State:** explore
- **Status:** active
- **Actor:** director
- **Rationale:** Director wants a deep-research/plan capability comparable to Claude's own deep research mode, producing a large document (research report or implementation plan) -- distinct from investigate-live-question's current answer-one-question-inline-in-a-Work-Object shape. Framed as an Inquiry in explore state for divergent direction generation before any design or implementation.
### 2026-08-21T14:51:46Z — decision-recorded-plan-scope-synthesis-not-prospective

- **State:** explore
- **Status:** active
- **Actor:** director
- **Rationale:** Pressure-tested the Direction 4 tension before any direction selection. Decided (Decision 1): whichever direction is eventually chosen, the implementation-plan output mode synthesizes only already-accepted Decisions/History, never authors prospective architecture -- reconciles the ask with design-tracer-bullet's and develop-idea's existing anti-roadmap principles. Director: do recommended (meaningful consequence, generic acceptance sufficient). This scopes the ask; it does not yet select among Directions 1-3.
### 2026-08-21T14:52:51Z — direction-2-selected

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Director selected Direction 2 (Decision 2): a new sibling skill (research-produce-report) with its own deliverable exit contract, composing investigate-live-question internally, bounded by Decision 1's synthesis-only plan scope. Single direction selected, so transitioning explore -> design per develop-idea's routing rules.
### 2026-08-21T14:55:19Z — tracer-bullet-accepted-route-to-implement

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director accepted Decision 3's tracer bullet: hand-draft a synthesis-only implementation plan from 2026-08-21-004's Decisions/History trail, testing whether Decision 2's deliverable-produced exit contract is genuinely distinct from investigate-live-question's answered exit contract. Routing to implement-bounded-change to actually run the exercise -- design-tracer-bullet does not implement.
### 2026-08-21T14:57:31Z — tracer-bullet-confirmed-assumption-holds

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Decision 3's tracer bullet ran: hand-drafted a synthesis-only implementation plan from 2026-08-21-004's trail. Two genuine structural gaps found versus investigate-live-question's exit contract -- supersession resolution across a whole time-ordered trail (the source WO's own stale Next move section had to be detected and dropped), and a distinct standalone-document deliverable identity. Decision 2's assumption (a new skill with its own exit contract is genuinely needed, not just a longer answered outcome) holds. All three Success evidence items now met.
### 2026-08-21T14:58:00Z — return-to-design-for-skill-file-structure

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Director chose to design the new skill's own file structure next (exit-contract wording, composition of investigate-live-question calls, deliverable-document placement) rather than skip straight to implementation. Returning to design state for design-tracer-bullet's next bounded slice.
### 2026-08-21T15:00:01Z — accepted-deliverable-location-route-to-implement

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director accepted Decision 4's tracer bullet directly: a .work-studio/deliverables/ file, linked not embedded, satisfies 'a large document' without needing the relocation actually run first. Routing to implement-bounded-change to perform the accepted relocation and confirm the pattern before the full research-produce-report skill file is authored.
### 2026-08-21T15:00:52Z — deliverable-location-implemented-verified

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Decision 4 implemented: .work-studio/deliverables/2026-08-21-008-phase7-plan-demo.md created, linked from this Work Object's Intent section. File structure for the new research-produce-report skill is now bounded on all fronts: content scope (Decision 1), skill identity (Decision 2, confirmed by Decision 3), and deliverable location (Decision 4). Nothing left to design-tracer-bullet before authoring the real SKILL.md.
### 2026-08-21T18:44:14Z — Closed: All four Success evidence items met. Directions generated and neutrally presented; anti-roadmap tension surfaced and resolved (Decision 1); Direction 2 selected and its key assumption confirmed by a real tracer bullet, not assumed (Decisions 2-3); deliverable-location design accepted and demonstrated (Decision 4); the actual research-produce-report skill authored, adapters regenerated with no drift, and installed to ~/.claude/skills/ after explicit confirmation for the outside-repo write. Verified invocable in this session.

- **State:** close
- **Status:** closed
- **Actor:** director
- **Rationale:** All four Success evidence items met. Directions generated and neutrally presented; anti-roadmap tension surfaced and resolved (Decision 1); Direction 2 selected and its key assumption confirmed by a real tracer bullet, not assumed (Decisions 2-3); deliverable-location design accepted and demonstrated (Decision 4); the actual research-produce-report skill authored, adapters regenerated with no drift, and installed to ~/.claude/skills/ after explicit confirmation for the outside-repo write. Verified invocable in this session.
