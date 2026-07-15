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

Install a platform's adapter with the dependency-free maintainer tool. It
verifies checksums with the platform's `shasum`/`sha256sum` and requires **no
Python at runtime**:

```sh
# Codex user installation — available across repositories:
tools/install.sh --platform codex --global

# Codex repository pin — takes precedence inside this project:
tools/install.sh --platform codex --project .
```

| Platform | Global path | Project pin path |
|----------|-------------|------------------|
| Codex | `~/.agents/skills/` | `.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| GitHub Copilot | `~/.copilot/skills/` | `.copilot/skills/` |

Each adapter ships a `manifest.json` and a `SHA256SUMS` file with SHA-256
checksums; the installer refuses to install artifacts that do not match. A
**project-pinned** adapter always takes precedence over the global bootstrap
install — the pin is recorded in `.work-studio/adapter.lock`. Inspect which
install wins for a directory with:

```sh
tools/install.sh --platform codex --resolve .
```

Codex may discover user and repository skills with the same name. Generated
Codex adapters therefore read the lock and defer to its project-pinned copy at
runtime; a broken pin stops with an explicit error instead of silently using
the global copy.

### Verifying and testing

```sh
tools/install.sh --platform codex --verify          # verify committed artifacts
sh tests/run.sh                                     # full generator + installer suite
```

## Existing Skills

| Skill | Description |
|-------|-------------|
| [google-adk-agent-builder](skills/google-adk-agent-builder/SKILL.md) | Build and iterate on local Google ADK agents in Python — scaffolding, tools, multi-agent flows, session/memory wiring, and local dev loop |
| [conduct-work-object](skills/core/conduct-work-object/SKILL.md) | Detect, create, activate, resume, update, and close Work Objects — the canonical continuity surface of Andrelawas Work Studio |
| [pressure-test-decision](skills/core/pressure-test-decision/SKILL.md) | Resume a Work Object, identify the highest-leverage unresolved decision, recommend before asking one question, and safely persist the confirmed choice |
| [turn-signal-into-work](skills/core/turn-signal-into-work/SKILL.md) | Capture a live signal, classify its smallest durable handling, and activate a Work Object only with explicit user authority |

## Platform Adapters

Generated adapters are committed artifacts. Regenerate after editing the core:

```bash
python3 tools/generate-adapters.py           # generate all adapters
python3 tools/generate-adapters.py --check   # verify no drift
```

| Platform | Adapters | Manifest |
|----------|----------|----------|
| Codex | [conduct-work-object](adapters/codex/skills/conduct-work-object/SKILL.md), [pressure-test-decision](adapters/codex/skills/pressure-test-decision/SKILL.md), [turn-signal-into-work](adapters/codex/skills/turn-signal-into-work/SKILL.md) | [manifest.json](adapters/codex/manifest.json) |
| Claude Code | [conduct-work-object](adapters/claude-code/skills/conduct-work-object/SKILL.md), [pressure-test-decision](adapters/claude-code/skills/pressure-test-decision/SKILL.md), [turn-signal-into-work](adapters/claude-code/skills/turn-signal-into-work/SKILL.md) | [manifest.json](adapters/claude-code/manifest.json) |
| GitHub Copilot | [conduct-work-object](adapters/github-copilot/skills/conduct-work-object/SKILL.md), [pressure-test-decision](adapters/github-copilot/skills/pressure-test-decision/SKILL.md), [turn-signal-into-work](adapters/github-copilot/skills/turn-signal-into-work/SKILL.md) | [manifest.json](adapters/github-copilot/manifest.json) |

## Conformance Gate

Slice 1 is gated by a CI workflow (`.github/workflows/ci.yml`)
that enforces cross-platform behavioral equivalence:

- **Drift detection**: `python3 tools/generate-adapters.py --check` fails when
  committed artifacts diverge from source
- **Behavioral matrix**: `tools/verify-conformance.py --all` checks that all
  behavioral scenarios are documented and every platform has expected outcomes
- **Structural verification**: All adapters contain required sections,
  degradation rules, and platform declarations
- **Manifest integrity**: `manifest.json` and `SHA256SUMS` checksums are
  validated against generated files
- **Generator contract**: Unit tests verify byte-for-byte idempotence, core
  body preservation, and drift detection

The [behavioral matrix](fixtures/slice-1-behavioral-matrix.md) covers:
discovery, Work Object creation/resumption, pressure-testing, decision
persistence, concurrency/authority, and capability degradation.

Run locally:
```bash
python3 tools/verify-conformance.py --all
python3 -m unittest discover -s tests -v
```

## Planned Work Studio Skills

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
| [CAPABILITY-DEGRADATION.md](references/CAPABILITY-DEGRADATION.md) | Three-tier capability classification (native/manual-fallback/unsupported) and degradation rules |

## Behavioral Fixtures

Fixtures specify observable behavior for skills and handoffs. They are the
regression suite for instruction changes; they do not prescribe hidden
reasoning.

| Fixture | Description |
|---------|-------------|
| [personal-institution-work-studio-contract.md](fixtures/personal-institution-work-studio-contract.md) | Privacy, provenance, personalization, and handoff behavior across the two packages |

## Verification Evidence

| Evidence | Description |
|----------|-------------|
| [codex-installed-workflow-evidence.md](docs/verification/codex-installed-workflow-evidence.md) | Codex installation, fresh-task loading, resumption, and decision-persistence evidence |

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
