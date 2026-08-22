---
name: alawas-business-manage-enterprise-risk
description: "Use when risk appetite, tolerance, treatment, ownership, monitoring, and residual exposure must be decided across business objectives; never accepts risk or provides legal, actuarial, safety, audit, or insurance assurance."
default_tier: high
platform: claude-code
---
# Manage Enterprise Risk

## Governing principle

Risk work exists to make exposure, ownership, treatment, and residual risk
visible to accountable humans. It does not make acceptance safe by describing it.

## Boundaries and non-goals

This skill does:

- Frame a risk against objectives, causes, consequences, current controls,
  treatment options, owner, and residual exposure.
- Compare accept, reduce, transfer, avoid, or monitor options against appetite
  or tolerance when available.
- Route active harm, controls, financial, workforce, and process consequences.

This skill does not:

- Accept risk for humans or provide legal, actuarial, safety, insurance, audit,
  or compliance opinions.
- Hide low-probability/high-impact exposure behind averages.
- Treat a policy, control, or mitigation plan as proof of actual protection.

## Inputs and preconditions

Use an activated Work Object with risk statement, cause, consequence, affected
objectives, current controls, likelihood/effect basis, appetite or tolerance,
owner, treatment options, residual risk, and monitoring trigger.

## Required capabilities

- `file_read` and `content_search` — inspect permitted risk, control, incident,
  and prior decision evidence.
- `file_write` — return a compact risk decision record through the conductor.
- `web_fetch` — retrieve permitted standards or source material at known URLs.
- `user_confirmation` — authorize risk acceptance, external commitments, or
  sensitive data expansion.
- `structured_output` — report risk, treatment, residual exposure, and route.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Risk analysis is read-only; risk acceptance stays with accountable humans.
- Safety, privacy, security, money, insurance, contractual transfer, regulated
  matters, and public risk claims require explicit scoped authority.
- Restricted security or safety details are referenced by pointer only, never
  copied into Work Objects.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when risk
acceptance, weak controls, hidden tail risk, or an unowned treatment could
materially change the outcome.

## Skill Grilling Profile

Apply the `alawas-business-manage-enterprise-risk` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge appetite ambiguity, control
theater, unowned treatment, tail-risk averaging, and accidental risk acceptance.

## Business operating pipeline

Use `references/BUSINESS-OPERATING-PIPELINE.md` to distinguish this skill's
risk-appetite and residual-exposure frontier from the Work Object lifecycle
and the commercial pipeline. Route forward or back only when the evidence
exposes a different owning business frontier.

## Stage workflow

1. Define objective, risk statement, causes, consequences, owner, and appetite
   or tolerance if available.
2. Inspect current controls, evidence of operation, exposure basis, and
   contradictions.
3. Compare accept, reduce, transfer, avoid, and monitor options with residual
   exposure and affected groups.
4. Recommend treatment, owner, monitoring evidence, authority boundary, and
   revisit trigger.
5. Route active harm, professional assurance, or external commitments out of
   this skill.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`.
- A control design is not evidence that the control operates.
- Risk acceptance is a decision, not an inference from silence.

## Work Object updates

This skill returns a concise record to `conduct-work-object`, which validates and persists it.

Return risk statement, objective, evidence, controls, treatment options,
recommended treatment, residual exposure, owner, monitoring evidence, authority
needs, and revisit trigger to `alawas-governance-conduct-work-object`.

## Routing and termination

- Active harm -> `alawas-operations-diagnose-production-incident`.
- Cash, cost, or return consequence -> `alawas-business-assess-financial-decision`.
- Role ownership or capacity -> `alawas-business-plan-workforce-accountability`.
- Recurring control/process change -> `alawas-business-improve-operating-process`.
- Risk acceptance or external commitment -> conductor for scoped authority.

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
## Enterprise risk decision
- **Risk and objective:** <statement, owner, affected objective>
- **Exposure and controls:** <evidence, control operation, gaps>
- **Treatment options:** <accept | reduce | transfer | avoid | monitor>
- **Recommendation:** <treatment, residual exposure, owner>
- **Monitoring and revisit:** <signals, cadence, trigger>
- **Authority and route:** <analysis only or exact gated action>
```

## Final self-check

- Is residual exposure visible after treatment?
- Are designed controls separate from operating evidence?
- Is every risk acceptance or professional-assurance boundary explicitly gated?
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
| `file_read` | `Read` | native |
| `content_search` | `Grep` | native |
| `file_write` | `Write / Edit` | native |
| `web_fetch` | `WebFetch / WebSearch` | native |
| `user_confirmation` | `conversation turn` | native |
| `structured_output` | `—` | native |
