---
name: business-formulate-strategy
default_tier: high
description: "Use when strategic objectives, arenas, advantage thesis, non-goals, assumptions, and review triggers must be chosen; never allocates resources, publishes commitments, or substitutes for accountable owner approval."
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

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when the
strategy hides an unresolved trade-off, depends on weak market evidence, or
would silently authorize resource movement or public commitment.

## Skill Grilling Profile

Apply the `business-formulate-strategy` profile in
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

Return the objective, arena, advantage thesis, non-goals, assumptions, evidence
gaps, alternatives considered, chosen strategy, authority needs, routes, and
revisit trigger to `conduct-work-object`.

## Routing and termination

- Market evidence gap -> `business-manage-market-intelligence`.
- Money consequence -> `business-assess-financial-decision`.
- Capacity consequence -> `business-plan-workforce-accountability`.
- Process consequence -> `business-improve-operating-process`.
- Public commitment or material reallocation -> conductor for scoped authority.

## Output template

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
