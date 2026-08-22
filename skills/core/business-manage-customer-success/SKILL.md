---
name: business-manage-customer-success
default_tier: high
description: "Use when post-sale onboarding, adoption, realized outcomes, customer health, renewal risk, or intervention priority must be decided; never contacts customers, edits CRM or CS tools, grants concessions, or promises outcomes without scoped authority."
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

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when health
evidence is weak, a promised outcome is unsupported, or an intervention would
cross customer-contact, concession, private-data, or renewal authority.

## Skill Grilling Profile

Apply the `business-manage-customer-success` profile in
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

Return customer boundary, sold outcome, onboarding/adoption evidence, health
signals, outcome gaps, intervention recommendation, risks, authority needs, and
revisit trigger to `conduct-work-object`.

## Routing and termination

- New sale or expansion opportunity -> `business-manage-commercial-pipeline`.
- Concession, refund, or margin effect -> `business-assess-financial-decision`.
- Account coverage or support capacity -> `business-plan-workforce-accountability`.
- Systemic onboarding/support flow -> `business-improve-operating-process`.
- Customer contact, CS/CRM write, concession, refund, or promise -> conductor
  for scoped authority.

## Output template

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
