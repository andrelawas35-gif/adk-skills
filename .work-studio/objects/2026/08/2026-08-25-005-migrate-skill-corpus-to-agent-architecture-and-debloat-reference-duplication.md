---
schema_version: 1
id: 2026-08-25-005
title: Migrate skill corpus to agent architecture and debloat reference duplication
type: project
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-25T23:28:26Z
updated_at: 2026-08-26T00:37:41Z
next_action: Route to alawas-engineering-verify-release-evidence: assess whether the tracer's own-scope evidence (pointer mechanism + core assembly + payload-boundary proof) is sufficient to close this design slice as verified-with-known-gaps, given the corpus-wide blocker is explicitly deferred rather than resolved.






















---
## Intent

Migrate the Work Studio skill corpus from duplicated flat files to an agent-based
architecture. The current system has ~50 unique skills duplicated into 349
physical SKILL.md copies across 7 locations (core, .agents, 5 adapters), with
331 shared reference document copies wasting ~45,000+ lines, and 250 near-identical
adapter projections. This project consolidates references to a single source of
truth, collapses adapter projections into generated views, slims each SKILL.md
by extracting boilerplate into agent-level defaults, creates `.claude/agents/`
definitions for domain-specialized agents, and rewires the orchestrator to spawn
agents instead of loading skills directly.

**Predecessor:** `2026-08-21-009` (closed — doc refinement subsumed by this scope).
**Builds on:** `2026-08-25-003` (complete — general orchestrator, now the routing spine).
**Consumes:** `2026-08-25-001` (adapter projection work feeds Phase 2).

## Success evidence

- [ ] Single `references/` directory holds all shared docs; zero copies in `.agents/skills/*/references/`
- [ ] Adapter directories (`adapters/claude-code/`, etc.) are gitignored and generated on demand
- [ ] Each SKILL.md reduced by ~20-30% — no inline consequence/authority, grilling, evidence, or capability-degradation boilerplate
- [ ] `.claude/agents/` contains definitions for all domain agents (orchestrator, conductor, grilling-engine, thinker, designer, engineer, operator, business-analyst, researcher, producer, reviewer)
- [ ] Orchestrator spawns domain agents via `Agent` tool instead of loading skills via `Skill` tool
- [ ] All existing skill routing tests (`test_orchestrator*.py`) still pass after migration
- [ ] No functional regression — every skill's governing principle, boundaries, stage workflow, and routing rules are preserved

## Constraints and non-goals

**Constraints:**
- Each SKILL.md must keep its irreducible core: frontmatter, governing principle, boundaries, inputs, stage workflow, routing, output template, self-check
- The `skills/core/` directory remains the canonical source of truth for skill logic
- `generate-adapters.py` must be updated to work with the new structure
- Agent definitions must declare which references they load — no implicit bundling
- The CLI (`tools/ws`) is unaffected — it operates on Work Objects, not skills

**Non-goals:**
- Rewriting skill logic or changing domain boundaries
- Migrating to a different AI coding platform
- Changing the Work Object schema or lifecycle states
- Building a runtime agent framework — this uses Claude Code's native `Agent` tool

## Decisions and revisit triggers

### Decision 1 — Supersede 2026-08-21-009

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | WO `2026-08-21-009` scope consumed by this broader migration |
| **Authorization** | Director confirmation ("close that one") |
| **Confidence** | high — doc refinement is a proper subset of agent migration |
| **Actor** | director |
| **Revisit trigger** | If doc-level refinements emerge that are unrelated to agent architecture |
| **Rationale** | The original WO identified the same duplication problem but scoped only to doc editing. This WO addresses the structural cause. |

### 2026-08-25T23:36:06Z — Sequence migration as reference/projection debloat first, agentization second

