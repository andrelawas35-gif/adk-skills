---
name: alawas-model-user-flow
description: "DEFERRED. Use when user goals need mapping to interface actions; translates user objectives into goal-action-state-response flows; does not implement interface changes."
platform: codex
---
# Model User Flow

## Governing principle

An interface serves user goals, not developer abstractions. Before defining
screens or specifications, map what users are trying to accomplish to the
actions, states, and responses they will encounter. The flow model is the
bridge between user intent and interface structure.

## Boundaries and non-goals

This skill does:

- Map user goals to sequences of actions, states, and responses.
- Produce durable user flow definitions at `design/flows/<slug>.yaml` in the
  host project (DEC-11, ADR 0028).
- Reference the discovery snapshot (`[system:discovery]`) to ground flows in
  the actual interface structure.
- Identify missing routes, components, or states that the flow requires but
  the codebase lacks.

This skill does not:

- Implement any interface changes.
- Define screen layouts, component hierarchies, or navigation structure
  (that is `alawas-define-interface-architecture`).
- Create specifications or Figma output.
- Modify existing host-project code.

## Inputs and preconditions

**Required input:** a readable Work Object in the `explore` or `decide` state
with a clear user goal or set of goals to model.

**Preconditions:** a `[system:discovery]` Evidence Ledger entry exists from
`alawas-audit-product-interface`. The host project root is identifiable.

## Required capabilities

- `file_read` — read discovery snapshot and existing flows.
- `file_write` — create flow definitions in the host project.
- `structured_output` — produce YAML flow definitions.
- `user_confirmation` — confirm flow accuracy with the user.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Creating a new flow file is **meaningful consequence** — it writes a durable
  artifact to the host project.
- Reading existing flows and the discovery snapshot is low consequence.
- Modifying an existing flow file is meaningful consequence.
- A high-consequence Work Object requires explicit confirmation naming the
  proposed mutation. Do not stage, annotate, change status, append History,
  or make any other mutation before receiving that scoped confirmation;
  reading and recommending remain allowed.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only
its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only
under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

The flow-modeling lens asks:

1. Does the flow represent a real user goal, not a system process?
2. Are all states reachable and all transitions valid?
3. Does the flow account for error states and edge cases?

## Skill Grilling Profile

Apply the `alawas-model-user-flow` profile and continuous Grilling Session in
`references/SKILL-AWARE-GRILLING.md`.

## Stage workflow

### 1. Identify user goals

From the Work Object's intent and user input, identify the user goals to
model. Each goal becomes a separate flow.

### 2. Map goal to actions

For each goal, define the sequence of user actions (clicks, inputs,
navigation) that accomplish the goal. Reference discovered routes and
components from the `[system:discovery]` entry.

### 3. Define states and responses

For each action, define: the pre-state (what the user sees), the action
itself, the post-state (what changes), and the system response (feedback,
navigation, data change). Include error states and recovery paths.

### 4. Identify gaps

Compare the flow against the discovery snapshot. Report routes, components,
or states that the flow requires but the codebase lacks. These gaps inform
downstream skills about what needs to be built.

### 5. Write flow definition

Create `design/flows/<slug>.yaml` with the complete flow definition. The
`design/flows/` directory is created if it does not exist (meaningful
consequence — user confirmation required).

## Routing and termination

**Route when:**
- Flow definition is written — return to `alawas-conduct-work-object`.
- Gaps require design decisions — route to `alawas-define-interface-architecture`.

**Terminate when:**
- All identified user goals have flow definitions.
- The user confirms the flows are accurate.

## Output contract

Each flow file at `design/flows/<slug>.yaml` contains:

- `goal`: the user objective this flow serves
- `preconditions`: what must be true before the flow starts
- `steps`: ordered list of action-state-response triples
- `error_paths`: alternative paths for error conditions
- `gaps`: routes, components, or states not yet in the codebase

## Final self-check

- [ ] Flow definitions are durable files at `design/flows/`
- [ ] Flows reference discovered routes and components, not assumptions
- [ ] Error states and edge cases are modeled
- [ ] Gaps between flow requirements and codebase are reported
- [ ] No host-project code was modified
- [ ] User confirmed flow accuracy before recording
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

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
| `file_write` | `create_file / replace_string_in_file` | native |
| `structured_output` | `—` | native |
| `user_confirmation` | `conversation turn` | native |
