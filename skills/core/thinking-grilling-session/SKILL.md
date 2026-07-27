---
name: grilling-session
default_tier: high
description: "Use when the user explicitly requests continuous grilling or accepts a candidate; maintains one decision frontier and one question at a time; does not persist or execute without the owning skill's authority."
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
`conduct-work-object` only when the user asks to retain the session or an
accepted decision needs durable continuity. The conductor alone checkpoints
durable session state.

Use the receiving profile's gates, escalation, and pressure scenario as a
lens; do not let a profile replace the engine or restart the conversation.
Stage skills may nominate a Grilling Candidate under the Agreement Loop's
three-part threshold, but must show its Candidate Card and wait for explicit
entry rather than silently starting this session.

## Subject resolution

When no explicit subject is named, the five-rung evidence inspection passes
through the steps named in `references/AGREEMENT-LOOP.md` and this skill's
entry instructions. If those rungs all miss, the following ladder closes the
gap (rungs 6-7):

- **rung 6** — resolve to `active.md` Primary and state it in the Context
  Card as a correctable claim with its basis. Permitted without new machinery
  by the existing correctability guarantee at `AGREEMENT-LOOP.md:68`.
- **rung 7** — when there is no register, no Primary, or the guess is
  rejected: construct nothing. No Context Card, no profile, no frontier.
  Ask one wide question about what is unresolved, and resolve the subject
  from the answer.

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
