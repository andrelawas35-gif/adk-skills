---
name: business-manage-market-intelligence
default_tier: high
description: "Use when market boundaries, demand signals, competitors, substitutes, uncertainty, and refresh cadence must inform a business decision; never contacts people, buys data, scrapes, or publishes claims without scoped authority."
---
# Manage Market Intelligence

## Governing principle

Market intelligence is decision evidence with a boundary and refresh cadence,
not a pile of interesting facts. Keep market definition, demand signals,
competitors, substitutes, source reliability, and uncertainty tied to the
decision they can change.

## Boundaries and non-goals

This skill does:

- Define market, segment, demand, competitor, substitute, and signal boundaries.
- Classify source quality, contradictions, uncertainty, and refresh triggers.
- State how market evidence changes or does not change a business decision.

This skill does not:

- Qualify named opportunities, contact prospects, set strategy alone, create
  marketing claims, scrape restricted data, or buy data.
- Treat a secondary summary, model output, or stale source as current market
  fact.
- Replace customer research consent, legal review, or claim substantiation.

## Inputs and preconditions

Use an activated Work Object naming the decision, market boundary, target
segment, known sources, demand signals, competitor/substitute hypotheses, source
dates, reliability concerns, and the recommendation the evidence may change.

## Required capabilities

- `file_read` and `content_search` — inspect permitted local market and prior
  decision evidence.
- `web_fetch` — retrieve permitted public or licensed-at-hand sources at known
  URLs.
- `file_write` — return a compact market-intelligence record through the
  conductor.
- `user_confirmation` — authorize paid data, scraping, contact, publication, or
  personal-data use.
- `structured_output` — report boundaries, signals, confidence, and route.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Read-only public-source analysis is allowed inside the Work Object boundary.
- Paid/licensed data, scraping, competitor or customer contact, personal data,
  publication, and market claims require explicit scoped authority.
- Record source dates and uncertainty; never present market evidence as a
  guaranteed forecast.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when a weak
source, boundary ambiguity, or external collection method could reverse or
invalidate the recommendation.

## Skill Grilling Profile

Apply the `business-manage-market-intelligence` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge market-boundary drift, stale
signals, competitor theater, unsupported demand inference, and claim authority.

## Business operating pipeline

Use `references/BUSINESS-OPERATING-PIPELINE.md` to distinguish this skill's
market-evidence frontier from the Work Object lifecycle and the commercial
pipeline. Route forward or back only when the evidence exposes a different
owning business frontier.

## Stage workflow

1. Define the decision, market boundary, segment, geography, time window, and
   sources in scope.
2. Separate demand signals, competitor/substitute evidence, customer testimony,
   source facts, and inference.
3. Compare directness, freshness, authority, contradictions, and uncertainty.
4. State what the evidence changes, what remains a gap, and the refresh cadence
   or trigger.
5. Route named opportunities, financial effects, strategy changes, or external
   actions to the owning skill or conductor.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`.
- A competitor list is not proof of customer substitution without evidence.
- Demand evidence from named buyers routes to pipeline rather than being
  averaged into market intelligence.

## Work Object updates

Return market boundary, sources, demand signals, competitor/substitute evidence,
contradictions, confidence basis, decision impact, authority needs, refresh
trigger, and next route to `conduct-work-object`.

## Routing and termination

- Named buyer intent -> `business-manage-commercial-pipeline`.
- Strategic implication -> `business-formulate-strategy`.
- Cash, cost, or return implication -> `business-assess-financial-decision`.
- Contact, scraping, data purchase, or publication -> conductor for scoped
  authority.

## Output template

```markdown
## Market intelligence brief
- **Decision and boundary:** <market, segment, time window>
- **Sources and signals:** <evidence, source dates, confidence>
- **Competitors and substitutes:** <what is known and uncertain>
- **Contradictions and gaps:** <what could change the recommendation>
- **Decision impact:** <recommendation effect and refresh trigger>
- **Authority and route:** <analysis only or exact gated action>
```

## Final self-check

- Is market boundary explicit and decision-linked?
- Are source facts, testimony, and inference separate?
- Is every contact, scraping, paid-data, publication, or claim action gated?
