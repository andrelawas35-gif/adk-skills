# Documentation Classification Map — 2026-08-15-010 (slice 1)

Read-only classification of 64 documentation files across `references/`
(21 files), `docs/` (39 files), and the repo root (4 files), per the scope
given to this Work Object's first bounded slice. Excluded from this pass:
`skills/*/SKILL.md`, `.work-studio/objects/**`, and the two YAML config
files under `references/epistemic/` (noted below, not classified). No file
was moved, renamed, or edited; this document is the only artifact produced.

## Classification table

| File | Lines | Classification | Canonical owner (if not self) | Notes |
|---|---|---|---|---|
| references/AGREEMENT-LOOP.md | 390 | governance (conversational-engine rules) + domain model (provenance tags) | self (tags also defined here, see Duplication) | Defines the 6-tag provenance taxonomy (lines 98–111) that EVIDENCE-MODEL.md explicitly cites as canonical. Mixed-purpose: engine mechanics (runtime/orchestration-flavored) plus authority-adjacent rules (convergence/authority in final section). Borderline **runtime/orchestration** for the turn-loop/mode mechanics, **governance** for authority/convergence sections. |
| references/CAPABILITY-DEGRADATION.md | 89 | governance | self | Defines tiers, required behaviors, and disclosure rules — an institutional-control document (what an adapter is permitted to claim). |
| references/CONSEQUENCE-AUTHORITY.md | 140 | governance | self | The apparent single canonical authority-policy owner (see Duplication/Misplacement sections — largely confirmed, with caveats). |
| references/DIRECTOR-LANGUAGE.md | 66 | agent-facing rule | self | Presentation/behavior instruction for the agent, explicitly scoped ("governs presentation only... never changes what is true"). |
| references/DRIFT-AND-DEBT-TAXONOMY.md | 180 | domain model/schema | self | Defines 16 named failure-shape classes (a classification schema) with worked examples; not a decision-rights document. |
| references/EVIDENCE-MODEL.md | 81 | domain model/schema | self | Defines how evidence entries attach to the ledger; explicitly defers tag taxonomy to AGREEMENT-LOOP.md, avoiding duplication by cross-reference. |
| references/MISSING-ARTIFACT-GAP.md | 39 | constitution | self | Short, durable, system-wide behavioral invariant ("do not fabricate"); self-describes as extracted from WORKSPACE-DOCUMENTATION-CONTRACT.md by design (see ADR 0021). |
| references/SKILL-AWARE-GRILLING.md | 449 | agent-facing rule | self | Per-skill operating profiles (gates, escalation, pressure scenario) for an executing agent; large but single-purpose catalogue. |
| references/WORK-OBJECT.md | 145 | domain model/schema | self | Defines the Work Object schema, identity rules, storage, and body sections — "what things exist and what do they mean." |
| references/architecture/epistemic-graph-loop-system-improvement-architecture.md | 1154 | reference/explanation | — | Research/proposal document ("Repository-grounded research and implementation guidance"); proposes schema/CLI/graph changes not yet accepted as canonical. Large — candidate for research/proposal debt (see DRIFT-AND-DEBT-TAXONOMY class 15) but that classification is out of scope here. |
| references/architecture/langgraph-local-runtime-integrated-build-plan.md | 477 | reference/explanation | — | Proposed build plan for a future runtime; explicitly proposal-stage, not enacted. |
| references/constraints/constraint-driven-studio-operating-system-research-and-applied-architecture.md | 1855 | reference/explanation | — | Largest file in scope. Deep-research report proposing a constraint taxonomy, director contract, and orchestration model. Contains a "Director Decision Card" and "Director operating model" section that **overlaps** in subject with CONSEQUENCE-AUTHORITY.md and work-studio-director-system-reference.md — see Duplication section. |
| references/director/director-curriculum-for-epistemic-creative-technology-studio.md | 731 | reference/explanation | — | A 24-week training curriculum; clearly reference material, not a rule the system enforces. |
| references/director/work-studio-director-system-reference.md | 1226 | reference/explanation | — | Large synthesized reference guide for the director. Verified by direct read (§9–10) that it **cites and links** CONSEQUENCE-AUTHORITY.md, AGREEMENT-LOOP.md, and EVIDENCE-MODEL.md rather than restating their rules independently — it summarizes and cross-references, it does not duplicate verbatim. Genuinely mixed-purpose (glossary + operating rhythm + architecture commentary), fitting the "reference/explanation" category by design. |
| references/epistemic/epistemic-engineering-research-and-applied-architecture.md | 1380 | reference/explanation | — | Research report defining a proposed epistemic ontology, claim/decision lifecycles, and threat taxonomy — proposal-stage, not the system's enforced rule. |
| references/epistemic/epistemic-rules-essential.md | 17 | agent-facing rule | — (conflicts with epistemic-rules-full.md and AGREEMENT-LOOP.md) | Defines a **3-tag** system (`[system]`, `[decision]`, `[inference]`) as "the" tag system a skill must use. This directly conflicts with the 6-tag system in AGREEMENT-LOOP.md/EVIDENCE-MODEL.md — see Duplication/Contradiction. |
| references/epistemic/epistemic-rules-full.md | 19 | agent-facing rule | — (near-duplicate of AGREEMENT-LOOP.md tags) | Defines the same 6-tag system as AGREEMENT-LOOP.md lines 98–111, restated independently rather than by cross-reference — see Duplication. |
| references/epistemic/lint-allowlist.yaml | — | not classified, config | — | Skipped per scope. |
| references/epistemic/taxonomy.yaml | — | not classified, config | — | Skipped per scope; referenced by work-studio-director-system-reference.md as a mirror of the provenance tag set. |
| references/shared/consequence-authority-preamble.md | 1 | agent-facing rule (pointer) | references/CONSEQUENCE-AUTHORITY.md | One line: "Apply `references/CONSEQUENCE-AUTHORITY.md`." A pure include-pointer, not independent content — correctly avoids duplication. |
| references/shared/director-language-preamble.md | 9 | agent-facing rule (near-duplicate summary) | references/DIRECTOR-LANGUAGE.md | Restates DIRECTOR-LANGUAGE.md's rule in condensed prose rather than a bare pointer — see Duplication (minor/low-risk, summary-style). |
| references/shared/grilling-entry-preamble.md | 3 | agent-facing rule (pointer) | references/AGREEMENT-LOOP.md | Pointer plus one added behavioral clause (nomination threshold gate); mostly a pointer. |
| references/shared/work-object-updates-preamble.md | 1 | agent-facing rule (pointer) | conduct-work-object skill | One line, pure pointer. |
| docs/adr/0001–0025 (25 files) | 3–191 each | governance (decision records) | self, individually | As a group: Architecture Decision Records — by nature "who decided what, under which conditions, and why," i.e. governance-class decision records, each independently accepted and dated. Outlier: **ADR 0021** ("extract-behavioral-rule-from-workspace-documentation-contract-into-constitution-file", 161 lines) is itself the acceptance record for MISSING-ARTIFACT-GAP.md's existence — a governance record *about* constitution-file scoping, not a constitution file itself. **ADR 0025** (191 lines, canonical-runtime-truth-boundary-and-single-writer-rule) is unusually long and reads closer to an architecture spec than a typical trade-off record — flagged as ambiguous below. |
| docs/design/authority-sensitivity-component-plan.md | 262 | reference/explanation (historical design record) | — | Findings/contradictions/decisions/component-design structure — a point-in-time design artifact that fed later ADRs, not currently-enforced policy. |
| docs/design/capability-degradation-component-plan.md | 287 | reference/explanation (historical design record) | — | Same structure/purpose as above; predates and informed references/CAPABILITY-DEGRADATION.md. |
| docs/design/claude-design-mcp-integration-plan.md | 238 | reference/explanation (historical design record) | — | Integration plan document; 25-decisions log. |
| docs/design/deterministic-cli-component-plan.md | 294 | reference/explanation (historical design record) | — | Predates and informed the `ws` CLI described in WORK-OBJECT.md. |
| docs/design/evidence-model-component-plan.md | 337 | reference/explanation (historical design record) | — | Predates and informed references/EVIDENCE-MODEL.md. |
| docs/design/grilling-session-7-evidence-model.md | 625 | reference/explanation (session transcript/ledger) | — | A recorded grilling-session ledger (Observed/Claimed/Inferred/Decided), the working material behind evidence-model-component-plan.md — largest of the grilling-session files. |
| docs/design/grilling-session-8-authority-sensitivity.md | 179 | reference/explanation (session transcript/ledger) | — | Same pattern, feeding authority-sensitivity-component-plan.md. |
| docs/design/grilling-session-9-deterministic-cli.md | 105 | reference/explanation (session transcript/ledger) | — | Same pattern, feeding deterministic-cli-component-plan.md. |
| docs/design/grilling-session-10-capability-degradation.md | 172 | reference/explanation (session transcript/ledger) | — | Same pattern, feeding capability-degradation-component-plan.md. |
| docs/design/grilling-session-11-platform-adapters.md | 104 | reference/explanation (session transcript/ledger) | — | Same pattern, feeding platform-adapters-component-plan.md. |
| docs/design/platform-adapters-component-plan.md | 276 | reference/explanation (historical design record) | — | Findings on adapter-generation pipeline. |
| docs/design/shared-protocols-component-plan.md | 268 | **ambiguous / misplacement flag** | — | Filename says "constitution" but content structure (current-state findings → contradictions → accepted decisions → migration steps) matches every other `*-component-plan.md` file exactly. This is a component plan, not a constitution-class file — filename does not match content. See Misplacement section. |
| docs/personal-institution-work-studio-protocol-spec.md | 91 | domain model/schema + governance (mixed) | — | Defines the Personal Institution↔Work Studio protocol boundary (what an Evidence Bridge is, user-story-level) and some implementation/testing decisions — genuinely mixed-purpose. |
| docs/verification/codex-installed-workflow-evidence.md | 108 | project-specific state (out of scope) / reference | — | This is verification evidence for a specific installed-workflow run — arguably "project-specific state" territory even though it lives outside `.work-studio/objects/`. Flagged rather than force-classified. |
| docs/work-studio-planning-session-2026-07-15.md | 493 | reference/explanation (historical planning record) | — | README.md calls this "the accepted system design" — it is the original planning record the current architecture derives from; historical acceptance record, not live-enforced policy text itself. |
| CLAUDE.md | 9 | agent-facing rule (pointer) | references/DIRECTOR-LANGUAGE.md | Root instruction file; entirely a pointer to DIRECTOR-LANGUAGE.md plus one summary line. |
| CONTEXT.md | 225 | domain model/schema | self | Canonical glossary/domain-context file per WORKSPACE-DOCUMENTATION-CONTRACT.md's own registry (`type: domain-context`). Textbook domain model file — "what things exist and what do they mean." |
| README.md | 178 | reference/explanation | self | Repository overview/onboarding document: architecture map, install instructions, contributing guide. Not a rule the system enforces. |
| WORKSPACE-DOCUMENTATION-CONTRACT.md | 178 | governance | self | Defines artifact ownership, creation authority, stage triggers, and the sole-custodian rule for documentation mutation — decision-rights/institutional-control by definition. Also functions partly as domain model/schema (the registry itself enumerates artifact *types*), genuinely dual-purpose but governance is the dominant kind of truth it owns (who may create/mutate what). |

