# Andrelawas Work Studio

A personal skill system for carrying work from a live signal through inquiry,
decision, design, implementation, verification, deployment, observation, and
post-deployment repair. The repository also retains the original Google ADK
agent-builder skill as an implementation capability.

The accepted system design is recorded in
[docs/work-studio-planning-session-2026-07-15.md](docs/work-studio-planning-session-2026-07-15.md).

## Architecture

Skills are authored once in a portable canonical core (`skills/core/`). Platform
adapters are generated from the core plus a minimal overlay that changes only
metadata, discovery wiring, and capability mappings — never core decision logic,
authority rules, or schema semantics.

```
skills/core/                     ← Canonical source (edit here)
adapters/codex/                  ← Generated: Codex (VS Code)
adapters/claude-code/            ← Generated: Claude Code
adapters/github-copilot/         ← Generated: GitHub Copilot
tools/generate-adapters.py       ← Dependency-free generator
```

## Installing Skills

Copy the generated adapter for your platform into the appropriate skills
directory:

| Platform | Install path |
|----------|-------------|
| Codex (VS Code) | `~/.codex/skills/` |
| Claude Code | `~/.claude/skills/` |
| GitHub Copilot | `~/.copilot/skills/` |

Each adapter's `manifest.json` contains SHA-256 checksums for verification.
Project-pinned adapters take precedence over global installations.

## Existing Skills

| Skill | Description |
|-------|-------------|
| [google-adk-agent-builder](skills/google-adk-agent-builder/SKILL.md) | Build and iterate on local Google ADK agents in Python — scaffolding, tools, multi-agent flows, session/memory wiring, and local dev loop |
| [conduct-work-object](skills/core/conduct-work-object/SKILL.md) | Detect, create, activate, resume, update, and close Work Objects — the canonical continuity surface of Andrelawas Work Studio |
| [pressure-test-decision](skills/core/pressure-test-decision/SKILL.md) | Resume a Work Object, identify the highest-leverage unresolved decision, recommend before asking one question, and safely persist the confirmed choice |

## Platform Adapters

Generated adapters are committed artifacts. Regenerate after editing the core:

```bash
python3 tools/generate-adapters.py           # generate all adapters
python3 tools/generate-adapters.py --check   # verify no drift
```

| Platform | Adapters | Manifest |
|----------|----------|----------|
| Codex | [conduct-work-object](adapters/codex/skills/conduct-work-object/SKILL.md), [pressure-test-decision](adapters/codex/skills/pressure-test-decision/SKILL.md) | [manifest.json](adapters/codex/manifest.json) |
| Claude Code | [conduct-work-object](adapters/claude-code/skills/conduct-work-object/SKILL.md), [pressure-test-decision](adapters/claude-code/skills/pressure-test-decision/SKILL.md) | [manifest.json](adapters/claude-code/manifest.json) |
| GitHub Copilot | [conduct-work-object](adapters/github-copilot/skills/conduct-work-object/SKILL.md), [pressure-test-decision](adapters/github-copilot/skills/pressure-test-decision/SKILL.md) | [manifest.json](adapters/github-copilot/manifest.json) |

## Planned Work Studio Skills

- `turn-signal-into-work`
- `investigate-live-question`
- `design-tracer-bullet`
- `implement-bounded-change`
- `verify-release-evidence`
- `deploy-with-recovery`
- `diagnose-production-incident`
- `review-outcome-and-adapt`
- `maintain-working-method`

## Shared References

| Reference | Description |
|-----------|-------------|
| [WORK-OBJECT.md](references/WORK-OBJECT.md) | Work Object schema, identity rules, storage, history format |
| [AGREEMENT-LOOP.md](references/AGREEMENT-LOOP.md) | Shared reasoning protocol for decision boundaries |
| [EVIDENCE-MODEL.md](references/EVIDENCE-MODEL.md) | Provenance lanes and evidence recording rules |
| [CONSEQUENCE-AUTHORITY.md](references/CONSEQUENCE-AUTHORITY.md) | Consequence levels, sensitivity classes, and authority gates |

## Skill Structure

Each skill follows this layout:

```
skills/
  <skill-name>/
    SKILL.md          # Required — YAML frontmatter + instructions
    references/       # Optional — docs, patterns, or guides the skill references
    agents/           # Optional — sub-agent configs (e.g., openai.yaml)
```

## Contributing

1. Fork this repo
2. Add your skill folder under `skills/`
3. Ensure `SKILL.md` has valid YAML frontmatter with `name` and `description`
4. Open a PR with a description of what the skill does and when to use it

## License

MIT
