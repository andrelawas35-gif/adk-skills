---
name: alawas-governance-maintain-working-method
description: "Use when repeated workflow evidence may justify a reusable rule; trials, revises, or retires a bounded working method; does not promote exceptions or temporary guardrails into permanent policy silently."
default_tier: high
platform: codex
---
# Maintain Working Method

## Governing principle

A Workflow Candidate is an evidence-bearing proposal, not a rule waiting to
be declared true. Keep its origin, supporting and contrary evidence, bounded
tests, and uncertainty durable. Promotion creates a separate, linked,
versioned Working Method only when the scoped proof and explicit human
confirmation exist.

## Boundaries and non-goals

This skill does:

- Create, retrieve, revise, retire, and review Workflow Candidates arising
  from permitted Work Studio work such as an outcome-review.
- Maintain a candidate's immutable identity, proposed rule, scope, origin
  references, append-only evidence and lifecycle events, including bounded test references, timestamps, and optional approved Evidence Bridge reference.
- Assess attributable bounded-test evidence as `supported`, `contradicted`,
  or `insufficient`; distinguish a scoped result from a universal claim.
- Promote an eligible candidate to a separate, linked, versioned Working Method
  after explicit human confirmation.

This skill does not:

- Read, search, copy, or mutate Personal Institution records, chat history,
  external systems, production data, or personal archives.
- Treat `none observed within scope` as `no contradiction exists`, turn a
  candidate into a rule in place, or infer proof from an unrun test.
- Implement, deploy, export, share, migrate a schema, create telemetry, or
  automatically apply a Working Method to other Work Objects.

## Inputs and preconditions

**Required input:** a bounded candidate maintenance request and enough local
Work Studio material to identify the proposed rule, scope, and origin.

**For promotion:** one completed bounded Work Object with a predeclared
hypothesis, scope, and signal; an attributable `supported`, `contradicted`, or
`insufficient` result; a documented contrary-evidence review; and explicit
human confirmation of the exact separate Working Method to create.

If a required field, completed test, result attribution, contrary-evidence
review, approval, or authority is absent, retain the candidate and state the
gap. Do not promote it.

## Required capabilities

The platform adapter classifies every capability as native, manual-fallback,
or unsupported and follows `references/CAPABILITY-DEGRADATION.md` when needed.

- `file_read` and `content_search` — read only permitted local Work Studio
  records, candidate records, and user-approved bridge summaries.
- `file_write` — pass a candidate or Working Method update to
  `alawas-governance-conduct-work-object` for durable persistence.
- `user_confirmation` — obtain the exact acceptance required for promotion or
  a meaningful-consequence update.
- `structured_output` — return a bounded candidate assessment and next route.

## Consequence and authority rules

**Authority gate:** Promotion of a Workflow Candidate to a Working Method
requires explicit human confirmation at ALL consequence levels. Referencing
an Evidence Bridge requires explicit human confirmation. Before proceeding:
(1) verify the receiving Work Object's consequence and sensitivity fields,
(2) request confirmation naming the candidate, bounded scope, and target,
(3) record a structured authority History entry per the authority recording
contract in `references/CONSEQUENCE-AUTHORITY.md`.

- Reading and recommending do not authorize a candidate mutation, promotion,
  evidence transfer, export, or application of a method.
- A low- or meaningful-consequence candidate update may be recorded only with
  the authority required by the receiving Work Object. A high-consequence
  update requires confirmation naming that exact mutation before any write.
  Do not stage, annotate, change status, append History, or make any other
  mutation before that confirmation.
- Promotion always requires explicit human confirmation, even when the
  candidate has supporting evidence. The confirmation names the candidate,
  bounded scope, target Working Method, and version relationship.
- An Evidence Bridge may be referenced only when the user has approved the
  minimum necessary bridge for this receiving Work Object. Record its
  provenance and sensitivity; do not copy its source material.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its
stage-specific lens below. Do not ask for blanket authority to promote future
candidates, collect evidence, or apply a Working Method.

