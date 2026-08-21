# Work Studio Configuration

This file marks the workspace root for Andrelawas Work Studio. Agents discover
it by searching upward from the current working directory, stopping at the
repository or filesystem boundary.

## Workspace

- **Name**: andrelawas-work-studio
- **Root**: https://github.com/andrelawas35-gif/adk-skills
- **Created**: 2026-07-15

## Storage

- Work Objects: `.work-studio/objects/`
- Active register: `.work-studio/active.md`
- Signal inbox: `.work-studio/inbox.md`
- Tracked in this repo's git history (2026-08-21) so Work Objects sync across
  machines via ordinary push/pull. A Work Object needing to stay off git
  (e.g. `sensitivity: restricted`) should be excluded by its specific path,
  not by reverting to the old blanket exclusion.

## Boundaries

- Repository root is the discovery boundary
- Home directory is never scanned automatically
- External stores require explicit configuration

## Active skills

- `governance-conduct-work-object` (canonical core + generated adapters)
- `thinking-pressure-test-decision` (canonical core + generated adapters)
- `thinking-turn-signal-into-work` (canonical core + generated adapters)
- `google-adk-agent-builder`

## Tools

- `tools/generate-adapters.py` — Generate platform adapters from core + overlays
