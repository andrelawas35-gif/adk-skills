---
name: business-manage-enterprise-risk
default_tier: high
description: "Use when risk appetite, tolerance, treatment, ownership, monitoring, and residual exposure must be decided across business objectives; never accepts risk or provides legal, actuarial, safety, audit, or insurance assurance."
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

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when risk
acceptance, weak controls, hidden tail risk, or an unowned treatment could
materially change the outcome.

## Skill Grilling Profile

Apply the `business-manage-enterprise-risk` profile in
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

Return risk statement, objective, evidence, controls, treatment options,
recommended treatment, residual exposure, owner, monitoring evidence, authority
needs, and revisit trigger to `conduct-work-object`.

## Routing and termination

- Active harm -> `operations-diagnose-production-incident`.
- Cash, cost, or return consequence -> `business-assess-financial-decision`.
- Role ownership or capacity -> `business-plan-workforce-accountability`.
- Recurring control/process change -> `business-improve-operating-process`.
- Risk acceptance or external commitment -> conductor for scoped authority.

## Output template

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
