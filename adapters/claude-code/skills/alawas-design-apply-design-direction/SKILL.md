---
name: alawas-design-apply-design-direction
description: "Use when natural-language design direction needs interpretation and execution; proposes concrete changes, executes only after user confirmation, and does not modify code beyond confirmed scope."
default_tier: medium
platform: claude-code
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
- Execute code changes in the target project after user confirmation (Path A).
- Route to Claude Design for design-tool execution when the direction requires
  visual or structural generation (Path B).
- Record the confirmed direction and execution as evidence.

This skill does not:

- Execute changes without user confirmation.
- Modify code beyond the confirmed scope.
- Execute Claude Design operations without explicit human confirmation.
- Claim the interpretation matches intent without confirmation.
- Produce authored specifications — structure emerges from conversation.
- Invent changes not grounded in current project state.

## Inputs and preconditions

**Required input:** a readable Work Object in any state, where design direction
has been given and not yet executed, with at least a `[system:discovery]` entry
or `[system:token-inventory]` entry. No lifecycle state is required or excluded.

**Preconditions:** `alawas-design-audit-product-interface` or `alawas-design-build-design-foundation` has
run at least once. The user has provided design direction.

## Required capabilities

**Path A (code-first):**
- `file_read` — read target project code, discovery, tokens.
- `file_write` — write code changes to target project after confirmation.
- `content_search` — find relevant code in target project.
- `structured_output` — produce the confirmed direction record.
- `user_confirmation` — confirm the interpretation before executing.

**Path B (Claude Design):**
All Path A capabilities, plus:
- `claude_design` — access Claude Design MCP tools for design generation and editing.

> Path B requires pre-invocation authentication via the `claude_design` capability.
> If the auth probe fails, Path B degrades to manual-fallback with the instruction
> to authenticate. Path B never falls back silently to Path A — the fallback is
> explicit and requires user confirmation.

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

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

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

### 5. Route execution path

Choose the execution path based on the confirmed interpretation:

- **Path A (code-first):** The direction can be implemented through code
  changes alone. Proceed to step 5a.
- **Path B (Claude Design):** The direction requires design-tool execution
  (visual generation, structural layout, asset creation). Proceed to step 5b.

The path is chosen by the user during the confirmation step (step 4).
Explicitly state which path is recommended and why.

> **Path B → Path A fallback:** If Claude Design is unavailable (auth failure,
> capability not declared, runtime does not support MCP), Path B does NOT
> silently fall back to Path A. The agent must report the unavailability and
> ask the user: (1) authenticate and retry Path B, (2) switch to Path A with
> the understanding that design-tool output will be unavailable, or (3) pause.

### 5a. Execute Path A (code-first)

Write the confirmed code changes to the target project. Each change is
traceable to a specific element of the confirmed interpretation.

### 5b. Execute Path B (Claude Design)

**Precondition — version freshness check:** Before any Claude Design revision,
read the latest `[system:design-project-ref]` entry for the target project.
If a newer version ref exists than the one the agent loaded, report the
version conflict to the user and pause. Do not proceed with a stale ref.

**Authentication probe:** Before invoking any Claude Design tool, run the
pre-invocation authentication probe via the `claude_design` capability.
If the probe fails, report the auth failure and offer the Path B → Path A
fallback options above. Do not attempt to cache, infer, or reuse credentials.

**No unattended invocation:** Every Claude Design mutation (create, revise,
sync, export) requires the user's explicit confirmation for the specific
operation. No background, batched, or automatically retried invocations.

**No automatic retry:** If a Claude Design operation fails, report the
failure and ask the user how to proceed. Do not automatically retry.

**Runtime and model attribution:** Record the runtime platform and the
Claude Design model used for each operation in the evidence entry.

### 6. Record evidence

Record the confirmed direction as a `[system:design-direction]` Evidence
Ledger entry (see Output contract below for format).

For Path B, additionally record:
- `[system:design-project-ref]` with `claude-design:` provider prefix
- `[system:design-approval]` with version ref, brief reference, and scope
- Runtime platform and model attribution on each evidence entry

## Routing and termination

