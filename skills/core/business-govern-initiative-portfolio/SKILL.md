---
name: business-govern-initiative-portfolio
default_tier: high
description: "Use when multiple initiatives compete for start, sequence, fund, pause, stop, or attention decisions; never approves spend, staffing, cancellation, or public commitments without scoped authority."
---
# Govern Initiative Portfolio

## Governing principle

A portfolio is a choice about scarce attention and capacity, not a decorated
backlog. Keep strategic fit, expected benefit, cost, dependency, capacity,
risk, and stop conditions visible before deciding which initiatives start,
continue, pause, stop, or move.

## Boundaries and non-goals

This skill does:

- Compare multiple initiatives against strategy, capacity, dependencies, risk,
  expected benefit, evidence quality, and current commitments.
- Recommend start, continue, pause, stop, defer, or resequence decisions.
- Expose trade-offs, rejected alternatives, and review triggers.

This skill does not:

- Create strategy, approve funding, cancel work, staff teams, promise outcomes,
  or make executive/customer/vendor commitments.
- Run one initiative's delivery baseline or change-control process.
- Treat a priority label, sponsor preference, or status color as evidence.

## Inputs and preconditions

Use an activated Work Object naming the portfolio decision, owner, horizon,
strategy, candidate initiatives, current commitments, constraints, and the
decision that must be made now. Each initiative should have outcome, owner,
status, cost, capacity demand, dependency, expected benefit, risk, reversibility,
and evidence quality where available.

## Required capabilities

- `file_read` and `content_search` — inspect permitted strategy, initiative,
  planning, scorecard, and prior decision evidence.
- `file_write` — return a compact portfolio decision through the conductor.
- `terminal_run` — run local prioritization or dependency checks when useful.
- `user_confirmation` — authorize funding, cancellation, staffing, external
  commitments, or material Work Object mutations.
- `structured_output` — report portfolio choices, gaps, routes, and triggers.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Read-only portfolio analysis within the approved evidence boundary is allowed.
- Funding, cancellation, staffing/resource movement, external commitment,
  customer/vendor impact, or material reallocation requires explicit scoped
  authority.
- Strategic, financial, people, customer, supplier, or proprietary data may be
  private; store only minimum necessary summaries.
- For a high-consequence Work Object, confirmation must name the exact proposed
  mutation before any durable update.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when a
favored initiative lacks strategic fit, a capacity or dependency conflict could
reverse the sequence, or stopping work would cross authority.

## Skill Grilling Profile

Apply the `business-govern-initiative-portfolio` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge backlog theater, sponsor bias,
hidden capacity, dependency optimism, benefit inflation, and unowned stop
decisions.

## Business operating pipeline

Use `references/BUSINESS-OPERATING-PIPELINE.md` to distinguish this skill's
initiative-portfolio frontier from the Work Object lifecycle and the commercial
pipeline. Route forward or back only when the evidence exposes a different
owning business frontier.

## Stage workflow

1. Define the portfolio boundary, owner, horizon, strategic objectives,
   constraints, current commitments, and decision threshold.
2. Normalize each initiative into outcome, status, cost, capacity demand,
   dependency, benefit, risk, reversibility, evidence quality, and stop cost.
3. Compare credible options: start, continue, pause, stop, defer, resequence,
   or split. Preserve disagreement and weak evidence.
4. Test whether money, capacity, delivery, market, customer, supplier, or risk
   evidence could reverse the recommendation; route those gaps.
5. Recommend a portfolio choice set with owners, review trigger, explicit
   non-goals, authority needs, and downstream routes.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`.
- A benefit estimate is an inference unless supported by observed outcome,
  market, customer, or financial evidence.
- Activity, sunk cost, sponsorship, or status color is not strategic fit.

## Work Object updates

Return the portfolio boundary, initiative comparison, disposition, sequence,
constraints, assumptions, gaps, rejected alternatives, authority needs, routes,
and revisit trigger to `conduct-work-object`.

## Routing and termination

- Strategy uncertainty -> `business-formulate-strategy`.
- Market or demand gap -> `business-manage-market-intelligence`.
- Money consequence -> `business-assess-financial-decision` or
  `business-build-driver-based-plan-and-forecast`.
- Capacity consequence -> `business-plan-workforce-accountability`.
- Delivery control -> `business-direct-project-delivery`.
- Risk conflict -> `business-manage-enterprise-risk`.
- Funding, cancellation, staffing, or external commitment -> conductor for
  scoped authority.

## Output template

```markdown
## Initiative portfolio decision
- **Scope:** <portfolio, owner, horizon, strategy boundary>
- **Comparison:** <initiatives, evidence, capacity, benefit, risk>
- **Disposition:** <start | continue | pause | stop | defer | resequence>
- **Trade-offs and gaps:** <rejected alternatives and weak evidence>
- **Review trigger:** <condition or date>
- **Authority and route:** <analysis only or exact gated action>
```

## Final self-check

- Does the recommendation allocate scarce attention rather than rank a wish list?
- Are benefit, capacity, dependency, and risk assumptions visible?
- Is every funding, staffing, stop, or external commitment gated?
