---
name: business-assess-financial-decision
default_tier: high
description: "Use when a business choice needs cash, cost, break-even, return, or scenario analysis; exposes assumptions and downside; never moves money, approves spend, files accounts, or presents estimates as accounting advice."
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

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when an
unverified assumption, liquidity boundary, irreversible cost, or asymmetric
downside could reverse the recommendation.

## Skill Grilling Profile

Apply the `business-assess-financial-decision` profile in
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

Return the decision, alternatives, source baseline, scenario table, assumptions,
sensitivity, downside and liquidity risks, recommendation, confidence basis,
authority needs, and revisit trigger to `conduct-work-object`.

## Routing and termination

- Revenue evidence gap → `business-manage-commercial-pipeline`.
- Capacity or role assumption → `business-plan-workforce-accountability`.
- Process-cost assumption → `business-improve-operating-process`.
- Money movement or commitment → conductor for explicit authority.

## Output template

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
