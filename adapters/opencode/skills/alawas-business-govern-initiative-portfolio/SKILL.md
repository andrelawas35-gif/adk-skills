---
name: alawas-business-govern-initiative-portfolio
description: "Use when multiple initiatives compete for start, sequence, fund, pause, stop, or attention decisions; never approves spend, staffing, cancellation, or public commitments without scoped authority."
default_tier: high
platform: opencode
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

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when a
favored initiative lacks strategic fit, a capacity or dependency conflict could
reverse the sequence, or stopping work would cross authority.

## Skill Grilling Profile

Apply the `alawas-business-govern-initiative-portfolio` profile in
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

This skill returns a concise record to `conduct-work-object`, which validates and persists it.

Return the portfolio boundary, initiative comparison, disposition, sequence,
constraints, assumptions, gaps, rejected alternatives, authority needs, routes,
and revisit trigger to `alawas-governance-conduct-work-object`.

## Routing and termination

- Strategy uncertainty -> `alawas-business-formulate-strategy`.
- Market or demand gap -> `alawas-business-manage-market-intelligence`.
- Money consequence -> `alawas-business-assess-financial-decision` or
  `alawas-business-build-driver-based-plan-and-forecast`.
- Capacity consequence -> `alawas-business-plan-workforce-accountability`.
- Delivery control -> `alawas-business-direct-project-delivery`.
- Risk conflict -> `alawas-business-manage-enterprise-risk`.
- Funding, cancellation, staffing, or external commitment -> conductor for
  scoped authority.

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
| `terminal_run` | `bash` | native |
| `user_confirmation` | `question / permission ask` | native |
| `structured_output` | `—` | native |
