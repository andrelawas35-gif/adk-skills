---
name: business-direct-project-delivery
default_tier: high
description: "Use when delivery approach, scope, schedule, dependencies, change control, or continue/recover/escalate decisions must govern a bounded business initiative; never implements, funds, staffs, contracts, or promises delivery without scoped authority."
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

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when the
baseline is missing, a change request hides new scope, or recovery would cross
resource, customer, vendor, contract, or live-system authority.

## Skill Grilling Profile

Apply the `business-direct-project-delivery` profile in
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

Return baseline, delivery evidence, dependencies, risks, change-control
assessment, recommendation, authority needs, recovery path, and revisit trigger
to `conduct-work-object`.

## Routing and termination

- Code or repo implementation -> `engineering-implement-bounded-change`.
- Financial viability or spend -> `business-assess-financial-decision`.
- Role capacity or accountability -> `business-plan-workforce-accountability`.
- Recurring process experiment -> `business-improve-operating-process`.
- Customer/vendor commitments or baseline changes -> conductor for scoped
  authority.

## Output template

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
