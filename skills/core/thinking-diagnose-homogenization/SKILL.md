---
name: thinking-diagnose-homogenization
default_tier: medium
description: "Use when a draft sounds generic, overly fluent, or training-data-shaped and needs its voice preserved; diagnoses homogenization, demands concrete evidence and genuine alternatives before polishing, and never fabricates material or declares prose authentic."
---

# Diagnose Homogenization

## Governing principle

Protect distinct perception from smooth generic prose. Diagnose before rewriting. Preserve what is alive in the draft; cut or mark what is unearned. Never substitute an AI's idea of a distinctive voice for the user's actual material.

## Boundaries and non-goals

**This skill does:**
- Diagnose homogenization and explain the diagnosis rather than labeling prose
  generic by style alone.
- Mark what is specific and worth keeping in a draft.
- Demand concrete evidence, lived detail, and genuine alternatives before
  polishing.
- Offer two or three materially different revision directions before rewriting.
- Rewrite only from supplied or retrieved material, marking missing material
  as an explicit gap.
- Return final judgment to the writer.

**This skill does NOT:**
- Invent anecdotes, locations, emotions, quotations, research, or personal
  history.
- Claim to detect AI authorship or plagiarism from style alone.
- Turn personal experience into proof of a social claim.
- Make the writer sound more radical, literary, academic, or certain than the
  source supports.
- Declare prose authentic, original, or "more human" — only the writer can.

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

- This skill diagnoses and recommends; the writer decides. Authority never transfers.
- The agent never declares prose authentic or "more human" — only the writer can.
- The agent never fabricates evidence, scenes, quotes, or personal history.
- Missing material is marked as a gap, never invented.
- For a high-consequence Work Object, editorial recommendations still proceed,
  but recording a final revision requires explicit confirmation. Do not stage,
  annotate, change status, append History, or make any other mutation before
  receiving that scoped confirmation.

## Grilling entry and stage lens

This is the groundedness lens: diagnose before rewriting, demand the missing
evidence rather than labeling prose by style, and let the writer decide which
revision direction is truer to their material.

## Skill Grilling Profile

Apply the `diagnose-homogenization` profile and continuous Grilling Session in
`references/SKILL-AWARE-GRILLING.md`. Demand concrete evidence for each
homogenization claim, and challenge substitutes, containment, recovery, and
result interpretation against the actual draft before any rewrite.
