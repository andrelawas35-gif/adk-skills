---
name: alawas-design-apply-design-direction
description: "Use when natural-language design direction needs interpretation and execution; proposes concrete changes, executes only after user confirmation, and does not modify code beyond confirmed scope."
default_tier: medium
platform: github-copilot
---
# Apply Design Direction

## Governing principle

Natural language is expressive but ambiguous. When a user says "make it feel
more focused," that direction must be translated into concrete, observable
code changes before execution. This skill bridges creative intent and
implementation — it proposes an interpretation, confirms with the user, then
executes. The user retains full creative authority.

## Boundaries and non-goals

This skill does:

- Receive natural-language design direction from the user.
- Read the current discovery snapshot and token inventory to understand the
  target project's current state.
- Propose a concrete interpretation of the direction: what will change, what
  will be preserved, and what is out of scope.
- Execute code changes in the target project after user confirmation.
- Record the confirmed direction and execution as evidence.

This skill does not:

- Execute changes without user confirmation.
- Modify code beyond the confirmed scope.
- Claim the interpretation matches intent without confirmation.
- Produce authored specifications — structure emerges from conversation.
- Invent changes not grounded in current project state.

## Inputs and preconditions

**Required input:** a readable Work Object in the `decide` or `build` state
with natural-language direction from the user and at least a `[system:discovery]`
entry or `[system:token-inventory]` entry.

**Preconditions:** `alawas-design-audit-product-interface` or `alawas-design-build-design-foundation` has
run at least once. The user has provided design direction.

## Required capabilities

- `file_read` — read target project code, discovery, tokens.
- `file_write` — write code changes to target project after confirmation.
- `content_search` — find relevant code in target project.
- `structured_output` — produce the confirmed direction record.
- `user_confirmation` — confirm the interpretation before executing.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Proposing an interpretation is **low consequence** (no files modified).
- Executing confirmed changes is **meaningful consequence** — target project
  code is modified.
- Each execution is scoped to the confirmed interpretation. Changes beyond
  confirmed scope require a new confirmation cycle.
- A high-consequence Work Object requires explicit confirmation naming the
  proposed mutation. Do not stage, annotate, change status, append History,
  or make any other mutation before receiving that scoped confirmation;
  reading and recommending remain allowed.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only
its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only
under the Agreement Loop's three-part threshold. Show its Candidate Card
and wait for explicit entry; do not silently start a continuous session.

The direction lens asks:

1. Is the direction specific enough to produce observable changes?
2. Does the proposed interpretation preserve the right things?
3. Could the proposed changes have unintended effects elsewhere?

## Skill Grilling Profile

Apply the `alawas-design-apply-design-direction` profile and continuous Grilling Session
in `references/SKILL-AWARE-GRILLING.md`.

## Stage workflow

### 1. Parse direction

Read the user's natural-language direction. Identify intent: what should
change, what should stay, and what is out of bounds.

If the direction is too vague to produce observable changes (e.g., "make it
better"), ask one clarifying question before proceeding. Do not guess.

### 2. Read current state

Read the discovery snapshot, token inventory, and relevant target project
code to understand what exists now.

### 3. Propose interpretation

Propose a concrete interpretation of the direction:

- **What changes:** specific code modifications with rationale.
- **What is preserved:** explicitly unchanged elements.
- **What is out of scope:** aspects the direction does not address.

Present this to the user in natural language, grounded in the current state.

### 4. Confirm with user

Wait for explicit user confirmation. The user may:
- Accept the interpretation as-is.
- Modify the interpretation (refine, narrow, expand).
- Reject and provide new direction.

Do not proceed to execution without confirmation.

### 5. Execute confirmed changes

Write the confirmed code changes to the target project. Each change is
traceable to a specific element of the confirmed interpretation.

### 6. Record evidence

Record the confirmed direction as a `[system:design-direction]` Evidence
Ledger entry containing: the original direction, the confirmed interpretation,
and the executed changes.

## Routing and termination

**Route when:**
- Changes executed — route to `alawas-design-verify-design-implementation` for verification.
- Direction is too vague — ask the user for clarification.

**Terminate when:**
- Confirmed changes are executed and evidence recorded.
- The user withdraws or changes direction.

## Output contract

The `[system:design-direction]` Evidence Ledger entry contains:

- `direction`: the original natural-language direction
- `interpretation`: the confirmed interpretation
  - `changes`: what was changed and why
  - `preserved`: what was explicitly unchanged
  - `out_of_scope`: what was not addressed
- `execution`: list of files modified with change descriptions
- `confirmation`: how the user confirmed (explicit acceptance)

## Final self-check

- [ ] User confirmed the interpretation before any code was modified
- [ ] Every code change is traceable to the confirmed interpretation
- [ ] Preserved elements are explicit — not just "everything else"
- [ ] Vague direction was clarified, not guessed at
- [ ] Evidence entry records direction, interpretation, and execution
- [ ] Changes do not exceed confirmed scope
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

### Model tier

This skill declares `default_tier: medium`.
The platform overlay resolves this to `claude-sonnet-4-20250514`.
The prompt budget for this tier is approximately 40000 tokens (advisory).

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
