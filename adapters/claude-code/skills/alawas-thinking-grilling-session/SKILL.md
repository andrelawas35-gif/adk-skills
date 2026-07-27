---
name: alawas-thinking-grilling-session
description: "Use when the user explicitly requests continuous grilling or accepts a candidate; maintains one decision frontier and one question at a time; does not persist or execute without the owning skill's authority."
default_tier: high
platform: claude-code
---
# Grilling Session

## Governing principle

This is the visible entry point for continuous Work Studio grilling. It owns
the live conversation; `AGREEMENT-LOOP.md` is the sole normative engine.

## Entry and delegation

On an explicit grilling request in a Work Studio-pinned project, follow
`references/AGREEMENT-LOOP.md` in full. Inspect enough local evidence to choose
and state a correctable initial profile from
`references/SKILL-AWARE-GRILLING.md`, then ask exactly one question.

Run ephemerally unless an active Work Object is relevant. Do not create,
resume, or mutate a Work Object merely to begin grilling. Route to
`alawas-governance-conduct-work-object` only when the user asks to retain the session or an
accepted decision needs durable continuity. The conductor alone checkpoints
durable session state.

Use the receiving profile's gates, escalation, and pressure scenario as a
lens; do not let a profile replace the engine or restart the conversation.
Stage skills may nominate a Grilling Candidate under the Agreement Loop's
three-part threshold, but must show its Candidate Card and wait for explicit
entry rather than silently starting this session.

## Required capabilities

- `file_read` — inspect relevant code, records, and local instructions.
- `content_search` — locate discoverable evidence before questioning.
- `directory_list` — identify scoped project evidence when necessary.
- `structured_output` — present a compact Context Card and one question.
- `user_confirmation` — obtain explicit promotion or mutation authority.

## Consequence and authority rules

The engine has no independent artifact-mutation authority. If a proposed
handoff would create or update a high-consequence Work Object, the confirmation
must name that mutation. Do not stage, annotate, change status, append History,
or make any other mutation before receiving that scoped confirmation.

## Boundaries

- In a Work Studio-pinned project, explicit `grill me` and `grill this` use
  this skill rather than the generic `grilling` skill.
- Outside that project context, leave generic grilling to the generic skill.
- Do not implement, deploy, write artifacts, or claim convergence without the
  authority and confirmation required by the Agreement Loop.
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

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
| `directory_list` | `Bash ls` | native |
| `structured_output` | `—` | native |
| `user_confirmation` | `conversation turn` | native |
