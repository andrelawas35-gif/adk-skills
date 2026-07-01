# ADK Skills

A collection of VS Code Copilot skills for building Google Agent Development Kit (ADK) agents and related tooling.

## What Are Skills?

Skills are reusable prompt templates and workflows that VS Code Copilot loads on demand. Each skill lives in its own folder with a `SKILL.md` file containing YAML frontmatter (name, description, triggers) and markdown instructions.

## Installing Skills

Copy any skill folder into your VS Code Copilot skills directory:

- **Windows**: `%USERPROFILE%\.copilot\skills\`
- **macOS**: `~/.copilot/skills/`
- **Linux**: `~/.copilot/skills/`

Restart VS Code or reload the Copilot extension after adding skills.

## Available Skills

| Skill | Description |
|-------|-------------|
| [google-adk-agent-builder](skills/google-adk-agent-builder/SKILL.md) | Build and iterate on local Google ADK agents in Python — scaffolding, tools, multi-agent flows, session/memory wiring, and local dev loop |

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
