---
name: alawas-governance-govern-scorecards
description: "Use when outcome evidence must be judged across declared dimensions; exposes gaps, subgroup harm, and non-compensable failures; does not let aggregates trigger automatic rules or sharing."
default_tier: high
platform: lm-studio-bionic
---
# Govern Scorecards

## Governing principle

A scorecard is a review of attributable outcomes, not a measure of personal
worth or agent activity. It makes evidence, uncertainty, and tensions visible
so a human can decide whether to propose a bounded workflow change.

## Boundaries and non-goals

This skill does:

- Review completion, decision quality, reality contact, loop burden, routing quality,
  recovery quality, personal fit, artifact value, and novelty yield.
- Preserve each dimension's evidence, inference, confidence, exceptions, and
  revisit trigger, including conflicting signals and `insufficient` evidence.
- Propose a scoped Workflow Candidate or a linked successor revision through
  `alawas-governance-maintain-working-method`.
- Preserve prior scorecards, candidates, evidence, and rule versions.

This skill does not:

- Compute a composite score, ranking, or activity proxy from message counts,
  hours, streaks, or artifact volume.
- Infer identity, personality, enduring preference, or capability from a
  scorecard.
- Promote, apply, retire, deploy, export, or directly alter a Working Method,
  skill, adapter, or workflow rule.
- Read or copy personal-archive content without a user-approved summary.

## Inputs and preconditions

The input is a completed or reviewed Work Object with durable, attributable
outcome evidence. Each reviewed dimension requires a stated scope, source or
system evidence, inference, confidence, exceptions, and revisit trigger.
Missing material is recorded as `insufficient`; it is never silently converted
into a low score or a negative judgment.

## Required capabilities

The platform adapter classifies each capability as native, manual-fallback, or
unsupported and follows `references/CAPABILITY-DEGRADATION.md` when needed.

- `file_read` and `content_search` — retrieve the Work Object, permitted local
  outcome evidence, decision records, and prior candidate lineage.
- `file_write` — pass a concise scorecard or proposal record to
  `alawas-governance-conduct-work-object` for durable persistence.
- `user_confirmation` — obtain the scoped authority needed for a proposed rule
  or any later candidate-maintenance decision.
- `artifact_rendering` — render scorecard evidence as a visual artifact; without
  it, present the data in structured text.
- `structured_output` — return dimension-level evidence, conflicts, gaps,
  proposal status, and next route.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

**Authority gate:** Proposing a Workflow Candidate that would change a
workflow rule requires explicit human confirmation at ALL consequence levels.
Before proceeding: (1) verify the receiving Work Object's consequence and
sensitivity fields, (2) request confirmation naming the proposed rule and
scope, (3) record a structured authority History entry per the authority
recording contract in `references/CONSEQUENCE-AUTHORITY.md`.

- A scorecard may recommend one bounded next move but never changes a workflow
  rule directly.
- A proposed rule remains an unconfirmed Workflow Candidate until the existing
  bounded test, contrary-evidence review, and explicit human confirmation gates
  in `alawas-governance-maintain-working-method` are satisfied.
- A material revision creates a separate successor candidate or Working Method
  linked with `supersedes`; it never overwrites the prior version.
- High-consequence changes require explicit, scoped human confirmation before
  any durable mutation.
- For a high-consequence Work Object, confirmation must name the exact proposed
  mutation. Do not stage, annotate, change status, append History, or make any
  other mutation before that confirmation.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

When scorecard evidence conflicts or is insufficient, recommend preserving the
conflict or filling the smallest relevant gap rather than forcing a score,
identity claim, or proposal. Route a material workflow decision to
`alawas-thinking-pressure-test-decision` before recording it.

## Skill Grilling Profile

Apply the `alawas-governance-govern-scorecards` profile and continuous Grilling Session in
`references/SKILL-AWARE-GRILLING.md`. Tie every dimension to an attributable,
decision-relevant evidence source; challenge activity proxies, hidden
distributions, aggregation, identity claims, and automatic action. On direct
entry, route through `alawas-governance-conduct-work-object` first. Return the compact continuity
record; do not reset context, store a transcript, or mutate the Work Object.

## Stage workflow

### 1. Establish the review boundary

Read the Work Object's intended outcome, scope, evidence ledger, decision
record, verification evidence, recovery history, and uncertainty. State what
period, context, and sources the scorecard covers. Do not infer a scorecard
dimension from chat activity or unavailable records.

### 2. Review dimensions without collapsing conflicts

For every applicable dimension, retain this minimum record:

- dimension and bounded scope;
- attributable evidence and its provenance;
- a clearly labelled inference;
- confidence, exceptions, and a revisit trigger;
- `supported`, `contradicted`, or `insufficient` assessment where appropriate.

Conflicting signals remain separate. For example, a delivered artifact can
have favorable artifact value evidence and contradictory recovery-quality
evidence; neither is averaged into a composite score.

### 3. Propose, but do not govern automatically

When the review supports a change, propose a Workflow Candidate with a
testable rule, scope, origin scorecard reference, supporting and contrary
evidence, confidence, exceptions, and revisit trigger. Route it to
`alawas-governance-maintain-working-method`; do not apply the proposal or treat one scorecard as
universal proof.

When a proposed or promoted rule changes materially, create a successor linked
by `supersedes`. Preserve the predecessor's identity, evidence, scope, and
version history. If evidence is insufficient or materially contradictory,
recommend a bounded investigation, revision, or retirement decision rather
than a new rule.

### 4. Protect personal fit and novelty yield