**Route when:**
- Path A executed — route to `alawas-design-verify-design-implementation` for verification.
- Path B executed — route to `alawas-design-verify-design-implementation` for verification
  (brief-to-browser comparison; see that skill's governing principle).
- Direction is too vague — ask the user for clarification.

**Terminate when:**
- Confirmed changes are executed and evidence recorded.
- The user withdraws or changes direction.
- Claude Design is unavailable and the user chooses to pause.

## Output contract

The `[system:design-direction]` Evidence Ledger entry contains:

- `direction`: the original natural-language direction
- `interpretation`: the confirmed interpretation
  - `changes`: what was changed and why
  - `preserved`: what was explicitly unchanged
  - `out_of_scope`: what was not addressed
- `execution`: list of files modified with change descriptions (Path A) or
  Claude Design artifact references with `claude-design:` provider prefix (Path B)
- `confirmation`: how the user confirmed (explicit acceptance)
- `path`: `A` or `B` — which execution path was used
- `evidence_refs`: list of related evidence entry references

**Path B only — `[system:design-direction]` also contains:**
- `brief`: the structured implementation brief (see Brief self-sufficiency below)
- `runtime`: the runtime platform that executed Path B
- `model`: the Claude Design model used

### Brief self-sufficiency

The implementation brief is the portability contract. An agent without Claude
Design access must be able to implement the approved design from the brief
alone. The brief must contain:

- `design_intent`: what the design achieves in user-observable terms
- `visual_spec`: layout, spacing, color, typography, and responsive behaviour
  at each affected viewport
- `structural_changes`: additions, modifications, or removals to the component
  tree or DOM structure
- `assets`: references to generated or modified assets (`claude-design:` URIs)
- `acceptance_criteria`: observable conditions that verify the implementation
  matches the brief

### Evidence entry formats

#### `[system:design-project-ref]`

Recorded when a Claude Design project or file is created or referenced.

- `provider`: `claude-design`
- `project_ref`: `claude-design:<project-identifier>`
- `version_ref`: the git revision or design-file version at time of reference
- `purpose`: why the project was created or referenced
- `runtime`: the runtime platform that created the reference

#### `[system:design-approval]`

Recorded when the user approves a design for implementation.

- `version_ref`: the git revision or design-file version being approved
- `brief_ref`: reference to the `[system:design-direction]` entry containing
  the implementation brief
- `scope`: what is approved (specific changes, preserved elements, exclusions)
- `approver`: the user who approved
- `runtime`: the runtime platform that recorded the approval

### Authority tiers

Claude Design operations are classified by consequence:

| Tier | Operations | Consequence | Gate |
|------|-----------|-------------|------|
| Low | Authentication probe, read-only queries, version-freshness check | Low | None beyond capability declaration |
| Meaningful | Create new design, revise existing design, sync to project | Meaningful | Human confirmation per operation |
| High | Export to external format, share with external audience | High | Human confirmation naming the exact export scope |

Authority tier gates apply **in addition to** the WO's consequence level.

## Final self-check

- [ ] User confirmed the interpretation before any execution (Path A or Path B)
- [ ] Every code change is traceable to the confirmed interpretation
- [ ] Preserved elements are explicit — not just "everything else"
- [ ] Vague direction was clarified, not guessed at
- [ ] Evidence entry records direction, interpretation, and execution
- [ ] Changes do not exceed confirmed scope
- [ ] Path A/B routing is explicit, never a silent fallback
- [ ] Path B operations have human confirmation per operation
- [ ] Version freshness was checked before any Claude Design revision
- [ ] Authentication probe was run before any Claude Design invocation
- [ ] Runtime and model attribution recorded on Claude Design evidence entries
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

### Epistemic rules

This skill uses the **essential 3‑tag system** (`references/epistemic/epistemic-rules-essential.md`).

The epistemic tier is resolved from the skill's `default_tier` (medium).
**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the epistemic tier is upgraded to at least `medium` (essential 3‑tag).
When `consequence: high`, the epistemic tier is upgraded to the strongest
available tier (full 6‑tag).
`actual_epistemic_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

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
| `file_read` | `Read` | native |
| `file_write` | `Write / Edit` | native |
| `content_search` | `Grep` | native |
| `structured_output` | `—` | native |
| `user_confirmation` | `conversation turn` | native |
| `claude_design` | `MCP tool discovery (runtime)` | native |
