---
name: alawas-design-design-tracer-bullet
description: "Use when an accepted direction needs the smallest end-to-end experiment; returns a bounded, observable, reversible tracer design; does not implement it or authorize production effects."
default_tier: high
platform: github-copilot
---
# Design Tracer Bullet

## Governing principle

The first slice should buy evidence, not architecture. Design the smallest
end-to-end path that can demonstrate whether the Work Object's riskiest
assumption holds, while making its state, authorization, failure behavior,
observability, non-goals, and rollback explicit.

## Boundaries and non-goals

This skill does:

- Receive a Design-state Work Object and its relevant evidence and decisions.
- Recommend one bounded, demoable tracer bullet before asking one question.
- Define the slice's entry and resulting state, authorization boundary,
  failure behavior, observability, exit criteria, non-goals, and rollback.
- Record only an accepted design and route it to `alawas-governance-conduct-work-object` for
  the next specialist.

This skill does not:

- Implement, test, deploy, or operate the tracer bullet.
- Create production architecture, a generalized framework, or a roadmap.
- Invent evidence, change a confirmed decision, or replace human authority.
- Persist an unaccepted recommendation as a design decision.

## Inputs and preconditions

**Required input:** a readable, schema-valid Work Object in the `design` state,
including its intent, success evidence, constraints, evidence ledger, decisions,
open questions, consequence, and sensitivity.

**Preconditions:** `alawas-governance-conduct-work-object` has discovered the workspace and
established the Work Object. The user has requested design work or has routed
the Work Object here. If the work is not in the Design state, return it to the
conductor with the missing transition rather than designing around it.

## Required capabilities

The platform adapter classifies each capability as native, manual-fallback, or
unsupported and follows `references/CAPABILITY-DEGRADATION.md` when needed.

- `file_read` — read the Work Object, relevant evidence, and prior decisions.
- `file_write` — record an accepted design through the conductor.
- `content_search` — retrieve discoverable technical constraints when relevant.
- `structured_output` — present a bounded design record.
- `user_confirmation` — obtain acceptance of the recommended design.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Designing and recommending do not authorize implementation or any external
  action.
- A low- or meaningful-consequence accepted design may be recorded only after
  the user accepts the immediately preceding recommendation in its stated
  scope.
- A high-consequence Work Object requires explicit confirmation naming the
  proposed design-record mutation. Do not stage, annotate, change status,
  append History, or make any other mutation before that confirmation.
- The recorded design authorizes only a route to the next specialist; it does
  not grant blanket authority to implement, deploy, export, or change scope.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

An explicit grilling request runs the full tracer-bullet profile. Otherwise,
nominate a Candidate Card only if an unresolved boundary would materially
change the tracer bullet. Retrieve discoverable facts first. Then:

1. State the known evidence, inference, riskiest assumption, and consequence.
2. Recommend one smallest end-to-end tracer bullet, including its trade-off.
3. Ask one decision-bearing question that accepts, rejects, or changes that
   specific recommendation.
4. Enter the continuous session only after explicit acceptance. Otherwise,
   preserve the accepted boundary and its revisit trigger.

Run the Adjacent Possibility Pass only when it changes the option space: name
the dominant assumption, generate materially distinct evidence-grounded
alternatives, state their changed assumptions and costs, and recommend one.
Explore every material branch over successive one-question turns; do not dump a
menu or generate novelty merely to make the design feel more complete.

## Skill Grilling Profile

Apply the `alawas-design-design-tracer-bullet` profile and continuous Grilling Session in
`references/SKILL-AWARE-GRILLING.md`. Start from the riskiest falsifiable
assumption, define observable exit evidence, and challenge substitutes,
containment, recovery, and result interpretation against the real code path.

## Stage workflow

### 1. Orient to the Work Object

Read the Design-state Work Object. Separate known evidence, inferences,
confirmed decisions, and unresolved questions. Identify the smallest success
evidence that would reduce uncertainty enough to choose the next move.

### 2. Name the riskiest assumption

Express one falsifiable assumption in observable terms. Prefer the uncertainty
whose failure would invalidate the most downstream work. If no assumption can
be named from the record, recommend the smallest evidence-gathering action and
ask one question rather than inventing a tracer bullet.

### 3. Recommend a bounded tracer bullet

Define one end-to-end slice with:

- **Entry and resulting state:** the smallest input, state transition, and
  visible output that demonstrate the path.
- **Authorization:** the exact user, system, or test authority required; no
  broader production access is implied.
- **Failure behavior:** expected failure modes, the safe response, and what
  must not be claimed when the assumption fails.
