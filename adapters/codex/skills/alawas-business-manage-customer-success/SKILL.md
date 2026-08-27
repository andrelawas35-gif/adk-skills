---
name: alawas-business-manage-customer-success
description: "Use when post-sale onboarding, adoption, realized outcomes, customer health, renewal risk, or intervention priority must be decided; never contacts customers, edits CRM or CS tools, grants concessions, or promises outcomes without scoped authority."
default_tier: high
platform: codex
---
# Manage Customer Success

## Governing principle

Customer success is realized customer value after the sale, not optimism about
the relationship. Keep onboarding, adoption, outcome evidence, health signals,
renewal risk, obligations, and intervention authority separate.

## Boundaries and non-goals

This skill does:

- Assess post-sale onboarding, adoption, realized outcomes, health evidence,
  renewal risk, obligations, and intervention options.
- Recommend one account or segment action: continue, intervene, escalate,
  requalify, investigate, or stop a promise.
- Route new sales, concessions, delivery defects, workforce coverage, and
  process problems.

This skill does not:

- Qualify new opportunities, promise concessions, contact customers, edit CRM
  or customer-success tools, issue refunds, or decide product roadmap.
- Treat usage volume, sentiment, or relationship warmth as proof of realized
  outcome.
- Store unrestricted customer data or private usage exports in a Work Object.

## Inputs and preconditions

Use an activated Work Object with customer/account identifier, sold outcome,
onboarding state, adoption evidence, realized outcome evidence, health signals,
renewal or expansion risk, obligations, private-data boundary, and owner.

## Required capabilities

- `file_read` and `content_search` — inspect permitted customer, account,
  support, usage-summary, and prior decision evidence.
- `file_write` — return a compact customer-success record through the conductor.
- `web_fetch` — retrieve permitted customer/account evidence at known sources.
- `user_confirmation` — authorize customer contact, CRM/CS writes, private-data
  expansion, concessions, refunds, renewal terms, promises, or escalations.
- `structured_output` — report health basis, outcome gaps, and route.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Read-only customer-success analysis is allowed inside the approved evidence
  boundary.
- Customer contact, CRM/CS-tool writes, usage/private data, concessions,
  refunds/credits, promised outcomes, renewal terms, and escalations require
  explicit scoped authority.
- Customer data is private by default; store only minimum necessary summaries.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when health
evidence is weak, a promised outcome is unsupported, or an intervention would
cross customer-contact, concession, private-data, or renewal authority.

## Skill Grilling Profile

Apply the `alawas-business-manage-customer-success` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge activity-as-value, hidden churn
risk, unsupported outcome claims, concession creep, and private-data expansion.

## Business operating pipeline

Use `references/BUSINESS-OPERATING-PIPELINE.md` to distinguish this skill's
post-sale realized-value frontier from the Work Object lifecycle and the
commercial pipeline. Route forward or back only when the evidence exposes a
different owning business frontier.

## Stage workflow

1. Define sold outcome, customer/account boundary, owner, obligations, and time
   window.
2. Inspect onboarding, adoption, realized outcome evidence, health signals,
   renewal/expansion risk, and contradictions.
3. Separate account-level intervention from systemic process, workforce,
   financial, or pipeline issues.
4. Recommend continue, intervene, escalate, requalify, investigate, or stop a
   promise with evidence, owner, authority needs, and revisit trigger.
5. Route external customer action, concessions, or private-data expansion to the
   conductor.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`.
- Usage, sentiment, and relationship strength are signals, not proof of realized
  customer outcome.
- Customer statements remain testimony unless independently corroborated.

## Work Object updates

This skill returns a concise record to `conduct-work-object`, which validates and persists it.

Return customer boundary, sold outcome, onboarding/adoption evidence, health
signals, outcome gaps, intervention recommendation, risks, authority needs, and
revisit trigger to `alawas-governance-conduct-work-object`.

## Routing and termination

- New sale or expansion opportunity -> `alawas-business-manage-commercial-pipeline`.
- Concession, refund, or margin effect -> `alawas-business-assess-financial-decision`.
- Account coverage or support capacity -> `alawas-business-plan-workforce-accountability`.
- Systemic onboarding/support flow -> `alawas-business-improve-operating-process`.
- Customer contact, CS/CRM write, concession, refund, or promise -> conductor
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
## Customer-success decision
- **Customer outcome:** <account, sold outcome, obligation>
- **Adoption and health:** <evidence, gaps, renewal risk>
- **Intervention options:** <continue | intervene | escalate | investigate>
- **Recommendation:** <owner, evidence, revisit trigger>
- **Authority and route:** <analysis only or exact gated action>
```

## Final self-check

- Is realized customer value separate from usage and relationship signals?
- Are account-level and systemic problems routed separately?
- Is every customer contact, tool write, concession, refund, or promise gated?
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
| `file_write` | `create_file / replace_string_in_file` | native |
| `web_fetch` | `open_browser_page / mcp tools` | native |
| `user_confirmation` | `conversation turn` | native |
| `structured_output` | `—` | native |
