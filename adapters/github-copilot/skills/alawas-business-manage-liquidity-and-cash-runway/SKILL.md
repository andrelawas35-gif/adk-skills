---
name: alawas-business-manage-liquidity-and-cash-runway
description: "Use when cash timing, obligations, runway, liquidity gaps, or escalation options must be decided; never moves money, borrows, invests, pays, collects, or gives accounting/legal/insolvency advice."
default_tier: high
platform: github-copilot
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

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when one
inflow, obligation, cash restriction, covenant, or timing assumption could
reverse runway or escalation.

## Skill Grilling Profile

Apply the `alawas-business-manage-liquidity-and-cash-runway` profile in
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

This skill returns a concise record to `conduct-work-object`, which validates and persists it.

Return cash position, horizon, dated inflows/obligations, scenarios, runway
range, timing gaps, reversal variables, options, authority needs, routes, and
revisit trigger to `alawas-governance-conduct-work-object`.

## Routing and termination

- One bounded financial choice -> `alawas-business-assess-financial-decision`.
- Integrated baseline -> `alawas-business-build-driver-based-plan-and-forecast`.
- Supplier/payment issue -> `alawas-business-source-and-govern-suppliers`.
- Payroll or role-capacity issue -> `alawas-business-plan-workforce-accountability`.
- Risk threshold -> `alawas-business-manage-enterprise-risk`.
- Payment, financing, collection, filing, or external communication -> conductor
  for scoped authority.

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
The platform overlay resolves this to `claude-sonnet-4-20250514`.
The prompt budget for this tier is approximately 80000 tokens (advisory).

**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the effective tier is upgraded to at least `medium`. When `consequence: high`,
the effective tier is upgraded to the strongest available model.
`actual_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `read_file` | native |
| `content_search` | `grep_search` | native |
| `terminal_run` | `run_in_terminal` | native |
| `file_write` | `create_file / replace_string_in_file / multi_replace_string_in_file` | native |
| `user_confirmation` | `conversation turn` | native |
| `structured_output` | `—` | native |
