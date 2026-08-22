---
name: alawas-business-source-and-govern-suppliers
description: "Use when make/buy, sourcing strategy, supplier selection, supplier governance, or supplier performance response must be decided; never contacts suppliers, negotiates, awards, purchases, or signs contracts without scoped authority."
default_tier: high
platform: codex
---
# Source and Govern Suppliers

## Governing principle

Supplier decisions combine need, qualification, relationship model, performance,
risk, cost, and authority. Keep make/buy logic and supplier governance separate
from procurement execution.

## Boundaries and non-goals

This skill does:

- Frame make/buy, sourcing strategy, supplier selection, relationship model, or
  supplier performance response.
- Compare supplier options by criteria, evidence, service, risk, cost, and
  governance needs.
- Recommend a sourcing or supplier-governance decision with gates and routes.

This skill does not:

- Issue RFPs, contact suppliers, negotiate, award, purchase, sign contracts, or
  perform legal/sanctions determinations.
- Treat lowest price as total value or a preferred supplier as proven fit.
- Replace procurement, legal, compliance, or accountable owner approval.

## Inputs and preconditions

Use an activated Work Object with need, make/buy alternatives, selection
criteria, candidate sources, cost/service/risk evidence, constraints, supplier
data permission, relationship model, and accountable owner.

## Required capabilities

- `file_read` and `content_search` — inspect permitted sourcing, supplier,
  contract-summary, and prior decision evidence.
- `web_fetch` — retrieve permitted public supplier or standards evidence at
  known URLs.
- `file_write` — return a compact supplier decision through the conductor.
- `user_confirmation` — authorize supplier contact, RFPs, negotiation, awards,
  purchase orders, contracts, shared data, or spend.
- `structured_output` — report criteria, recommendation, gates, and route.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Read-only supplier analysis is allowed inside the approved evidence boundary.
- Supplier contact, RFPs, negotiation, awards, purchase orders, contracts,
  sanctions/compliance checks, shared data, and spend require explicit scoped
  authority.
- Supplier, pricing, and contract data may be private; store minimum summaries.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when a
make/buy assumption, supplier risk, missing criterion, or gated external action
could reverse the recommendation.

## Skill Grilling Profile

Apply the `alawas-business-source-and-govern-suppliers` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge cheapest-bid bias, supplier
qualification gaps, hidden contract authority, make/buy shortcuts, and
performance evidence gaps.

## Business operating pipeline

Use `references/BUSINESS-OPERATING-PIPELINE.md` to distinguish this skill's
make/buy, sourcing, supplier-selection, and supplier-governance frontier from
the Work Object lifecycle and the commercial pipeline. Route forward or back
only when the evidence exposes a different owning business frontier.

## Stage workflow

1. Define need, owner, make/buy boundary, decision criteria, constraints, and
   non-goals.
2. Inspect supplier evidence, service fit, risk, cost, relationship model, and
   governance needs.
3. Compare make, buy, defer, or redesign alternatives when credible.
4. Recommend sourcing path, supplier-governance model, performance evidence,
   authority gates, and revisit trigger.
5. Route execution, contracts, spend, or legal/compliance determinations outside
   this skill.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`.
- A vendor claim is testimony or marketing evidence, not proof of performance.
- Total cost, delivery fit, risk, and relationship governance are distinct.

## Work Object updates

This skill returns a concise record to `conduct-work-object`, which validates and persists it.

Return need, make/buy alternatives, criteria, supplier evidence, cost/service
risk, recommendation, relationship model, authority needs, and revisit trigger
to `alawas-governance-conduct-work-object`.

## Routing and termination

- Spend viability -> `alawas-business-assess-financial-decision`.
- Internal capacity alternative -> `alawas-business-plan-workforce-accountability`.
- Supplier-process integration -> `alawas-business-improve-operating-process`.
- Supplier contact, award, purchase, contract, or shared data -> conductor for
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
## Supplier decision
- **Need and criteria:** <scope, owner, make/buy boundary>
- **Options and evidence:** <supplier, internal, defer, redesign>
- **Risks and governance:** <service, relationship, controls, gaps>
- **Recommendation:** <source | govern | requalify | defer | stop>
- **Authority and route:** <analysis only or exact gated action>
```

## Final self-check

- Are make/buy, supplier qualification, and purchasing execution separate?
- Is total value broader than lowest price?
- Is every supplier contact, purchase, contract, and spend action gated?
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
