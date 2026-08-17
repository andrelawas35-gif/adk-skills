# Repository Operating Contract

## Purpose

Orient any agent working in this repository quickly. This file is a thin
pointer layer — it names where the real rules live, and does not restate
them.

## Canonical locations

- Documentation discovery and lifecycle rules: `WORKSPACE-DOCUMENTATION-CONTRACT.md`
- Consequence and authority ladder: `references/CONSEQUENCE-AUTHORITY.md`
- Evidence provenance tags and rules: `references/AGREEMENT-LOOP.md`, `references/EVIDENCE-MODEL.md`
- Work Object schema and lifecycle: `references/WORK-OBJECT.md`
- How responses are written to the director: `references/DIRECTOR-LANGUAGE.md` (see also `CLAUDE.md`, scoped to conversational tone)
- Skill procedures: `skills/core/*/SKILL.md`
- Constitutionally protected files: `.work-studio/constitutional-files.list`

## Before starting work

Inspect `WORKSPACE-DOCUMENTATION-CONTRACT.md` before reading or creating an
artifact — it is the single discovery source for canonical project records.
Do not search plausible alternatives and pick one.

## Skill selection

Route through `skills/core/governance-conduct-work-object/SKILL.md`, which
discovers or creates the relevant Work Object and routes to the appropriate
specialist skill by lifecycle state.

## Modification rules

All canonical mutations route through `python3 -m tools.ws`
(`--expect-updated` on every mutating command). Files listed in
`.work-studio/constitutional-files.list` require a linked authority record
to modify. See `references/CONSEQUENCE-AUTHORITY.md` for the full authority
ladder.

## Verification

Run `python3 tools/generate-adapters.py --check`, `python3 -m tools.ws
validate`, and `python3 -m pytest tests/` before treating a change as
complete.

## Escalation

A material new decision, authority boundary, or unresolved conflict routes
to `skills/core/thinking-pressure-test-decision/SKILL.md` or back to
`skills/core/governance-conduct-work-object/SKILL.md` — see
`references/CONSEQUENCE-AUTHORITY.md` for what requires explicit human
confirmation before proceeding.
