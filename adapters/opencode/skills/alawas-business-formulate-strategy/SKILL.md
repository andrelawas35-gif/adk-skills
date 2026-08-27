---
name: alawas-business-formulate-strategy
description: "Use when strategic objectives, arenas, advantage thesis, non-goals, assumptions, and review triggers must be chosen; never allocates resources, publishes commitments, or substitutes for accountable owner approval."
default_tier: high
platform: opencode
---
# Formulate Strategy

## Governing principle

Strategy is a coherent choice set, not a slogan. Name the objective, arena,
advantage thesis, explicit non-goals, assumptions, and review trigger before
downstream portfolio, market, financial, workforce, or process decisions depend
on it.

## Boundaries and non-goals

This skill does:

- Frame a strategic choice set with objective, arena, advantage thesis,
  non-goals, assumptions, owner, and review triggers.
- Compare credible strategic alternatives against current evidence and
  constraints.
- Route market, money, capacity, and execution consequences to the owning
  business or lifecycle skill.

This skill does not:

- Allocate initiatives, approve spend, set pricing, create marketing claims,
  redesign operations, or make public commitments.
- Treat a preference, aspiration, or framework label as a strategic choice.
- Replace owner, board, legal, regulatory, or public-commitment authority.

## Inputs and preconditions

Use an activated Work Object that names the strategic decision, horizon,
decision owner, current commitments, relevant constraints, alternatives,
stakeholders, assumptions, and why the choice matters now. Missing evidence
remains a gap rather than a synthesized strategy.

## Required capabilities

- `file_read` and `content_search` — inspect permitted strategy, market,
  operating, and prior decision evidence.
- `file_write` — return a compact strategy choice record through the conductor.
- `web_fetch` — retrieve permitted market or standard evidence at known sources.
- `user_confirmation` — authorize public commitments, material reallocations,
  or external communications.
- `structured_output` — report choices, assumptions, routes, and triggers.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Read-only strategy analysis is allowed inside the Work Object boundary.
- Owner/board approval, public commitments, material reallocations, regulated
  claims, and external communications require explicit scoped authority.
- Strategy evidence may be private; store only minimum necessary summaries.
- For a high-consequence Work Object, confirmation must name the exact proposed
  mutation before any durable update.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when the
strategy hides an unresolved trade-off, depends on weak market evidence, or
would silently authorize resource movement or public commitment.

## Skill Grilling Profile

Apply the `alawas-business-formulate-strategy` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge slogan strategy, fuzzy arenas,
unsupported advantage, hidden non-goals, and assumptions that downstream work
would treat as settled.

## Business operating pipeline

Use `references/BUSINESS-OPERATING-PIPELINE.md` to distinguish this skill's
strategic-choice frontier from the Work Object lifecycle and the commercial
pipeline. Route forward or back only when the evidence exposes a different
owning business frontier.

## Stage workflow

1. Define the decision owner, horizon, objective, affected work, constraints,
   current commitments, and explicit non-goals.
2. Compare credible strategic alternatives by arena, advantage thesis,
   evidence, assumptions, reversibility, and downstream consequences.
3. Test whether market, financial, workforce, process, or delivery gaps could
   reverse the choice; route those gaps rather than burying them.
4. Recommend one choice set with owner, assumptions, confidence basis,
   downstream routes, and review trigger.
5. Keep every resource movement, public statement, or external commitment
   outside this skill until separately authorized.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`.
- A strategic assumption is an inference unless supported by current evidence.
- Distinguish strategic fit from affordability, capacity, operational flow, and
  customer buying evidence.

## Work Object updates

This skill returns a concise record to `conduct-work-object`, which validates and persists it.

Return the objective, arena, advantage thesis, non-goals, assumptions, evidence
gaps, alternatives considered, chosen strategy, authority needs, routes, and
revisit trigger to `alawas-governance-conduct-work-object`.

## Routing and termination

- Market evidence gap -> `alawas-business-manage-market-intelligence`.
- Money consequence -> `alawas-business-assess-financial-decision`.
- Capacity consequence -> `alawas-business-plan-workforce-accountability`.
- Process consequence -> `alawas-business-improve-operating-process`.
- Public commitment or material reallocation -> conductor for scoped authority.

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
## Strategy choice
- **Objective and horizon:** <goal, owner, time boundary>
- **Arena and advantage:** <where to play and why this can work>
- **Non-goals and constraints:** <what is explicitly excluded>
- **Alternatives and assumptions:** <credible choices and weak points>
- **Recommendation:** <chosen choice set and review trigger>
- **Authority and route:** <analysis only or exact gated action>
```

## Final self-check

- Is the output a coherent choice set rather than a slogan?
- Are assumptions, evidence, and owner decisions separate?
- Is every public commitment or resource movement explicitly gated?
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
The platform overlay resolves this to `anthropic/claude-sonnet-4-20250514`.
The prompt budget for this tier is approximately 80000 tokens (advisory).

**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the effective tier is upgraded to at least `medium`. When `consequence: high`,
the effective tier is upgraded to the strongest available model.
`actual_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `read` | native |
| `content_search` | `grep` | native |
| `file_write` | `edit / write / apply_patch` | native |
| `web_fetch` | `webfetch` | native |
| `user_confirmation` | `question / permission ask` | native |
| `structured_output` | `—` | native |
