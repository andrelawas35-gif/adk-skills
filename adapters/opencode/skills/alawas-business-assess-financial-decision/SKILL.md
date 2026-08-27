---
name: alawas-business-assess-financial-decision
description: "Use when a business choice needs cash, cost, break-even, return, or scenario analysis; exposes assumptions and downside; never moves money, approves spend, files accounts, or presents estimates as accounting advice."
default_tier: high
platform: opencode
---
# Assess Financial Decision

## Governing principle

A financial model is a conditional story about money, not a verdict. Make cash
timing, unit economics, assumptions, ranges, downside, and decision thresholds
visible before recommending whether to proceed, revise, defer, or stop.

## Boundaries and non-goals

This skill does:

- Frame a bounded business decision and compare the status quo with credible
  alternatives.
- Build or inspect cash-flow, cost, contribution, break-even, return, and
  sensitivity evidence proportionate to the decision.
- Separate accounting facts, operational estimates, assumptions, and judgment.
- Recommend a decision with downside, liquidity, and revisit conditions.

This skill does not:

- Move money, approve spend, open accounts, set payroll, file taxes, prepare
  statutory statements, value securities, or replace an accountant or adviser.
- Invent prices, volumes, margins, discount rates, tax treatment, or financing.
- Hide cash timing behind profit, average away downside, or report false precision.

## Inputs and preconditions

Use an activated Work Object naming the decision, alternatives, time horizon,
currency, decision owner, maximum acceptable downside, and available source
records. Restricted credentials or account details stay outside the Work Object.

## Required capabilities

- `file_read` and `content_search` — inspect permitted financial and operating evidence.
- `file_write` — return the analysis through the conductor.
- `terminal_run` — run reproducible local calculations when useful.
- `user_confirmation` — authorize access to private sources or any financial commitment.
- `structured_output` — present scenarios, assumptions, and recommendation.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Financial analysis is read-only; every money movement, spend approval,
  financing action, filing, or commitment requires explicit scoped authority.
- Financial records are private by default. Store minimum summaries, never
  credentials, full account numbers, or unrestricted transaction exports.
- State when professional accounting, tax, legal, or investment advice is needed.
- For a high-consequence Work Object, confirmation must name the exact proposed
  mutation. Do not stage, annotate, change status, append History, or make any
  other mutation before that confirmation.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when an
unverified assumption, liquidity boundary, irreversible cost, or asymmetric
downside could reverse the recommendation.

## Skill Grilling Profile

Apply the `alawas-business-assess-financial-decision` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge profit/cash confusion, omitted
costs, demand certainty, terminal-value dependence, and downside concealment.

## Business operating pipeline

Use `references/BUSINESS-OPERATING-PIPELINE.md` to distinguish this skill's
bounded money-decision frontier from the Work Object lifecycle and the
commercial pipeline. Route forward or back only when the evidence exposes a
different owning business frontier.

## Stage workflow

1. Define the decision, alternatives, horizon, currency, owner, threshold, and
   excluded effects.
2. Establish the source baseline: current cash effects, fixed and variable
   costs, contribution, obligations, capacity constraints, and timing.
3. Model base, downside, and upside cases with named assumptions. Calculate
   break-even or return only when inputs support it; otherwise retain a range.
4. Test the variables most capable of reversing the result and state the
   weakest evidence. Compare against doing nothing and the cheapest credible alternative.
5. Recommend proceed, revise, defer, or stop with conditions, funding/authority
   boundary, recovery path, and revisit trigger.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md` and retain source dates and currency.
- A spreadsheet formula can verify arithmetic, not the truth of its assumptions.
- Profit, cash flow, and financing capacity are distinct; report each when relevant.

## Work Object updates

This skill returns a concise record to `conduct-work-object`, which validates and persists it.

Return the decision, alternatives, source baseline, scenario table, assumptions,
sensitivity, downside and liquidity risks, recommendation, confidence basis,
authority needs, and revisit trigger to `alawas-governance-conduct-work-object`.

## Routing and termination

- Revenue evidence gap → `alawas-business-manage-commercial-pipeline`.
- Capacity or role assumption → `alawas-business-plan-workforce-accountability`.
- Process-cost assumption → `alawas-business-improve-operating-process`.
- Money movement or commitment → conductor for explicit authority.

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
## Financial decision analysis
- **Decision and horizon:** <scope, alternatives, currency>
- **Baseline:** <source facts and dates>
- **Scenarios:** <downside | base | upside with assumptions>
- **Sensitivity and risks:** <reversal variables, cash, irreversibility>
- **Recommendation:** <proceed | revise | defer | stop, with conditions>
- **Authority and route:** <analysis only or exact gated action>
```

## Final self-check

- Are arithmetic, source facts, assumptions, and judgment separate?
- Did the analysis show cash timing and downside, not only expected return?
- Is every financial commitment outside this skill and explicitly gated?
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