Personal fit is a scoped, user-provided outcome signal when attributable; it
is not an identity claim and cannot authorize personal-archive access.
Novelty yield records whether a bounded review produced a useful new option or
falsified an assumption. It must not reward novelty churn, artifact volume, or
changes made merely to improve a scorecard.

## Evidence rules

- Label source, system, lived, inference, decision, and unresolved material
  according to `references/EVIDENCE-MODEL.md`.
- A missing signal is an evidence gap, not an unfavorable result.
- A user-approved summary is a minimum-necessary reference only; it does
  not authorize reading the archive it came from.
- State `none observed within scope` only for the sources and period actually
  reviewed.

## Dependency invocation rules

- Route a workflow-rule proposal, revision, contrary-evidence review, bounded
  test, promotion, or retirement to `alawas-governance-maintain-working-method`.
- Route unresolved outcome evidence to `alawas-governance-review-outcome-and-adapt` or
  `alawas-research-investigate-live-question`.
- Route a material governance decision to `alawas-thinking-pressure-test-decision`.
- Report a missing dependency as reduced capability; do not imitate its gates.

## Work Object updates

Return a concise record to `alawas-governance-conduct-work-object` containing the scorecard
scope, each reviewed dimension's evidence and provenance, inference,
confidence, exceptions, revisit trigger, conflicts, evidence gaps, and any
unconfirmed candidate or successor relationship. The conductor owns schema
validation, state/status transitions, History, and durable record placement.

## Routing and termination

- **Evidence supports a proposal:** route the unconfirmed scoped candidate to
  `alawas-governance-maintain-working-method`; do not promote or apply it.
- **Evidence conflicts or is insufficient:** preserve the boundary and route
  the smallest investigation, outcome review, or decision move.
- **Material revision:** route the linked successor through
  `alawas-governance-maintain-working-method` using `supersedes`; do not mutate the predecessor.
- **Manual-fallback capability:** pause with one concrete user-run instruction
  and mark the affected evidence unverified.
- **Unsupported capability:** stop the affected route, record the limitation,
  and route to a supported platform or the user.

## Output template

Apply `references/DIRECTOR-LANGUAGE.md` to everything said to the
director. Lead with plain meaning; attach the technical term to the explanation
rather than substituting it. Order anything worth explaining as: what's
happening, why it matters, the technical term, the evidence, the
recommendation, what needs deciding. Short answers stay short, and any part may
be marked absent — "Evidence: none, this is inference" is valid and preferred.
Never fill a part to complete the shape. Never phrase a decision in terms the
director must decode before choosing. Record content is never translated:
field names, state names, record IDs, and file paths stay exact.

```markdown
## Scorecard governance review

- **Scope:** <Work Object, period, and evidence boundary>
- **Dimensions:** <evidence, inference, confidence, exceptions, revisit trigger>
- **Conflicts and gaps:** <preserved conflicts and insufficient evidence>
- **Proposal:** <none | unconfirmed Workflow Candidate | linked successor>
- **Protection:** <no aggregate, activity proxy, identity inference, or automatic change>
- **Next route:** <maintain-working-method | investigate | decision | none>
```

## Anti-patterns

- Averaging conflicting evidence into a number that conceals the trade-off.
- Treating message count, hours, streaks, or artifact volume as outcome value.
- Inferring identity or stable personal traits from a bounded review.
- Treating a scorecard proposal as a confirmed or applied workflow rule.
- Rewriting earlier evidence or rule versions to make the newest version look
  inevitable.

## Final self-check

- Does every reviewed dimension preserve attributable evidence, inference,
  confidence, exceptions, and a revisit trigger?
- Are conflicts and `insufficient` evidence visible rather than aggregated?
- Did the review avoid activity proxies and identity inference?
- Is every proposal unconfirmed, scoped, and routed through
  `alawas-governance-maintain-working-method`?
- Does each material revision retain immutable predecessor history with
  `supersedes`?
- Did the review avoid automatic promotion, rule application, Personal
  Institution access, deployment, export, and direct mutation?
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

### Epistemic rules

This skill uses the **full 6‑tag system** (`references/epistemic/epistemic-rules-full.md`).

The epistemic tier is resolved from the skill's `default_tier` (high).
**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the epistemic tier is upgraded to at least `medium` (essential 3‑tag).
When `consequence: high`, the epistemic tier is upgraded to the strongest
available tier (full 6‑tag).
`actual_epistemic_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

For a high-consequence Work Object, confirmation must name the exact
proposed mutation. Do not stage, annotate, change status, append History,
or make any other mutation before receiving that scoped confirmation.

### Model tier

This skill declares `default_tier: high`.
The platform overlay resolves this to `Qwen3.5-9B Q4`.
The prompt budget for this tier is approximately 32000 tokens (advisory).

**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the effective tier is upgraded to at least `medium`. When `consequence: high`,
the effective tier is upgraded to the strongest available model.
`actual_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `native project file access (Read file)` | native |
| `content_search` | `Search (native project index)` | native |
| `file_write` | `Edit / write file (native coding tools)` | native |
| `user_confirmation` | `conversation turn` | native |
| `artifact_rendering` | `—` | manual-fallback |
| `structured_output` | `Structured output (native, per-session schema)` | native |

### Capability Degradation

Apply `references/CAPABILITY-DEGRADATION.md`. Per-capability
classifications and notes below.

#### `artifact_rendering` (manual-fallback)

- **Behavior**: Pause and give one concrete manual instruction.
- **Record**: Append History entry noting the capability gap, the
  manual action taken, and what remains unverified.
- **Note**: Bionic does not expose a dedicated artifact-rendering surface for generated skill output. Render deliverables via the document/file workflow or manual steps.
