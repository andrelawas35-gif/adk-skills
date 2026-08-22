---
name: business-manage-liquidity-and-cash-runway
default_tier: high
description: "Use when cash timing, obligations, runway, liquidity gaps, or escalation options must be decided; never moves money, borrows, invests, pays, collects, or gives accounting/legal/insolvency advice."
---
# Manage Liquidity and Cash Runway

## Governing principle

Survival is cash on time, not profit on paper. Keep available cash, dated
obligations, committed inflows, timing uncertainty, runway, and escalation
options separate before a liquidity gap becomes harm.

## Boundaries and non-goals

This skill does:

- Analyze cash availability, dated obligations, inflows, scenarios, runway, and
  timing gaps.
- Identify reversal variables, safe options, escalation triggers, and authority
  boundaries.
- Route financing, payment, collections, supplier, workforce, or risk issues to
  the right owner.

This skill does not:

- Move money, borrow, invest, pay, collect, file taxes, negotiate creditors, or
  provide accounting, legal, tax, investment, covenant, or insolvency advice.
- Replace integrated driver-based planning or one bounded financial decision.
- Hide liquidity risk behind profit, revenue, bookings, or average scenarios.

## Inputs and preconditions

Use an activated Work Object with currency, horizon, current cash position,
cash availability, dated obligations, expected inflows, cash-timing evidence,
constraints, owner, and the liquidity decision or escalation threshold.

## Required capabilities

- `file_read` and `content_search` — inspect permitted cash, obligation,
  planning, supplier, payroll, tax, debt, and prior decision evidence.
- `terminal_run` — run reproducible local cash-timing calculations when useful.
- `file_write` — return a compact liquidity record through the conductor.
- `user_confirmation` — authorize source expansion, payments, transfers,
  borrowing, collections, commitments, or external communications.
- `structured_output` — report runway, timing gaps, options, and route.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Read-only liquidity analysis within the approved evidence boundary is allowed.
- Payments, transfers, borrowing, investments, collections, creditor/customer
  communications, covenant/insolvency matters, tax filings, and financing
  actions require explicit scoped authority and qualified review when
  appropriate.
- Financial records are private by default; credentials and full account details
  never enter the Work Object.
- For a high-consequence Work Object, confirmation must name the exact proposed
  mutation before any durable update.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when one
inflow, obligation, cash restriction, covenant, or timing assumption could
reverse runway or escalation.

## Skill Grilling Profile

Apply the `business-manage-liquidity-and-cash-runway` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge profit/cash substitution,
undated obligations, optimistic collections, restricted cash, covenant silence,
and delayed escalation.

## Business operating pipeline

Use `references/BUSINESS-OPERATING-PIPELINE.md` to distinguish this skill's
cash-timing and runway frontier from the Work Object lifecycle and the
commercial pipeline. Route forward or back only when the evidence exposes a
different owning business frontier.

## Stage workflow

1. Define horizon, currency, owner, liquidity threshold, available cash, and
   excluded actions.
2. Build the dated cash view: opening cash, committed inflows, obligations,
   payroll, tax, rent, debt, supplier, inventory, and other cash movements.
3. Run base, downside, and upside timing scenarios. Separate confirmed facts,
   assumptions, restrictions, and judgment.
4. Identify earliest gap, runway range, dominant reversal variables, and safe
   options or escalation triggers.
5. Recommend monitor, investigate, conserve, renegotiate, finance, defer,
   escalate, or stop as an analysis record with authority boundaries.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`.
- A receivable, booking, or forecast is not cash until timing and collectability
  evidence support it.
- A runway date is an inference from dated inputs and scenario assumptions, not
  assurance.

## Work Object updates

Return cash position, horizon, dated inflows/obligations, scenarios, runway
range, timing gaps, reversal variables, options, authority needs, routes, and
revisit trigger to `conduct-work-object`.

## Routing and termination

- One bounded financial choice -> `business-assess-financial-decision`.
- Integrated baseline -> `business-build-driver-based-plan-and-forecast`.
- Supplier/payment issue -> `business-source-and-govern-suppliers`.
- Payroll or role-capacity issue -> `business-plan-workforce-accountability`.
- Risk threshold -> `business-manage-enterprise-risk`.
- Payment, financing, collection, filing, or external communication -> conductor
  for scoped authority.

## Output template

```markdown
## Liquidity and cash runway decision
- **Scope:** <horizon, currency, owner, threshold>
- **Cash view:** <available cash, dated inflows, obligations>
- **Scenarios:** <base, downside, upside timing and runway>
- **Gaps and reversal variables:** <earliest gap and weak evidence>
- **Options:** <monitor | investigate | conserve | renegotiate | finance | defer | escalate | stop>
- **Authority and route:** <analysis only or exact gated action>
```

## Final self-check

- Are cash, profit, bookings, and receivables kept separate?
- Are obligations and inflows dated with evidence quality visible?
- Is every payment, borrowing, investment, filing, or external communication gated?
