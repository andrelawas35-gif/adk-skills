---
name: alawas-thinking-diagnose-homogenization
description: "Diagnose and revise generic, overly fluent, or training-data-shaped prose by demanding concrete evidence, lived detail, and genuine alternatives before polishing. Use when the user says 'make this more like me,' 'review this draft,' 'this sounds AI-generated,' 'make this less generic,' or wants writing to retain a distinct voice without fabricated specificity."
default_tier: medium
platform: codex
---
# Diagnose Homogenization

Protect distinct perception from smooth generic prose. Diagnose before rewriting. Preserve what is alive in the draft; cut or mark what is unearned. Never substitute an AI's idea of a distinctive voice for the user's actual material.

## Groundedness lens

Every writer brings characteristic subjects, ways of seeing, and habits of
thought — maps and routes, systems and logistics, craft knowledge, institutional
structures, storytelling, direct experience. The lens below is a test for
*groundedness*, not a list of approved topics.

Use this lens as a heuristic for concreteness, not as decorative vocabulary.
Do not inject subjects into a draft that are not about them. Favor the writer's
direct, question-led, thesis-aware language when it is supported by a scene,
observation, document, or project. Let a useful fragment remain a fragment.

### What to check

- Does the draft draw on the writer's actual material — a scene, object, named
  constraint, or lived process — or does it stay at the level of general
  observation?
- Does it name a specific rule, system, place, or person rather than an
  abstraction?
- Does it take a position that has a cost, or does it settle for familiar
  uplift?
- Does it preserve the writer's direct question or unresolved tension, or does
  it smooth the uncertainty into a conclusion?

### How to use it

When a passage feels generic or unearned, identify what specific evidence is
missing. Name the gap concretely — `[needs a concrete scene]`, `[name the rule
or system]`, `[source needed]`, `[scope, exception, or counterexample]` —
rather than calling the writing "AI-generated" or "generic" by style alone.

## Editing sequence

1. Identify the draft's intended claim, reader, and stakes from the text. Ask one clarification only if these cannot be inferred.
2. Mark what is specific and worth keeping: a concrete image, named constraint, surprising connection, direct question, lived scene, or defensible claim.
3. Identify homogenization signals. Explain the diagnosis rather than merely calling language "generic."
4. Check whether the draft supplies the evidence needed for specificity. Refer to relevant personal memory or capture tools only when the writer indicates material is available.
5. Offer two or three revision directions before choosing a rewrite. Each direction must make a different substantive choice, not merely swap adjectives.
6. Rewrite only from supplied or retrieved material. Mark missing material as `[needs a concrete scene]`, `[name the rule or system]`, or `[source needed]`.
7. Return control to the writer for the final judgment. Do not declare the prose authentic, original, or "more human."

## Homogenization signals

Look for these patterns:

| Signal | What to demand instead |
| --- | --- |
| Empty abstraction | A scene, object, actor, rule, place, or consequence |
| Familiar uplift or conclusion | A claim that takes a position and accepts its cost |
| Smooth causal leap | The missing evidence, mechanism, or uncertainty |
| Institutional or management language | The people, incentives, and material process it hides |
| Totalizing claim | Scope, exception, or counterexample |
| Generic personal statement | A dated observation, decision, or artifact |
| Polished cadence with no pressure | A question, tension, or unresolved fact |

Do not claim to detect AI authorship or plagiarism from style alone. Describe the prose's observable features instead: "This sentence makes a broad claim without an example," not "This was written by AI."

## Evidence rules

- Do not invent anecdotes, locations, emotions, quotations, research, or personal history.
- Do not turn personal experience into proof of a social claim. Label the experience as evidence and the claim as inference.
- Do not make the writer sound more radical, literary, academic, or certain than the source supports.
- Preserve qualified language when the uncertainty is honest; remove hedging only when it obscures a clear claim.
- When a draft lacks material, ask for one concrete thing: a scene, object, rule, conversation, document, or counterexample.

## Review format

Begin with the diagnosis. Use a rewrite only after identifying its evidence base:

```markdown
## What already carries voice

- [Specific element to preserve]

## Where the draft flattens

- **[Quoted phrase or location]:** [Why it sounds familiar, unearned, or overly smooth]

## Missing material

- [One concrete detail, source, or counterexample that would make the claim earned]

## Revision directions

1. **[Direction]:** [Substantive choice and trade-off]
2. **[Direction]:** [Substantive choice and trade-off]

## Revision

[A revised passage grounded only in available material, with gaps visibly marked.]
```

For a short draft, keep the response proportionate. A single strong sentence may need one question, not a full editorial report.

## Final check

Before returning a revision, ask:

- Could this passage plausibly be written by anyone without the writer's evidence?
- Did the revision add a real distinction or only a more stylish surface?
- Does each broad claim have a scene, source, mechanism, or stated uncertainty?
- Did the edit preserve an unresolved tension where resolution would be false?

If the answer exposes a gap, mark the gap and let the writer supply the material.

## Required capabilities

This skill requires the following abstract capabilities. The platform adapter
classifies each as native, manual-fallback, or unsupported and degrades
explicitly when one is unavailable (see `references/CAPABILITY-DEGRADATION.md`).

- `file_read` — Read drafts, source material, prior context
- `file_write` — Record editorial output through the conductor
- `content_search` — Search workspace for relevant evidence
- `structured_output` — Produce structured editorial evidence

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- This skill diagnoses and recommends; the writer decides. Authority never transfers.
- The agent never declares prose authentic or "more human" — only the writer can.
- The agent never fabricates evidence, scenes, quotes, or personal history.
- Missing material is marked as a gap, never invented.
- For a high-consequence Work Object, editorial recommendations still proceed,
  but recording a final revision requires explicit confirmation.

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live
outside this file.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `read_file` | native |
| `file_write` | `create_file / replace_string_in_file / multi_replace_string_in_file` | native |
| `content_search` | `grep_search` | native |
| `structured_output` | `—` | native |
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

### Epistemic rules

This skill uses the **essential 3‑tag system** (`references/epistemic/epistemic-rules-essential.md`).

The epistemic tier is resolved from the skill's `default_tier` (medium).
**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the epistemic tier is upgraded to at least `medium` (essential 3‑tag).
When `consequence: high`, the epistemic tier is upgraded to the strongest
available tier (full 6‑tag).
`actual_epistemic_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.


### Runtime pin resolution

Codex can discover both user and repository skills with the same name.
Before applying this skill, search upward from the current directory for
`.work-studio/adapter.codex.lock`, stopping at the repository or filesystem
boundary. Read its `dest` value and
resolve `<dest>/<this-skill-name>/SKILL.md`. When that path differs from
the currently loaded copy, **load and follow the pinned copy** before
continuing. A matching legacy `adapter.lock` remains valid during migration.
If the pinned file is unavailable, report the broken pin and
stop instead of silently falling back to the global copy.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `read_file` | native |
| `file_write` | `create_file / replace_string_in_file` | native |
| `content_search` | `grep_search` | native |
| `structured_output` | `—` | native |
