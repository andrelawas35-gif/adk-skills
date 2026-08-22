---
name: business-build-driver-based-plan-and-forecast
default_tier: high
description: "Use when operating drivers and scenarios must become an integrated profit, cash, and balance-sheet planning baseline; never approves budgets, moves money, files accounts, or presents forecasts as assurance."
---
# Build Driver-Based Plan and Forecast

## Governing principle

A forecast is a conditional planning baseline, not certainty. Tie every number
to a driver, source, assumption, scenario, and refresh rule so future decisions
can see what changed.

## Boundaries and non-goals

This skill does:

- Build or inspect a driver-based planning baseline across operating drivers,
  profit, cash timing, and balance-sheet implications.
- Separate source facts, assumptions, scenarios, sensitivity, and judgment.
- Expose refresh cadence, reversal variables, and routeable consequences.

This skill does not:

- Move money, approve budgets, file accounts, replace accounting advice, or
  decide one bounded investment by itself.
- Invent prices, volume, costs, cash timing, tax treatment, financing, or
  accounting facts.
- Present forecasts as assurance, accounting, tax, legal, or investment advice.

## Inputs and preconditions

Use an activated Work Object with planning horizon, currency, driver
definitions, source records, current baseline, scenario assumptions,
constraints, owner, and the decisions the baseline will support.

## Required capabilities

- `file_read` and `content_search` — inspect permitted planning, financial, and
  operating evidence.
- `terminal_run` — run reproducible local calculations when useful.
- `file_write` — return a compact planning baseline through the conductor.
- `user_confirmation` — authorize private financial-source access, commitments,
  or publication.
- `structured_output` — report drivers, scenarios, gaps, and refresh rules.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Financial and operating planning is read-only unless scoped authority names a
  commitment or source expansion.
- Private financial records stay minimum-summary only; credentials and full
  account details never enter the Work Object.
- Budget commitments, accounting/tax claims, financing actions, and published
  forecasts require explicit scoped authority.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when one
driver assumption, cash timing gap, or source contradiction could reverse the
baseline.

## Skill Grilling Profile

Apply the `business-build-driver-based-plan-and-forecast` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge false precision, profit/cash
confusion, hidden driver assumptions, scenario averaging, and stale baselines.

## Business operating pipeline

Use `references/BUSINESS-OPERATING-PIPELINE.md` to distinguish this skill's
integrated planning-baseline frontier from the Work Object lifecycle and the
commercial pipeline. Route forward or back only when the evidence exposes a
different owning business frontier.

## Stage workflow

1. Define horizon, currency, owner, supported decisions, and excluded effects.
2. Establish the baseline and driver tree from source records and operating
   assumptions.
3. Build base, downside, and upside scenarios; separate arithmetic from source
   truth and judgment.
4. Identify variables most likely to reverse a downstream recommendation and
   route weak evidence to the owning skill.
5. Recommend whether to use, revise, investigate, or defer the baseline with a
   refresh rule and authority boundary.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`.
- A formula verifies arithmetic, not the truth of assumptions.
- Profit, cash, and financing capacity are distinct and should not be collapsed.

## Work Object updates

Return driver definitions, source baseline, scenarios, assumptions, sensitivity,
cash and balance-sheet implications, gaps, authority needs, refresh trigger, and
routes to `conduct-work-object`.

## Routing and termination

- One bounded financial choice -> `business-assess-financial-decision`.
- Revenue evidence from named opportunities -> `business-manage-commercial-pipeline`.
- Capacity assumptions -> `business-plan-workforce-accountability`.
- Process-cost or cycle assumptions -> `business-improve-operating-process`.
- Commitments, filings, or publication -> conductor for scoped authority.

## Output template

```markdown
## Driver-based plan and forecast
- **Horizon and owner:** <scope, currency, supported decisions>
- **Driver tree:** <drivers, source records, assumptions>
- **Scenarios:** <downside | base | upside and cash timing>
- **Sensitivity and gaps:** <reversal variables and weak evidence>
- **Recommendation:** <use | revise | investigate | defer>
- **Authority and route:** <analysis only or exact gated action>
```

## Final self-check

- Does every number trace to a driver, source, or named assumption?
- Are profit, cash, and balance-sheet effects separate?
- Is every budget, filing, financing, or publication action gated?
