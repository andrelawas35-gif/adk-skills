---
name: alawas-business-build-driver-based-plan-and-forecast
description: "Use when operating drivers and scenarios must become an integrated profit, cash, and balance-sheet planning baseline; never approves budgets, moves money, files accounts, or presents forecasts as assurance."
default_tier: high
platform: github-copilot
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

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when one
driver assumption, cash timing gap, or source contradiction could reverse the
baseline.

## Skill Grilling Profile

Apply the `alawas-business-build-driver-based-plan-and-forecast` profile in
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

This skill returns a concise record to `conduct-work-object`, which validates and persists it.

Return driver definitions, source baseline, scenarios, assumptions, sensitivity,
cash and balance-sheet implications, gaps, authority needs, refresh trigger, and
routes to `alawas-governance-conduct-work-object`.

## Routing and termination

- One bounded financial choice -> `alawas-business-assess-financial-decision`.
- Revenue evidence from named opportunities -> `alawas-business-manage-commercial-pipeline`.
- Capacity assumptions -> `alawas-business-plan-workforce-accountability`.
- Process-cost or cycle assumptions -> `alawas-business-improve-operating-process`.
- Commitments, filings, or publication -> conductor for scoped authority.

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