- **Branch chosen**: Consolidate shared references and generated adapter projections first while keeping `skills/core/` as the canonical behavior source; then design a small `.claude/agents/` pilot before corpus-wide agent migration.
- **Alternatives considered**: Full agent migration now, rejected because `.claude/agents/` is not present in this workspace and reference injection is not yet proven across platforms; design-domain split first, rejected because agent granularity depends on the reference-loading mechanism; defer migration, rejected because duplicated references and adapter projections are already measured waste.
- **Rationale**: Current repository evidence shows healthy adapter generation and real duplication pressure, while the agent/subagent path is still platform-specific and unproven for shared reference loading.
- **Trade-offs accepted**: Slower agent-architecture payoff in exchange for preserving cross-platform skill behavior and avoiding a whole-corpus migration before the loading pattern is proven.
- **Confidence**: high
- **Revisit trigger**: Reopen if a `.claude/agents/` pilot proves shared-reference loading and if Codex/OpenCode/LM Studio paths have equivalent dispatch or generation behavior.
- **Edge cases noted**: The branch handles duplicated references well but does not itself prove Claude-only subagent behavior; it assumes shared references can be injected without weakening skill adherence; generated adapters may need to remain committed until install/update tooling changes.
- **Actor**: human

### 2026-08-25T23:47:19Z — Accepted tracer design: one skill, one shared reference path, one generated adapter projection, one Claude agent pilot

- **Design type**: tracer bullet
- **Result**: pass
- **Scope**: `thinking-pressure-test-decision` as the pilot skill; one shared reference loading path; one generated adapter projection path; one minimal `.claude/agents` pilot boundary.
- **Riskiest assumption**: A shared-reference plus generated-projection path can reduce duplication without changing canonical `skills/core/` behavior or breaking platform adapter checks.
- **Bounded path**: Preserve `skills/core/` as the behavior source, introduce the smallest generator-controlled shared-reference path needed by the pilot, regenerate/check the affected adapter projection, and define a minimal Claude project-agent pilot that preloads only the relevant skill.
- **Authorization**: Director acceptance of the immediately preceding tracer-bullet recommendation; this records design and routes implementation only, with no corpus-wide migration, deployment, export, or destructive action authorized.
- **Failure behavior**: Treat generated adapter drift, missing shared reference resolution, changed core assembly, or unverified Claude agent loading as tracer failure; do not claim corpus migration or agent architecture viability from a partial pass.
- **Observability**: Evidence must include `tools/generate-adapters.py --check`, one core/adapter behavior-preservation diff or assembly check, and an explicit `.claude/agents` pilot boundary.
- **Non-goals**: No corpus-wide migration, no deletion of all adapter directories, no orchestrator rewiring, no domain-agent split, and no production runtime agent framework.
- **Rollback**: Remove pilot files and generator changes, regenerate adapters back to the current behavior, and leave `skills/core/` as the unchanged canonical source.
- **Exit criteria**: Pass if the pilot removes one duplicated reference path, preserves core skill behavior, regenerates the adapter projection cleanly, and documents the Claude agent pilot boundary; fail if any of those signals cannot be verified.
- **Next route**: `alawas-engineering-implement-bounded-change`
- **Revisit trigger**: Reopen design if the pilot cannot load shared references without weakening skill adherence or if adapter checks require committed duplicate reference files.
- **Actor**: human

### 2026-08-26T00:05:03Z — Add missing pressure-test core assembly contract

- **Branch chosen**: Add `skills/core/thinking-pressure-test-decision/contract.md` so `tools/generate-adapters.py --check-core-assembly thinking-pressure-test-decision` can verify the tracer's behavior-preservation path.
- **Alternatives considered**: Accept focused pointer tests only, rejected because the Work Object explicitly kept core assembly preservation as an observability path; broaden into stale conductor contract repair or unrelated production asset pipeline repair, rejected as outside this bounded pilot.
- **Rationale**: Verification proved the shared-reference pointer and Claude pilot boundary, but core assembly remained unverified only because the pilot contract file was absent.
- **Trade-offs accepted**: The pressure-test contract mechanically mirrors the current `SKILL.md` body for byte-identical assembly rather than completing a broader lean-authoring migration.
- **Confidence**: high
- **Revisit trigger**: Reopen if the pressure-test `SKILL.md` changes without updating its contract, or if core assembly begins requiring corpus-wide contract normalization.
- **Edge cases noted**: The generator-wide adapter check can still be blocked by unrelated invalid core skills; that blocker must not be mistaken for pressure-test contract failure.
- **Actor**: human

