---
name: alawas-business-direct-project-delivery
description: "Use when delivery approach, scope, schedule, dependencies, change control, or continue/recover/escalate decisions must govern a bounded business initiative; never implements, funds, staffs, contracts, or promises delivery without scoped authority."
default_tier: high
platform: claude-code
---
# Direct Project Delivery

## Governing principle

Project delivery control makes a bounded initiative honest: scope, schedule,
dependencies, change, risk, recovery, and acceptance are visible before momentum
turns into hidden commitment.

## Boundaries and non-goals

This skill does:

- Define delivery approach, scope/schedule/dependency baseline, change-control
  rule, status, risks, and recovery options.
- Recommend continue, recover, escalate, defer, or stop for a bounded business
  initiative.
- Route implementation, finance, workforce, process, customer, vendor, and
  contractual consequences.

This skill does not:

- Implement code, allocate an initiative portfolio, approve budget, change
  contracts, promise customer delivery, or manage personnel actions.
- Treat activity, status color, or plan existence as evidence of control.
- Replace the conductor's Work Object lifecycle or release authority.

## Inputs and preconditions

Use an activated Work Object with objective, scope boundary, owner,
dependencies, schedule, delivery approach, constraints, risks, current status,
change requests, and acceptance or recovery criteria.

## Required capabilities

- `file_read` and `content_search` — inspect permitted project, dependency,
  change, and prior decision evidence.
- `file_write` — return a compact project-delivery record through the conductor.
- `terminal_run` — inspect local repo status or checks when project delivery
  depends on repository evidence.
- `user_confirmation` — authorize baseline changes, resource commitments,
  customer/vendor communications, spend, or live-system changes.
- `structured_output` — report baseline, status, recovery, and route.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Read-only delivery analysis is allowed inside the Work Object boundary.
- Baseline changes, resource commitments, vendor/customer communications,
  contractual dates, spend, and live-system changes require explicit scoped
  authority.
- Delivery recommendations do not authorize implementation, deployment, or
  release.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when the
baseline is missing, a change request hides new scope, or recovery would cross
resource, customer, vendor, contract, or live-system authority.

## Skill Grilling Profile

Apply the `alawas-business-direct-project-delivery` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge status theater, baseline drift,
dependency optimism, unowned change, and recovery plans without stop criteria.

## Business operating pipeline

Use `references/BUSINESS-OPERATING-PIPELINE.md` to distinguish this skill's
bounded initiative-delivery frontier from the Work Object lifecycle and the
commercial pipeline. Route forward or back only when the evidence exposes a
different owning business frontier.

## Stage workflow

1. Define objective, owner, scope boundary, delivery approach, acceptance
   criteria, and non-goals.
2. Inspect baseline schedule, dependencies, risks, current status, evidence of
   progress, and change requests.
3. Test whether continue, recover, escalate, defer, or stop best preserves the
   accepted outcome and authority boundary.
4. Recommend delivery control action with owner, evidence, stop condition,
   recovery path, and revisit trigger.
5. Route implementation and external commitments to the owning specialist or
   conductor.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`.
- A plan or status label is not evidence that dependencies are controlled.
- Separate accepted scope from requested scope and inferred scope.

## Work Object updates

This skill returns a concise record to `conduct-work-object`, which validates and persists it.

Return baseline, delivery evidence, dependencies, risks, change-control
assessment, recommendation, authority needs, recovery path, and revisit trigger
to `alawas-governance-conduct-work-object`.

## Routing and termination

- Code or repo implementation -> `alawas-engineering-implement-bounded-change`.
- Financial viability or spend -> `alawas-business-assess-financial-decision`.
- Role capacity or accountability -> `alawas-business-plan-workforce-accountability`.
- Recurring process experiment -> `alawas-business-improve-operating-process`.
- Customer/vendor commitments or baseline changes -> conductor for scoped
  authority.

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
## Project-delivery decision
- **Objective and baseline:** <scope, schedule, owner, acceptance>
- **Status and dependencies:** <evidence, risks, change requests>
- **Control decision:** <continue | recover | escalate | defer | stop>
- **Recovery and stop rule:** <path, owner, revisit trigger>
- **Authority and route:** <analysis only or exact gated action>
```

## Final self-check

- Are accepted scope and requested scope separate?
- Is progress evidenced beyond activity or status color?
- Is every baseline, resource, external, live-system, or contract action gated?
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
| `file_read` | `Read` | native |
| `content_search` | `Grep` | native |
| `file_write` | `Write / Edit` | native |
| `terminal_run` | `Bash` | native |
| `user_confirmation` | `conversation turn` | native |
| `structured_output` | `—` | native |
