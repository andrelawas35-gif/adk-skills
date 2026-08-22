---
schema_version: 1
id: 2026-08-22-002
title: Skill-existence test and Role/Skill/Capability taxonomy -- resolve 'capability' term collision
type: inquiry
status: active
state: explore
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-22T09:56:28Z
updated_at: 2026-08-22T09:57:41Z
next_action: Route to alawas-thinking-pressure-test-decision: pick the highest-leverage decision between (1) skill-existence rule adoption and (2) the capability naming collision, and test it





---
## Intent

Test two related proposals surfaced from a recapped "skills vs capabilities"
and "role vs skill vs capability" framing:

1. A skill-existence rule: "if removing the skill and simply calling a
   strong LLM produces equally safe and consistent results, delete the
   skill" — with repeatability, governance, epistemic discipline, authority
   boundaries, stable output contracts, and cross-model consistency as the
   qualifying criteria.
2. A Role / Skill / Capability taxonomy (`Role = authority/context`,
   `Skill = bounded method`, `Capability = primitive operation`), where
   "Capability" would name cognitive primitives (retrieve, perceive,
   compare, classify, infer, hypothesize, generate, critique, plan, verify,
   reflect).

Neither exists in the repo today (confirmed by direct inspection). The
second collides with an already load-bearing use of the word "capability"
(tool-level primitives — `file_read`, `web_fetch`, etc. — used in every
skill's `Required capabilities` section and `skill-map.yaml`). Originated
from a request to `alawas-research-produce-report`, which stopped rather
than author new governance/taxonomy as an accepted plan, and routed here
per director instruction ("New Work Object, route it to
pressure-test-decision").

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [ ] Pressure-test-decision has tested whether the skill-existence rule is
      adopted, rejected, or narrowed
- [ ] The "capability" naming collision is resolved — either the cognitive
      taxonomy is renamed, the tool-level usage is renamed, or the proposal
      is rejected entirely
- [ ] A recorded decision covering both, with rationale and revisit triggers


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
| [gap] | grep across the whole repo for skill-existence criteria, skill-creator meta-skill | No governance rule anywhere states when a skill should exist vs. be deleted in favor of calling a strong LLM directly. This is a genuinely new proposal, not a forgotten decision. |
| [gap] | CONTEXT.md (the actual domain glossary) | No Role/Skill/Capability triad exists anywhere in the repo. CONTEXT.md defines Personal Institution, Observation, Project, Source, Work Studio, etc. with explicit _Avoid_ lists, but nothing resembling Role = authority/context, Skill = bounded method, Capability = primitive operation. This is new, not accepted material. |
| [system] | every skill's Required capabilities section; work-studio/skill-map.yaml requires_capabilities field | 'Capability' is already a load-bearing term across every skill, meaning a tool-level primitive (file_read, file_write, directory_list, content_search, terminal_run, web_fetch, subagent_spawn, structured_output, user_confirmation, background_processes, git_operations). The proposed cognitive-primitive list (retrieve, perceive, compare, classify, infer, hypothesize, generate, critique, plan, verify, reflect) reuses the identical word for a different concept. Adopting the proposal as-is would make 'capability' ambiguous everywhere it is currently used. |
## Open questions

- Is the skill-existence rule ("delete if a strong LLM alone is equally
  safe") actually applicable to any skill in this repo today, or is it a
  reasonable-sounding principle with no current test case? Should it be
  applied retroactively to the existing 22 skills, or only prospectively?
- Does the Role/Skill/Capability taxonomy add decision-relevant structure
  the studio currently lacks, or does it re-describe the existing
  Work Object / skill / `Required capabilities` structure in new words?
- If the cognitive-primitive list is worth keeping, what should it be
  called instead of "capability" to avoid colliding with the existing,
  already-used meaning of that word?

## Next move

Route to `alawas-thinking-pressure-test-decision`. Two candidate
highest-leverage decisions — the skill's job is to pick which comes first:
(1) does the skill-existence rule get adopted, and (2) how is the
"capability" collision resolved (rename one side, or reject the taxonomy).
The three Evidence ledger entries above (no existing skill-existence rule,
no existing Role/Skill/Capability triad, and the confirmed term collision)
should carry forward as given context, not be re-derived.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T09:56:39Z — Created

- **State:** notice
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Signal originated from a request to alawas-research-produce-report (asking it to process a recapped section on 'skills vs capabilities' and 'role vs skill vs capability'). produce-report checked the claims: no existing skill-existence-justification rule anywhere in the repo, no Role/Skill/Capability triad in CONTEXT.md (the actual domain glossary) or anywhere else, and critically a real naming collision -- 'capability' is already a load-bearing term meaning tool-level primitives (file_read, web_fetch, etc.) in every skill's Required capabilities section and skill-map.yaml, while the proposed taxonomy uses the same word for cognitive primitives (retrieve, compare, infer...). Per its own boundary (never author new governance/taxonomy as a plan-type deliverable), it stopped and routed to conduct-work-object per director confirmation ("New Work Object, route it to pressure-test-decision").
### 2026-08-22T09:57:41Z — Classified and staged for pressure-test

- **State:** explore
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Intent, Success evidence, Open questions, Next move, and three Evidence ledger entries recorded directly per director instruction. Ready to route to pressure-test-decision -- two candidate decisions: adopt/reject the skill-existence rule, and resolve the 'capability' naming collision.