### 2026-08-26T00:20:19Z — Close single-reference pilot as scoped; next tracer targets multi-reference pointer resolution

- **Branch chosen**: Close this pilot slice as verified for its actual scope — one skill (`thinking-pressure-test-decision`), one shared-reference pointer (`CONSEQUENCE-AUTHORITY.md`). Do not claim the reference-pointer mechanism is validated corpus-wide. The next move is a second bounded tracer on `governance-conduct-work-object`, which references six shared documents (`CONSEQUENCE-AUTHORITY.md`, `AGREEMENT-LOOP.md`, `SKILL-AWARE-GRILLING.md`, `EVIDENCE-MODEL.md`, `DIRECTOR-LANGUAGE.md`, `MISSING-ARTIFACT-GAP.md`), to test whether the pointer mechanism generalizes past a single reference per skill before any batch rollout across the remaining 49 skills is authorized.
- **Alternatives considered**: Batch-rolling the one-reference pattern to all 50 skills now, rejected because the pilot only tested n=1 pointer per skill and most skills carry 3-6 references — extrapolating to batch scope risks discovering a multi-pointer failure mode only after many skills are queued behind it. A design-domain skill was also considered as the second pilot target (to test agent-granularity), rejected because agent granularity is a separate axis from reference-pointer resolution and does not test the actual untested risk; reference count, not domain, is the correct selection criterion.
- **Rationale**: The highest-leverage untested assumption is whether shared-reference-pointer resolution works when a skill has multiple pointers, not how many Claude agents the design domain should have. `governance-conduct-work-object` is the highest-reference-count skill in the corpus (6 pointers) and directly stress-tests the mechanism at its hardest known case, including the largest duplicated file (`SKILL-AWARE-GRILLING.md`, 691 lines x 47 copies).
- **Trade-offs accepted**: One more bounded implementation/verify cycle before the corpus-wide debloat pattern is trusted, in exchange for evidence grounded in the actual scaling risk rather than an easier proxy case.
- **Confidence**: high that a multi-reference pilot is more valuable evidence than closing outright; medium on `governance-conduct-work-object` specifically being the single best next candidate versus another high-reference-count skill.
- **Revisit trigger**: Reopen if the `governance-conduct-work-object` tracer reveals the pointer mechanism has a materially different failure mode than pointer-count scaling (e.g., ordering conflicts, merge collisions, or per-file pointer-worthiness that isn't uniform) — in that case the next tracer target and test design both need to change, not just proceed to a third skill.
- **Edge cases noted**: Not every reference on a skill is equally worth pointerizing — `MISSING-ARTIFACT-GAP.md` is short and may not carry the same duplication payoff as `SKILL-AWARE-GRILLING.md`; the next tracer should verify pointer-worthiness per reference, not assume uniform treatment. Also unresolved: whether passing this second pilot is sufficient to batch-roll, or whether a third pilot is needed — that decision is deferred to after this tracer's evidence exists, not decided now.
- **Actor**: human

### 2026-08-26T00:23:04Z — Accepted tracer design: multi-reference pointer migration for governance-conduct-work-object, scoped to the payload-boundary risk

- **Design type**: tracer bullet
- **Result**: pass
- **Scope**: Add all six `(governance-conduct-work-object, <filename>)` tuples to `tools/generate-adapters.py`'s `SHARED_REFERENCE_POINTER_PILOTS` in one implementation pass (CONSEQUENCE-AUTHORITY.md, AGREEMENT-LOOP.md, SKILL-AWARE-GRILLING.md, EVIDENCE-MODEL.md, DIRECTOR-LANGUAGE.md, MISSING-ARTIFACT-GAP.md). Author `skills/core/governance-conduct-work-object/contract.md` mirroring the pressure-test-decision pilot for `--check-core-assembly` verification. Regenerate all adapters and run `generate-adapters.py --check` plus the full `GeneratorContract` test suite. Specifically verify, as a named check, that a different skill still depending on the full `SKILL-AWARE-GRILLING.md` (`thinking-develop-idea`) still receives the complete file byte-unchanged in its generated adapter, not a pointer stub.
- **Riskiest assumption**: Grounded in direct reading of `tools/generate-adapters.py` (lines 40-94, 800-889): the pointer mechanism itself is a flat per-file lookup with no batching or ordering logic, so pointer count does not meaningfully increase risk for four of the six references. The real untested risk is narrower — whether pointer-izing `SKILL-AWARE-GRILLING.md` and `AGREEMENT-LOOP.md` specifically breaks their existing, separate payload-boundary scoping (`GRILLING_OVERLAY_REFS`) and the generated `epistemic-rules-full.md` tag-table excerpt mechanism, both of which other skills' epistemic references depend on.
- **Bounded path**: All 6 pointers in one pass rather than one-at-a-time, because the code evidence shows uniform low risk for 4 of the 6; the two grilling-overlay files are where a genuinely new interaction is being tested, and the `thinking-develop-idea` payload check targets exactly that interaction.
- **Authorization**: Director acceptance of the immediately preceding tracer-bullet recommendation ("accept"). Authorizes implementation and verification only — no corpus-wide rollout, no orchestrator rewiring, no deletion of adapter directories, consistent with this Work Object's standing constraints.
- **Failure behavior**: A `--check-core-assembly` failure for `governance-conduct-work-object` is treated as a contract-authoring gap, not a pointer-mechanism failure, and is fixable within scope (same pattern as the first pilot). If `thinking-develop-idea` (or any other grilling-dependent skill) loses its full `SKILL-AWARE-GRILLING.md` copy after this change, that is a genuine tracer failure — the payload boundary broke — and must be reported as fail, not papered over as partial success.
- **Observability**: `generate-adapters.py --check` output; `--check-core-assembly governance-conduct-work-object` output; full `GeneratorContract` test suite results; an explicit before/after diff confirming `thinking-develop-idea`'s generated `references/SKILL-AWARE-GRILLING.md` is byte-unchanged.
- **Non-goals**: No batch migration beyond this one skill. No new Claude agent definition (the first pilot's `.claude/agents/thinker-pressure-test-pilot.md` already covers that boundary). No pointer-worthiness scoring system — worthiness is judged qualitatively in the decision record, not built as new mechanism.
- **Rollback**: Remove the 6 tuples from `SHARED_REFERENCE_POINTER_PILOTS`, delete the new `contract.md`, regenerate adapters back to the current committed state.
- **Exit criteria**: Pass if all 6 pointers generate correctly, core assembly is byte-identical, full generator tests pass, and `thinking-develop-idea`'s grilling-file payload is provably unaffected. Fail if the payload boundary breaks for any other skill, or if `--check-core-assembly` cannot pass without misrepresenting `governance-conduct-work-object`'s actual behavior. Either result routes to implementation next — a clean, well-evidenced fail is still implementable as revert-plus-documentation.
- **Next route**: `alawas-engineering-implement-bounded-change`
- **Revisit trigger**: Reopen design if implementation reveals the payload-boundary and pointer mechanisms interact in a way not anticipated here (e.g., the tag-excerpt generation reads a pointer stub instead of real content for some other skill), or if `contract.md` authoring for a 6-reference skill proves materially harder than the 1-reference case.
- **Actor**: human

### 2026-08-26T00:37:08Z — Implementation complete on tracer's own scope; corpus-wide blocker left unblocked by director instruction

- **Branch chosen**: Implement the accepted tracer's bounded scope (6 pointer tuples, contract.md fix, targeted regeneration, payload-boundary verification) and record it as scope-complete-with-explicit-gaps, rather than deferring the whole tracer until an unrelated corpus-wide blocker is fixed. Director explicitly instructed: leave the blocker unblocked.
- **Alternatives considered**: Fix `production-operate-shot-pipeline`'s malformed Required-capabilities table now (same bounded-fix precedent as the earlier `production-operate-asset-pipeline` repair), rejected by director — leave it blocked. Recording nothing until the blocker clears was also implicitly rejected — the tracer's own scope has real, verified evidence worth persisting now.
- **Rationale**: The tracer's actual falsifiable risk — does pointer-izing SKILL-AWARE-GRILLING.md/AGREEMENT-LOOP.md for governance-conduct-work-object leak into other skills still depending on the full file — was directly tested and passed via diff-of-diffs proof (see Evidence ledger), independent of whether the corpus-wide `--check`/test-suite can currently run. The blocker is a pre-existing, unrelated, untracked skill defect, not a consequence of this tracer.
- **Trade-offs accepted**: This Work Object cannot yet claim the accepted design's full exit criteria (full `--check` and full GeneratorContract suite passing) are met. Two further gaps are also left unresolved: a stale test assertion contradicting the new pointer design, and two unrelated scope-creep diffs (PLATFORMS duplicate-opencode bug, universal-generator confirmation-text bleed) sitting uncommitted in the same working tree.
- **Confidence**: high on the payload-boundary property itself (proven by diff-of-diffs, not just a checksum comparison). Medium on overall tracer closure — the mechanism is verified sound, but full corpus-wide confidence remains blocked pending the shot-pipeline fix.
- **Revisit trigger**: Reopen when `production-operate-shot-pipeline`'s capabilities table is fixed (whether in this WO or a separate one) — at that point, re-run full `--check` and the GeneratorContract suite and update `test_pressure_test_decision_uses_one_shared_reference_pointer` (now stale, asserts governance-conduct-work-object is NOT a pointer pilot, which contradicts this accepted design). Also revisit if the PLATFORMS/duplicate-opencode and generate_adapter_section scope-creep diffs are ever committed unreviewed — they were found, not authorized, and remain untouched in the working tree.
- **Edge cases noted**: HEAD-based baselining (rather than working-tree baselining) was necessary because the canonical SKILL-AWARE-GRILLING.md source itself had +117 uncommitted lines of unrelated legitimate prior work at verification time — a literal byte-identity check against the working tree would have been meaningless.
- **Actor**: human

## Evidence ledger

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | Explore agent scan | 349 SKILL.md files across 7 locations; 50 unique skills |
| [system] | Explore agent scan | 331 reference doc copies from ~10 unique documents |
| [system] | Explore agent scan | SKILL-AWARE-GRILLING.md: 691 lines x 47 copies = ~32,000 wasted lines |
| [system] | Explore agent scan | 5 adapter dirs x 50 skills = 250 near-identical projections |
| [system] | Explore agent scan | .agents/skills/ copies are 30-50 lines larger than core (bundled refs) |
| [system] | Explore agent scan | 8 domains: thinking (7), governance (4), design (13), engineering (2), operations (2), business (15), research (2), production (4) |
| [system] | WO 2026-08-25-003 | General orchestrator complete — routing spine exists |
| [decision] | Director | Close 2026-08-21-009, superseded by this WO |
| [decision] | pressure-test-decision, director acceptance | Accepted recommendation: sequence migration as reference/projection debloat first while preserving skills/core as canonical behavior source, then design a small .claude/agents pilot before corpus-wide agentization. |
| [decision] | design-tracer-bullet, director acceptance | Accepted tracer design: pilot thinking-pressure-test-decision through one shared reference loading path, one generated adapter projection path, and one minimal .claude/agents boundary; no corpus-wide migration or orchestrator rewiring authorized. |
| [system] | codex implementation | Implemented accepted tracer: tools/generate-adapters.py emits a shared-reference resolver pointer for thinking-pressure-test-decision/CONSEQUENCE-AUTHORITY.md; regenerated adapter manifests and checksums; added .claude/agents/thinker-pressure-test-pilot.md as a read-only Claude agent pilot; focused unittest suite and generate-adapters --check passed; check-core-assembly remains an explicit gap because skills/core/thinking-pressure-test-decision/contract.md is absent. |
| [system] | codex verify-release-evidence | Verification executed for accepted tracer: generate-adapters.py --check passed with no drift across configured adapter platforms; focused unittest suite passed (6 tests); codex pilot pointer contains Shared Reference Pointer and canonical path, differs from canonical reference hash, and is 7 lines versus canonical 140 lines; non-pilot governance adapter reference hash matches canonical; .claude/agents/thinker-pressure-test-pilot.md declares Read/Grep/Glob only, model inherit, and skill alawas-thinking-pressure-test-decision. |
| [gap] | codex verify-release-evidence | Core assembly verification remains unverified: uv run --python 3.11 python tools/generate-adapters.py --check-core-assembly thinking-pressure-test-decision exits nonzero because skills/core/thinking-pressure-test-decision/contract.md is missing. This does not invalidate the generated adapter pointer checks, but it prevents claiming the core-assembly preservation path for the tracer. |
| [system] | codex contract repair | Added skills/core/thinking-pressure-test-decision/contract.md and extended tools/generate-adapters.py core assembly to support direct top-level contract sections, skip empty optional sections, and include Evidence rules when present. Verification passed: uv run --python 3.11 python tools/generate-adapters.py --check-core-assembly thinking-pressure-test-decision reported byte-identical assembly; direct import assertion confirmed the assembled pressure-test skill equals SKILL.md and includes the Evidence rules section. |
| [gap] | codex contract repair | Full generator unittest and generate-adapters --check are currently blocked before exercising this new regression because skills/core/production-operate-asset-pipeline exists in the core corpus but its Required capabilities section declares no backtick capability rows, raising ValueError: No required capabilities declared: production-operate-asset-pipeline. This appears outside the accepted thinking-pressure-test-decision contract repair scope. |
| [system] | codex next slice | Next slice repaired generator-wide blockers: converted production-operate-asset-pipeline Required capabilities from table to generator-recognized bullet declarations, added/confirmed required corpus-contract metadata for compact descriptions and Skill Grilling Profile coverage, added a generated high-consequence mutation floor, regenerated adapter projections, and verified generate-adapters --check plus full GeneratorContract tests. Asset pipeline tracer passed simulated mesh failure, resume, state transition, and persistence checks. |
| [system] | engineering-implement-bounded-change | SHARED_REFERENCE_POINTER_PILOTS extended with 6 governance-conduct-work-object tuples (CONSEQUENCE-AUTHORITY, AGREEMENT-LOOP, SKILL-AWARE-GRILLING, EVIDENCE-MODEL, DIRECTOR-LANGUAGE, MISSING-ARTIFACT-GAP). Only edit made to tools/generate-adapters.py. |
| [system] | engineering-implement-bounded-change | contract.md was stale relative to current SKILL.md (predated commit 68c1b2f's CLI-block relocation); fixed to reproduce current SKILL.md text exactly. --check-core-assembly governance-conduct-work-object now returns byte-identical MATCH. |
| [system] | engineering-implement-bounded-change | Payload-boundary property verified via diff-of-diffs: diff(HEAD canonical SKILL-AWARE-GRILLING.md, working-tree canonical) is line-for-line identical to diff(HEAD-baselined thinking-develop-idea adapter copy, regenerated copy) -- 118 lines each, identical content. Proves the pointer mechanism introduced zero additional changes to non-pilot skills; the only delta present is pre-existing unrelated WIP growth (+117 lines) in the canonical source itself. |
| [gap] | engineering-implement-bounded-change | Full `generate-adapters.py --check` and the entire GeneratorContract test suite are blocked by an untracked, unrelated skill: production-operate-shot-pipeline has a malformed Required-capabilities table (same failure class as the earlier production-operate-asset-pipeline bug, different skill). Director instruction: leave blocked, do not fix now. |
| [gap] | engineering-implement-bounded-change | test_pressure_test_decision_uses_one_shared_reference_pointer (tests/test_generate_adapters.py:333) is now stale: it hard-asserts governance-conduct-work-object's CONSEQUENCE-AUTHORITY.md equals full canonical text, contradicting this accepted design where that file is now also a pointer pilot. Confirmed via hash: regenerated file matches thinking-pressure-test-decision's pointer file, not canonical source. Needs updating once the suite is unblocked. |
| [gap] | engineering-implement-bounded-change | Two unrelated scope-creep diffs found uncommitted in the same working tree, investigated and left untouched: (1) PLATFORMS list adds lm-studio-bionic and a literal duplicate "opencode" entry (real bug, double-processes that platform); (2) generate_adapter_section gained 3 lines bleeding governance-conduct-work-object's confirmation-mutation policy text into the universal Platform Adapter section generator used by every skill on every platform. Neither authorized by this Work Object's accepted design. |
| [gap] | ws transition audit (verify) | Unresolved [gap] entries exist in the Evidence ledger. Residual uncertainty should be reviewed before proceeding. |
## Open questions

1. **Agent granularity for design domain** — 13 design skills mapped to one `designer` agent. Should accessibility/usability audits split into a separate `design-auditor` agent, or is one agent with selective skill loading sufficient?
2. **Grilling engine isolation** — Should the grilling engine be a standalone agent, or should each domain agent embed its own grilling capability with only the relevant profile section?
3. **Adapter generation timing** — Should adapters be generated at git pre-commit, CI, or on-demand only? Current `generate-adapters.py` runs manually.
4. **Reference loading mechanism** — How do agent definitions actually inject references? Claude Code agents don't have a `references:` frontmatter key today — the agent prompt must inline or read them. What's the practical pattern?

## Next move

Route to `alawas-thinking-pressure-test-decision`: decide whether the bounded
tracer evidence is sufficient to close this pilot slice and design the next
corpus-debloat tranche, without claiming full migration completion.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-25T23:28:39Z — Created

- **State:** notice
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Successor to 2026-08-21-009. Research complete: 349 SKILL.md copies from 50 unique skills, 331 reference doc duplicates (~45k wasted lines), 250 adapter projections. Five-phase plan: (1) extract shared references, (2) collapse adapter projections, (3) slim SKILL.md boilerplate, (4) create .claude/agents/ definitions for 10 domain agents, (5) rewire orchestrator to spawn agents. Domains: governance, engineering.
### 2026-08-25T23:31:42Z — Research complete, body populated with five-phase plan — transitioning to explore for pressure-testing phase sequencing and agent granularity

- **State:** explore
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Research phase produced comprehensive inventory (349 files, 331 ref copies, 8 domains, 50 skills). Plan drafted with 5 phases and 4 open questions. Next: pressure-test the phase order and agent boundaries before committing to build.
### 2026-08-25T23:36:38Z — Decision recorded: sequence migration as reference/projection debloat first, agentization second

- **State:** design
- **Status:** active
- **Actor:** codex
- **Rationale:** Director accepted pressure-test recommendation; design is now needed for the smallest shared-reference and agent-pilot tracer before implementation.
### 2026-08-25T23:37:03Z — Next move aligned with accepted pressure-test decision

- **State:** design
- **Status:** active
- **Actor:** codex
- **Rationale:** Body Next move now matches frontmatter: route to design-tracer-bullet for the debloat-first shared-reference and agent-pilot tracer.
### 2026-08-25T23:47:54Z — Accepted tracer design recorded and routed to implementation

- **State:** build
- **Status:** active
- **Actor:** codex
- **Rationale:** Director accepted the design-tracer-bullet recommendation; the next bounded step is implementation of the one-skill shared-reference, generated-adapter, and Claude-agent pilot.
### 2026-08-25T23:48:15Z — Next move aligned with accepted tracer implementation route

- **State:** build
- **Status:** active
- **Actor:** codex
- **Rationale:** Body Next move now matches frontmatter: route to implement-bounded-change for the accepted one-skill debloat and agent-pilot tracer.
### 2026-08-25T23:56:14Z — Implementation tracer complete; route to verification

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** Accepted one-skill tracer has been implemented with generator-controlled shared-reference pointer, regenerated adapter projections, read-only Claude agent pilot, and focused passing checks; remaining work is verification of evidence and explicit handling of the missing core assembly contract gap.
### 2026-08-25T23:56:30Z — Next move aligned with verification route

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** Body Next move now matches frontmatter: route to verify-release-evidence for the accepted tracer evidence, including pointer behavior, generated adapter manifests/checksums, Claude agent pilot boundary, and the explicit missing core-assembly contract gap.
### 2026-08-26T00:01:18Z — Verification complete with core-assembly gap

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** Accepted tracer evidence passed for generated adapter pointer behavior, manifests/checksums, focused tests, and Claude agent pilot boundary. Core assembly verification remains unavailable because skills/core/thinking-pressure-test-decision/contract.md is missing, so the next move is a bounded decision about adding that contract or accepting focused pointer tests as sufficient preservation evidence.
### 2026-08-26T00:05:48Z — Missing pressure-test contract added

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** Director chose the contract branch; the missing thinking-pressure-test-decision contract was added and its core assembly path now verifies byte-identically. Full generator checks remain blocked by an unrelated production-operate-asset-pipeline Required capabilities issue, so verification should classify that separately before any broader migration claim.
### 2026-08-26T00:16:40Z — Next slice verified

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** Cleared the recorded generator-wide blocker by repairing asset-pipeline capability metadata, completing missing grilling/profile and compact-description contract coverage, adding the generated high-consequence mutation floor, regenerating adapters, and passing serial drift, full generator contract, Claude pilot, and asset-pipeline tracer verification.
### 2026-08-26T00:20:43Z — Pilot slice closed as scoped; next tracer targets multi-reference pointer resolution on governance-conduct-work-object

- **State:** design
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Director accepted pressure-test recommendation: close the single-reference pilot (thinking-pressure-test-decision, 1 pointer) as verified for its actual scope, do not claim corpus-wide validation, and run a second bounded tracer on governance-conduct-work-object (6 reference pointers) to test whether the pointer mechanism generalizes before any batch rollout.
### 2026-08-26T00:23:25Z — Tracer design accepted for governance-conduct-work-object multi-reference pointer migration; routed to implementation

- **State:** build
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Director accepted the tracer-bullet recommendation: pointer-ize all 6 governance-conduct-work-object references in one pass, with the specific new risk being whether SKILL-AWARE-GRILLING.md/AGREEMENT-LOOP.md pointer-ization breaks the existing payload-boundary scoping that other grilling-dependent skills (e.g. thinking-develop-idea) rely on. No corpus-wide migration authorized.
### 2026-08-26T00:37:41Z — Tracer's own bounded scope implemented and verified; corpus-wide blocker left unblocked by director instruction

- **State:** verify
- **Status:** active
- **Actor:** claude-code
- **Rationale:** 6 pointer tuples added, contract.md fixed to byte-identical, payload-boundary property proven via diff-of-diffs (zero leakage into thinking-develop-idea despite unrelated +117-line WIP growth in the canonical source). Full --check and GeneratorContract suite remain blocked by an unrelated untracked skill (production-operate-shot-pipeline); director explicitly chose to leave this blocked rather than fix now. Three gaps recorded: the corpus blocker, a stale test assertion, and two untouched scope-creep diffs.