## Duplication found

1. **Provenance-tag taxonomy defined in three places with different scope.**
   - `references/AGREEMENT-LOOP.md` lines 98–111 define the 6-tag system
     (`[system]`, `[decision]`, `[memory]`, `[testimony]`, `[inference]`,
     `[gap]`) and are explicitly cited by `references/EVIDENCE-MODEL.md`
     (its own header, lines 4–7) as "the single authoritative source for tag
     definitions."
   - `references/epistemic/epistemic-rules-full.md` (19 lines) independently
     restates the same 6-tag table almost verbatim, rather than pointing to
     AGREEMENT-LOOP.md.
   - `references/epistemic/epistemic-rules-essential.md` (17 lines) defines
     a **different, incompatible 3-tag system** and states it is what "this
     skill" must use, collapsing `[gap]`, `[testimony]`, `[memory]` into
     `[inference]`.
   - This is genuine duplication (epistemic-rules-full.md vs.
     AGREEMENT-LOOP.md) plus a live **contradiction** (epistemic-rules-full.md
     vs. epistemic-rules-essential.md) about how many tags exist and which
     is canonical. Neither epistemic-rules-*.md file cites AGREEMENT-LOOP.md
     or EVIDENCE-MODEL.md as the source of truth the way EVIDENCE-MODEL.md
     itself does.