Outside an explicit grilling request, nominate a Grilling Candidate only under
the Agreement Loop's three-part threshold. Show its Candidate Card and wait for
explicit entry; do not silently start a continuous session.

## Skill Grilling Profile

Apply the `alawas-governance-maintain-working-method` profile and continuous Grilling Session in
`references/SKILL-AWARE-GRILLING.md`. Start from observed behavior and outcome,
seek contrary contexts, bound applicability and exceptions, and require a
reviewable trial before promotion. Keep attributed personal-fit defaults
separate from shared policy

## Candidate record contract

Create or maintain a candidate with these minimum fields:

```markdown
## Workflow Candidate

- **Identity:** <immutable id>
- **Proposed rule:** <testable instruction>
- **Scope:** <bounded context, exclusions, and intended user>
- **Origin references:** <linked Work Objects, reviews, or artifacts>
- **Evidence and lifecycle events:** <append-only, dated, attributable entries>
- **Bounded test references:** <predeclared hypothesis, scope, signal, result>
- **Timestamps:** <created, updated, and event times>
- **Evidence Bridge:** <none | approved reference, provenance, sensitivity>
- **Status:** <active | promoted | retired>
- **Relationships:** <none | supersedes | superseded by | promoted to>
```

Identity and prior evidence/lifecycle entries are immutable and append-only.
Correct a factual error with a dated correction event that preserves the
original claim and attribution. A material rule or scope revision creates a
linked successor candidate using `supersedes`; do not overwrite the earlier
candidate. Retirement records why the candidate is no longer active and does
not erase its evidence.

## Evidence rules

Apply `references/EVIDENCE-MODEL.md`.

- Label direct local observations `[system]` or `[testimony]`, interpretations
  `[inference]`, approval `[decision]`, and missing material `[gap]`.
- Preserve supporting evidence and contrary evidence with their source,
  date, scope, and limits. Contradictory evidence is not a reason to edit
  history or silently narrow a rule.
- A contrary-evidence review states the searched permitted sources, review
  scope and period, what was found, what was unavailable, and the resulting
  limitation. `none observed within scope` means only that no contrary evidence
  was found in that stated review; it never means no contradiction exists.
- An approved Evidence Bridge is a reference, not authorization to inspect the
  Personal Institution. If no approved bridge exists, record the absence as an
  uncertainty and continue only with permitted local evidence.

## Stage workflow

### 1. Establish the candidate boundary

Read the proposed rule, intended scope, origin references, current status,
evidence events, test references, consequence, sensitivity, and authority.
If the candidate originated from an outcome-review, preserve that origin rather
than treating the review conclusion as universal proof. Recommend the smallest
safe maintenance move before asking one decision-bearing question, following
`references/AGREEMENT-LOOP.md`.

### 2. Create or retrieve without inventing evidence

For a new candidate, assign immutable identity and capture only the minimum
record fields. For an existing one, retrieve its record and append new material
only when its source and scope are attributable. Do not manufacture an origin,
test result, Evidence Bridge, or contrary-evidence review from chat context.

### 3. Record bounded tests and assess their result

Each test reference must name a completed Work Object, its predeclared
hypothesis, bounded scope, signal, result, and attribution. Assess the result:

- `supported` — the stated signal supports the proposed rule within the
  completed test's scope.
- `contradicted` — attributable evidence conflicts with the proposed rule in
  the stated scope.
- `insufficient` — the test, signal, attribution, or evidence is missing or
  cannot assess the rule.

One completed test provides scoped confidence only. It does not establish a
universal method or authorize broader application.

### 4. Review contrary evidence and recommend the next move

Document the contrary-evidence review before recommending retain, revise,
retire, run another bounded test, or propose promotion. State supporting and
contrary evidence separately, including unresolved limits. Recommend one move
and its trade-off before asking for the needed decision; do not request blanket
authority for future methods or evidence collection.