- **Observability:** the minimal logs, metrics, artifact, or manual evidence
  that lets a person determine whether the assumption held.
- **Non-goals:** production hardening, scale, integrations, migrations, and
  any neighboring capabilities outside the evidence-seeking slice.
- **Rollback:** how to remove, disable, or revert the slice without leaving
  durable state or user impact behind.
- **Exit criteria:** the explicit evidence that ends the tracer-bullet effort
  and the next route for either result.

Keep interfaces and data intentionally narrow. A tracer bullet may use a fake,
manual, or isolated dependency when that preserves the risk being tested.

### 4. Ask for acceptance and record only the agreement

Recommend before asking one question. Do not present equal-weight menus. After
the user accepts with the authority required by the Work Object's consequence,
route to `alawas-governance-conduct-work-object` to append a concise Decision and History entry.
Record the assumption, bounded path, safeguards, accepted trade-off, exit
criteria, rollback, and revisit trigger. Do not record hidden reasoning, full
chat transcripts, or rejected alternatives as a decision.

### 5. Route without implementing

Route the accepted design to `alawas-engineering-implement-bounded-change` (when available) or
back to `alawas-governance-conduct-work-object` with the recommended next specialist. State that
this skill does not implement the tracer bullet. If the assumption fails,
route to the appropriate decision or investigation skill; if it holds, route
to bounded implementation with the recorded constraints.

## Evidence rules

- Label source, system, lived, inference, and decision material according to
  `references/EVIDENCE-MODEL.md`.
- Treat a proposed tracer bullet as an inference until the user accepts it.
- Use only minimum-necessary Work Object context. Do not scan a personal
  archive Work Studio does not own; request a user-approved summary if personal
  context would materially change the recommendation.
- Observability evidence must distinguish an executed demo from an unrun plan.

## Work Object updates

This skill does not mutate a Work Object directly. On accepted authority, pass
the conductor a concise design record containing:

- riskiest assumption and supporting evidence;
- bounded path, entry and resulting state;
- authorization, failure behavior, observability, non-goals, and rollback;
- exit criteria, next route, and revisit trigger;
- consequence, sensitivity, and the user's explicit acceptance.

The conductor owns schema validation, optimistic concurrency, state changes,
and History. If recording is unavailable, return the exact design record and
one concrete manual instruction; do not claim it was recorded.

## Routing and termination

- **Accepted design:** route through `alawas-governance-conduct-work-object` to the next
  specialist; report the agreed scope and exit criteria.
- **Rejected or changed recommendation:** revise the one changed boundary and
  ask one new decision-bearing question only if needed.
- **Missing evidence:** route to investigation or ask for the minimum missing
  fact; do not manufacture a plausible design.
- **Capability gap:** pause or stop the affected path as classified by the
  adapter, and state what remains unverified.
- **Outside Design state:** route to the conductor without creating a design.

## Output template

```markdown
## Tracer-bullet design

- **Work Object:** <id and current state>
- **Known evidence:** <provenance-labelled facts>
- **Riskiest assumption:** <falsifiable statement>
- **Recommendation:** <smallest end-to-end slice and trade-off>
- **State and authorization:** <entry/resulting state and scoped authority>
- **Failure and observability:** <safe failure behavior and evidence signal>
- **Non-goals and rollback:** <explicit exclusions and reversal path>
- **Exit criteria and route:** <what decides the next move>
- **Decision status:** <proposed | accepted and recorded | awaiting authority>
- **Question:** <one question, only when a decision remains>
```

## Anti-patterns

- Calling a feature slice a tracer bullet without naming a falsifiable risk.
- Designing a production architecture before the critical assumption is tested.
- Asking questions before giving a recommendation.
- Recording a proposal before user acceptance.
- Omitting authorization, failure behavior, observability, non-goals, or rollback.
- Treating an adjacent possibility as useful when it does not change the option space.
- Implementing, testing, deploying, or claiming execution from a design skill.

## Final self-check

- Is the Work Object in the Design state and is its riskiest assumption explicit?
- Does the design test that assumption with the smallest demoable end-to-end path?
- Did I recommend before asking one question and preserve human authority?
- Are state, authorization, failure behavior, observability, non-goals, rollback,
  exit criteria, and revisit trigger explicit?
- Did I record only accepted design through the conductor and avoid implementation?
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
| `file_read` | `read_file` | native |
| `file_write` | `create_file / replace_string_in_file / multi_replace_string_in_file` | native |
| `content_search` | `grep_search` | native |
| `structured_output` | `—` | native |
| `user_confirmation` | `conversation turn` | native |
