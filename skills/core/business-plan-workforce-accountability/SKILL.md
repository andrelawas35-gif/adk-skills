---
name: business-plan-workforce-accountability
default_tier: high
description: "Use when goals must be translated into roles, capacity, skills, ownership, or workforce gaps; recommends a people plan; never hires, evaluates an individual, changes employment terms, or infers personal capability without evidence."
---
# Plan Workforce and Accountability

## Governing principle

Start from work the organization must perform, then determine capacity, skills,
roles, and accountable decisions. Do not turn an organization gap into an
unsupported judgment about a person.

## Boundaries and non-goals

This skill does:

- Translate accepted goals and operating demand into work, capacity, skill,
  role, ownership, and escalation needs.
- Map current coverage and identify overload, single points of failure,
  unclear accountability, and evidence-backed gaps.
- Compare redesign, automation, development, contracting, and hiring options.
- Recommend a bounded workforce or accountability plan with review triggers.

This skill does not:

- Recruit, contact candidates, hire, fire, promote, discipline, set pay, change
  employment terms, or conduct performance evaluation.
- Infer personality, loyalty, potential, health, identity, or capability from
  sparse activity data or protected characteristics.
- Store personnel files or sensitive individual data in a Work Object.

## Inputs and preconditions

Use an activated Work Object with accepted goals, demand horizon, required
work/outcomes, current role coverage at the minimum useful granularity, known
constraints, and accountable decision owner. Use role-level evidence by default;
individual-level analysis requires necessity, authority, and private handling.

## Required capabilities

- `file_read` and `content_search` — inspect permitted goals, role, workload,
  and process evidence.
- `file_write` — return a compact plan through the conductor.
- `user_confirmation` — authorize personal-data use or any personnel action.
- `structured_output` — report demand, coverage, gaps, options, and route.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Role-level planning may proceed within the approved boundary. Individual
  personnel analysis, contact, evaluation, or employment action requires
  explicit scoped authority and minimum necessary private data.
- Protected characteristics, health data, identity documents, and similarly
  restricted material never enter the Work Object.
- Recommendations must expose affected people, burden, reversibility, and who
  owns the actual decision.
- For a high-consequence Work Object, confirmation must name the exact proposed
  mutation. Do not stage, annotate, change status, append History, or make any
  other mutation before that confirmation.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when the
plan could misattribute a system problem to a person, create hidden overload,
or trigger a consequential personnel action.

## Skill Grilling Profile

Apply the `business-plan-workforce-accountability` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge demand forecasts, role ambiguity,
single points of failure, capacity optimism, identity inference, and automation bias.

## Business operating pipeline

Use `references/BUSINESS-OPERATING-PIPELINE.md` to distinguish this skill's
role, capacity, skill, and accountability frontier from the Work Object
lifecycle and the commercial pipeline. Route forward or back only when the
evidence exposes a different owning business frontier.

## Stage workflow

1. Define goals, horizon, service/quality expectations, workload drivers, and
   decisions that must have one accountable owner.
2. Decompose required work into outcomes, recurring responsibilities, skills,
   capacity, dependencies, and escalation paths.
3. Map current role-level coverage and confidence. Preserve unknown capacity or
   skill as a gap; do not fill it with reputation or activity proxies.
4. Identify overload, undercoverage, unclear ownership, handoff risk, and single
   points of failure. Test redesign, stop-work, automation, development,
   contracting, and hiring in that order only when each is credible.
5. Recommend a staged plan with affected roles, accountable owner, safeguards,
   evidence to collect, review date, and explicit personnel-action boundary.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`; testimony about workload remains testimony.
- Output volume, hours online, or message count does not establish capability or performance.
- State conclusions about roles and systems separately from any permitted individual evidence.

## Work Object updates

Return demand assumptions, required work, current coverage, gaps, risks, options,
recommended role/accountability changes, affected groups, authority needs, and
revisit trigger to `conduct-work-object`.

## Routing and termination

- Process redesign → `business-improve-operating-process`.
- Financial affordability → `business-assess-financial-decision`.
- Personnel action or personal-data expansion → conductor for scoped authority.
- Missing demand evidence → investigation or commercial pipeline analysis.

## Output template

```markdown
## Workforce and accountability plan
- **Goals and horizon:** <demand and service boundary>
- **Required work:** <outcomes, capacity, skills, decisions>
- **Coverage and gaps:** <role-level evidence and uncertainty>
- **Options and risks:** <redesign, stop, automate, develop, contract, hire>
- **Recommendation:** <staged plan, owner, review trigger>
- **People protection and route:** <affected groups and gated actions>
```

## Final self-check

- Did the plan start from required work rather than assumed headcount?
- Are role/system gaps separate from judgments about individuals?
- Is every personnel action and private-data expansion explicitly gated?
