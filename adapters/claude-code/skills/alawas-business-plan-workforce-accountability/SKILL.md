---
name: alawas-business-plan-workforce-accountability
description: "Use when goals must be translated into roles, capacity, skills, ownership, or workforce gaps; recommends a people plan; never hires, evaluates an individual, changes employment terms, or infers personal capability without evidence."
default_tier: high
platform: claude-code
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

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when the
plan could misattribute a system problem to a person, create hidden overload,
or trigger a consequential personnel action.

## Skill Grilling Profile

Apply the `alawas-business-plan-workforce-accountability` profile in
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

This skill returns a concise record to `conduct-work-object`, which validates and persists it.

Return demand assumptions, required work, current coverage, gaps, risks, options,
recommended role/accountability changes, affected groups, authority needs, and
revisit trigger to `alawas-governance-conduct-work-object`.

## Routing and termination

- Process redesign → `alawas-business-improve-operating-process`.
- Financial affordability → `alawas-business-assess-financial-decision`.
- Personnel action or personal-data expansion → conductor for scoped authority.
- Missing demand evidence → investigation or commercial pipeline analysis.

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
| `user_confirmation` | `conversation turn` | native |
| `structured_output` | `—` | native |
