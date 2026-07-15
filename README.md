# Andrelawas Work Studio

A personal skill system for carrying work from a live signal through inquiry,
decision, design, implementation, verification, deployment, observation, and
post-deployment repair. The repository also retains the original Google ADK
agent-builder skill as an implementation capability.

The accepted system design is recorded in
[docs/work-studio-planning-session-2026-07-15.md](docs/work-studio-planning-session-2026-07-15.md).

## What Are Skills?

Skills are reusable operating instructions and workflows that Codex loads on
demand. Each skill lives in its own folder with a `SKILL.md` file containing
YAML frontmatter and Markdown instructions. The existing ADK skill may also be
adapted for other skill-capable agents.

## Installing Skills

During development, keep skills in this source repository. Install a released
skill folder into the appropriate personal skills directory:

- **Codex**: `$CODEX_HOME/skills/` (commonly `~/.codex/skills/`)
- **VS Code Copilot compatibility**: `~/.copilot/skills/`

Restart or reload the relevant agent after adding skills.

## Existing Skills

| Skill | Description |
|-------|-------------|
| [google-adk-agent-builder](skills/google-adk-agent-builder/SKILL.md) | Build and iterate on local Google ADK agents in Python — scaffolding, tools, multi-agent flows, session/memory wiring, and local dev loop |
| [conduct-work-object](skills/conduct-work-object/SKILL.md) | Detect, create, activate, resume, update, and close Work Objects — the canonical continuity surface of Andrelawas Work Studio |
| [pressure-test-decision](skills/pressure-test-decision/SKILL.md) | Resume a Work Object, identify the highest-leverage unresolved decision, recommend before asking one question, and safely persist the confirmed choice |

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