2. **Authority/consequence policy restated across multiple documents at
   varying depth**, checked specifically per this task's instruction:
   - `references/CONSEQUENCE-AUTHORITY.md` is the fullest, most detailed
     version (140 lines: levels, gates table, authority modes, structured
     History-entry format, the "five auditable-but-not-preventable
     categories").
   - `references/director/work-studio-director-system-reference.md` §10
     (lines 487–549, read directly) **summarizes** the same material with a
     mermaid flowchart and explicit inline citations back to
     `CONSEQUENCE-AUTHORITY.md` — this is compression-with-citation, not
     independent restatement, so it does not count as true duplication, but
     it is close enough to the line that a reader could mistake it for a
     second source of record.
   - `references/constraints/constraint-driven-studio-operating-system-research-and-applied-architecture.md`
     §3 ("Director operating model," "Director contract," "Director
     Decision Card") was not read in full line-by-line (1855 lines, header
     scan only) but its section titles closely parallel the authority-gate
     subject matter. **Not confirmed as duplicate or distinct — flagged
     below as needing a closer read before any duplication claim is made.**
   - `CLAUDE.md` and `WORKSPACE-DOCUMENTATION-CONTRACT.md` do **not**
     restate authority/consequence policy — confirmed by direct read.
     `CLAUDE.md` is a pure DIRECTOR-LANGUAGE pointer; the contract governs
     documentation-mutation authority specifically (a narrower, non-
     overlapping rule set), not the general consequence/authority gates.
   - Conclusion on the task's specific question: `references/CONSEQUENCE-AUTHORITY.md`
     **is** the fullest canonical authority-policy owner among files directly
     verified; other files either point to it, cite-and-summarize it, or
     govern a disjoint narrower authority (documentation mutation). The one
     unresolved case is the constraints research document, flagged below.

3. **`shared/director-language-preamble.md` vs. `DIRECTOR-LANGUAGE.md`** —
   the preamble is a condensed restatement (9 lines) rather than a bare
   pointer like the other three `shared/*-preamble.md` files (1–3 lines
   each). Low-risk (short, clearly subordinate), but inconsistent with the
   pattern the other three preambles use.

4. **Design-decision material duplicated across a plan and its grilling
   session** — each `docs/design/*-component-plan.md` file's "Accepted
   Decisions" section is, by construction, drawn from its corresponding
   `grilling-session-N-*.md` file's "Decisions Log." This is expected
   provenance (ledger → plan), not accidental duplication, but it means the
   same decision text exists in two files by design.

## Misplacement found

1. **`docs/design/shared-protocols-component-plan.md`** — filename claims
   "constitution" but its actual structure (current-state findings →
   contradictions/risks → accepted decisions → target component boundary →
   migration steps → tests required) is identical to every other
   `*-component-plan.md` file in the same directory. Nothing in the file
   itself reads as a durable, system-wide constitutional principle in the
   sense this audit uses the term (contrast with the genuinely constitution-
   class `references/MISSING-ARTIFACT-GAP.md`). The filename's implied
   purpose does not match the content found.

2. **`references/constraints/constraint-driven-studio-operating-system-research-and-applied-architecture.md`
   §3 "Director operating model" / "Director contract" / "Director Decision
   Card"** (lines 122–219 per header scan, not read in full) — potentially
   contains a restated or extended authority/decision-rights model that
   would belong in or alongside `CONSEQUENCE-AUTHORITY.md` if accepted, or
   is pure proposal content if not. Cannot confirm misplacement vs. correct
   placement (proposal document proposing a *new* director contract) without
   a full read — flagged in Ambiguous section rather than asserted.

3. No other large governance-shaped block was found embedded in a file
   classified as reference/explanation among the files read in full
   (AGREEMENT-LOOP.md, CONSEQUENCE-AUTHORITY.md, WORK-OBJECT.md,
   EVIDENCE-MODEL.md, CAPABILITY-DEGRADATION.md, MISSING-ARTIFACT-GAP.md,
   DRIFT-AND-DEBT-TAXONOMY.md, SKILL-AWARE-GRILLING.md, all four
   `shared/*-preamble.md` files, both `epistemic-rules-*.md` files,
   CLAUDE.md, CONTEXT.md, README.md, WORKSPACE-DOCUMENTATION-CONTRACT.md).

## Ambiguous / flagged for review

- **`references/AGREEMENT-LOOP.md`** — ambiguous: governance vs.
  runtime/orchestration, because the file is simultaneously (a) the
  turn-by-turn conversational engine mechanics (serial-depth/breadth-sweep
  modes, turn contract, checkpoint timing — orchestration-shaped) and (b)
  authority-adjacent convergence/action-authority rules in its final third
  (who may declare convergence, what authority a checkpoint needs —
  governance-shaped). It also independently hosts the provenance-tag
  taxonomy (domain-model-shaped). Not split into separate files, so no
  single category fits cleanly.

- **`docs/adr/0025-canonical-runtime-truth-boundary-and-single-writer-rule.md`**
  (191 lines) — ambiguous: governance (ADR) vs. constitution, because at
  191 lines it is unusually long for a trade-off record and its title
  ("canonical runtime truth boundary," "single-writer rule") reads like a
  durable system-wide invariant rather than a one-time accepted trade-off.
  Not read in full; flagged rather than reclassified.

- **`docs/verification/codex-installed-workflow-evidence.md`** — ambiguous:
  reference/explanation vs. project-specific state (which was declared out
  of scope for this slice as "`.work-studio/objects/**`" specifically, not
  "anything evidencing a specific run"). This file records evidence from one
  specific installation/run rather than a durable rule or schema. Flagged
  rather than force-classified into an out-of-scope bucket by a path
  technicality.

- **`references/constraints/constraint-driven-studio-operating-system-research-and-applied-architecture.md`**
  (1855 lines, largest file in scope) and
  **`references/epistemic/epistemic-engineering-research-and-applied-architecture.md`**
  (1380 lines) — both classified reference/explanation on the strength of a
  header scan plus their framing ("Deep research and applied architecture
  for Work Studio", "Research and applied architecture") rather than a full
  line-by-line read. Given their size, a full read was out of this bounded
  slice's budget. Flagged so a follow-up slice can confirm no governance-
  or constitution-class content is embedded and mistakenly left
  unclassified as "research."

- **`references/director/director-curriculum-for-epistemic-creative-technology-studio.md`**
  and **`references/director/work-studio-director-system-reference.md`** —
  both classified reference/explanation; work-studio-director-system-reference.md
  was spot-checked in full for its authority-related section (§9–10) and
  confirmed to cite rather than duplicate, but its other ~20 sections
  (glossary, lifecycle, routing, CLI surface, current contradictions) were
  only header-scanned, not read line-by-line. The "Known contradictions,
  drift, and debt" section (§20, lines 919–1027) in particular could itself
  duplicate or conflict with `DRIFT-AND-DEBT-TAXONOMY.md` — flagged for a
  closer read before concluding either way.