### 5. Promote only through a separate record

Promote only when all promotion preconditions are present. On explicit human
confirmation, route to `alawas-governance-conduct-work-object` to create a separate, linked,
versioned Working Method. The new record names its source candidate, version,
scoped rule, scope, evidence summary, contrary-evidence boundary, and
confirmation. Mark the candidate `promoted` with a link to the new record; do
not replace candidate evidence with the rule.

### 6. Revise or retire safely

When new evidence changes the rule or scope materially, create a successor
candidate linked by `supersedes`, append the reason, and retain the predecessor.
When the candidate is no longer useful, retire it with rationale and links to
the evidence. A retired or contradicted candidate remains retrievable; it is
not deleted or converted into a successful Working Method.

## Work Object updates

Return a concise record to `alawas-governance-conduct-work-object` containing the candidate
identity, proposed rule, scope, origin references, append-only events, test
reference and assessment, supporting and contrary evidence, contrary-evidence
review boundary, Evidence Bridge reference or absence, decision status,
relationship, next action, and uncertainty. The conductor owns schema
validation, durable record placement, History, and state/status transitions.

## Routing and termination

- **Candidate created or updated:** route the bounded record to
  `alawas-governance-conduct-work-object`; do not apply the rule.
- **Supported but not promotable:** retain the candidate, state the missing
  promotion condition, and recommend one bounded next move.
- **Contradicted:** preserve the evidence and recommend revision, retirement,
  or another bounded inquiry; do not promote.
- **Insufficient:** record the gap and route to the smallest authorized test
  or investigation; do not treat absence as support.
- **Promotion accepted:** route to `alawas-governance-conduct-work-object` for a separate,
  linked, versioned Working Method only.
- **Manual-fallback capability:** pause with one concrete user-run instruction
  and mark the affected evidence or verification unverified.
- **Unsupported capability:** stop the affected path, record the limitation,
  and route to a supported platform or the user.

## Output template

```markdown
## Workflow Candidate maintenance

- **Candidate:** <immutable id, status, relationship>
- **Proposed rule and scope:** <testable rule, limits, exclusions>
- **Origin:** <linked outcome-review or other permitted reference>
- **Evidence:** <supporting, contrary, attribution, and limits>
- **Contrary-evidence review:** <sources, scope, period, findings, unavailable material>
- **Bounded test:** <Work Object, hypothesis, signal, result: supported | contradicted | insufficient>
- **Evidence Bridge:** <none | approved reference, provenance, sensitivity>
- **Recommendation:** <retain | revise | retire | bounded test | propose promotion>
- **Decision status:** <proposed | accepted and recorded | awaiting authority>
- **Promotion:** <none | separate linked versioned Working Method>
- **Next route:** <conductor | investigate | decision | manual fallback>
```

## Anti-patterns

- Declaring a candidate a working method because it sounds plausible or has one
  favorable observation.
- Treating no contrary evidence found within a review scope as proof that none
  exists.
- Overwriting candidate identity, scope, prior evidence, or lifecycle history.
- Reading personal records through an Evidence Bridge reference.
- Promoting, deploying, or applying a method without the separate authority
  required for that act.

## Final self-check

- Does the candidate retain immutable identity and append-only evidence,
  lifecycle, and bounded-test events?
- Are supporting evidence, contrary evidence, inference, decision, and
  uncertainty clearly distinct and attributable?
- Does the contrary-evidence review say `none observed within scope` only when
  that is the actual bounded finding?
- Is every `supported`, `contradicted`, or `insufficient` result tied to a
  completed bounded test rather than a universal claim?
- Is any promoted method separate, linked, versioned, scoped, and explicitly
  human-confirmed?
- Did I avoid external, Personal Institution, implementation, deployment,
  export, and automatic-application work without separate authority?
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
| `file_write` | `create_file / replace_string_in_file` | native |
| `user_confirmation` | `conversation turn` | native |
| `structured_output` | `—` | native |
