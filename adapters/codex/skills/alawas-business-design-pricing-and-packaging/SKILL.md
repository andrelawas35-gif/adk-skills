---
name: alawas-business-design-pricing-and-packaging
description: "Use when value metric, package structure, prices or ranges, discount fences, offer terms, or pricing tests must be chosen; never publishes prices, quotes, discounts, or claims without scoped authority."
default_tier: high
platform: codex
---
# Design Pricing and Packaging

## Governing principle

Pricing is a hypothesis about value, willingness to pay, economics, and
fairness. Keep the value metric, package boundary, price/range, discount fence,
evidence, and test condition separate before the offer becomes a promise.

## Boundaries and non-goals

This skill does:

- Recommend value metric, package structure, price/range, discount rules, offer
  fences, and test design.
- Compare customer value, market references, economics, service burden,
  fairness, and operational feasibility.
- Expose assumptions, claim boundaries, and review triggers.

This skill does not:

- Publish prices, quote customers, grant discounts, edit commerce/CRM systems,
  or promise terms.
- Replace market research, financial viability analysis, legal/compliance
  review, or commercial opportunity management.
- Treat competitor prices, costs, or desired margin as sufficient by themselves.

## Inputs and preconditions

Use an activated Work Object naming the offer, target segment, use case, value
driver, current package or alternatives, known price references, economics,
service obligations, constraints, owner, and the decision that must be made now.

## Required capabilities

- `file_read` and `content_search` — inspect permitted strategy, market,
  customer, cost, package, and prior pricing evidence.
- `web_fetch` — retrieve permitted price, policy, or market evidence at known
  sources.
- `file_write` — return a compact pricing decision through the conductor.
- `user_confirmation` — authorize publication, customer quotes, discounts,
  claims, or live-system changes.
- `structured_output` — report package, pricing, assumptions, gaps, and route.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Read-only pricing design and test planning is allowed within the approved
  evidence boundary.
- Published prices, customer quotes, discounts, customer communications,
  regulated claims, discriminatory or protected-class-sensitive pricing, and
  live commerce/CRM changes require explicit scoped authority.
- Customer, competitor, cost, and margin evidence may be private; store only
  minimum necessary summaries.
- For a high-consequence Work Object, confirmation must name the exact proposed
  mutation before any durable update.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when weak
willingness-to-pay evidence, margin/cash conflict, fairness risk, or publication
authority could reverse the recommendation.

## Skill Grilling Profile

Apply the `alawas-business-design-pricing-and-packaging` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge competitor-price anchoring,
unsupported value metrics, discount leakage, claim overreach, margin blindness,
and hidden fairness or regulatory risk.

## Business operating pipeline

Use `references/BUSINESS-OPERATING-PIPELINE.md` to distinguish this skill's
pricing and offer-architecture frontier from the Work Object lifecycle and the
commercial pipeline. Route forward or back only when the evidence exposes a
different owning business frontier.

## Stage workflow

1. Define segment, use case, buyer, value driver, package alternatives, owner,
   decision horizon, and excluded commitments.
2. Inspect customer value, willingness-to-pay evidence, competitor/substitute
   references, costs, service burden, cash timing, and operational constraints.
3. Compare value metric, package boundaries, price/range, discount fences, and
   test options. Separate evidence from judgment.
4. Test whether market, financial, delivery, process, customer-success, or risk
   evidence could reverse the offer shape.
5. Recommend package, price/range or test range, discount rules, assumptions,
   authority needs, and revisit trigger.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`.
- A competitor price is context, not proof of willingness to pay or margin fit.
- A pricing test plan is not publication, customer promise, or validated demand.

## Work Object updates

This skill returns a concise record to `conduct-work-object`, which validates and persists it.

Return the pricing decision boundary, package alternatives, value metric,
price/range, discount fences, evidence, assumptions, gaps, authority needs,
routes, and revisit trigger to `alawas-governance-conduct-work-object`.

## Routing and termination

- Market or willingness-to-pay gap -> `alawas-business-manage-market-intelligence`.
- Named deal question -> `alawas-business-manage-commercial-pipeline`.
- Financial viability -> `alawas-business-assess-financial-decision`.
- Planning baseline effect -> `alawas-business-build-driver-based-plan-and-forecast`.
- Service burden or delivery feasibility -> `alawas-business-improve-operating-process`
  or `alawas-business-direct-project-delivery`.
- Publication, quote, discount, claim, or live-system change -> conductor for
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
## Pricing and packaging decision
- **Scope:** <offer, segment, use case, owner>
- **Package and metric:** <value metric, package boundaries, fences>
- **Price or test range:** <recommendation and evidence basis>
- **Economics and risks:** <margin, cash, fairness, claims, service burden>
- **Assumptions and gaps:** <weak evidence and reversal variables>
- **Authority and route:** <analysis only or exact gated action>
```

## Final self-check

- Is the offer architecture separate from one deal's negotiation?
- Are value, market evidence, economics, and fairness distinct?
- Is every quote, discount, publication, claim, or system write gated?
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


### Runtime pin resolution

Codex can discover both user and repository skills with the same name.
Before applying this skill, search upward from the current directory for
`.work-studio/adapter.codex.lock`, stopping at the repository or filesystem
boundary. Read its `dest` value and
resolve `<dest>/<this-skill-name>/SKILL.md`. When that path differs from
the currently loaded copy, **load and follow the pinned copy** before
continuing. A matching legacy `adapter.lock` remains valid during migration.
If the pinned file is unavailable, report the broken pin and
stop instead of silently falling back to the global copy.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `read_file` | native |
| `content_search` | `grep_search` | native |
| `web_fetch` | `open_browser_page / mcp tools` | native |
| `file_write` | `create_file / replace_string_in_file` | native |
| `user_confirmation` | `conversation turn` | native |
| `structured_output` | `—` | native |
