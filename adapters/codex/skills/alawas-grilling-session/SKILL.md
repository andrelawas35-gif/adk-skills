---
name: alawas-grilling-session
description: "Use when the user explicitly requests continuous grilling or accepts a candidate; maintains one decision frontier and one question at a time; does not persist or execute without the owning skill's authority."
platform: codex
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
`alawas-conduct-work-object` only when the user asks to retain the session or an
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
| `directory_list` | `list_dir` | native |
| `structured_output` | `—` | native |
| `user_confirmation` | `conversation turn` | native |
