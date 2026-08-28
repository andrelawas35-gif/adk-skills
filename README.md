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
adapters/lm-studio-bionic/       ← Generated: LM Studio Bionic
adapters/opencode/               ← Generated: OpenCode
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
| GitHub Copilot | `~/.copilot/skills/` | `.github/skills/` |
| LM Studio Bionic | `~/.lmstudio/skills/` | `.lmstudio/skills/` |
| OpenCode | `~/.config/opencode/skills/` | `.opencode/skills/` |

Each adapter ships a `manifest.json` and a `SHA256SUMS` file with SHA-256
checksums; the installer refuses to install artifacts that do not match. A
**project-pinned** adapter always takes precedence over the global bootstrap
install — each platform pin is recorded in `.work-studio/adapter.<platform>.lock`. Inspect which
install wins for a directory with:

```sh
tools/install.sh --platform codex --resolve .
```

Codex may discover user and repository skills with the same name. Generated
Codex adapters therefore read the lock and defer to its project-pinned copy at
runtime; a broken pin stops with an explicit error instead of silently using
the global copy.

### Claude Code on the web / mobile

Claude Code on the web runs each session in an ephemeral container, so a global
`~/.claude/skills/` install does not survive between sessions. There are two
ways to make these skills available on mobile:

- **One project** — pin the Claude Code adapter into the repo at
  `.claude/skills/` (committed, travels with the repo). Every web/mobile
  session that opens the repo auto-discovers it.
- **Every project** — install globally at session startup from the
  environment's **setup script** so any repo opened in that environment
  inherits the skills. Because the setup script runs on every startup, the
  ephemerality is moot:

  ```sh
  curl -fsSL https://raw.githubusercontent.com/andrelawas35-gif/adk-skills/master/tools/install-global.sh | sh
  ```

  `tools/install-global.sh` clones this repo (or reuses an existing checkout)
  and delegates to the checksum-verifying `install.sh --platform claude-code
  --global`. Override the source ref with `ADK_REF` (e.g. a release tag for a
  stable pin) or the clone URL with `ADK_REPO`.

### Verifying and testing

```sh
tools/install.sh --platform codex --verify          # verify committed artifacts
sh tests/run.sh                                     # full generator + installer suite
```

## Existing Skills

Canonical skills are namespace-prefixed by role so the capability is visible at
the point of invocation:

- `design-*`: design discovery, architecture, tracer bullets, and verification
- `engineering-*`: bounded implementation and release verification
- `governance-*`: Work Object continuity, method, scorecards, and review
- `operations-*`: deployment and production incident response
- `research-*`: live-question investigation
- `thinking-*`: signal capture, ideation, decision pressure-testing, and grilling

The original Google ADK builder remains at
[skills/google-adk-agent-builder/SKILL.md](skills/google-adk-agent-builder/SKILL.md).

## Platform Adapters

Generated adapters are committed artifacts. Regenerate after editing the core:

```bash
python3 tools/generate-adapters.py           # generate all adapters
python3 tools/generate-adapters.py --check   # verify no drift
```

| Platform | Adapters | Manifest |
|----------|----------|----------|
| Codex | Namespace-prefixed generated skills | [manifest.json](adapters/codex/manifest.json) |
| Claude Code | Namespace-prefixed generated skills | [manifest.json](adapters/claude-code/manifest.json) |
| GitHub Copilot | Namespace-prefixed generated skills | [manifest.json](adapters/github-copilot/manifest.json) |
| LM Studio Bionic | Namespace-prefixed generated skills | [manifest.json](adapters/lm-studio-bionic/manifest.json) |
| OpenCode | Namespace-prefixed generated skills | [manifest.json](adapters/opencode/manifest.json) |

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

## Shared References

| Reference | Description |
|-----------|-------------|
| [WORK-OBJECT.md](references/WORK-OBJECT.md) | Work Object schema, identity rules, storage, history format |
| [AGREEMENT-LOOP.md](references/AGREEMENT-LOOP.md) | Canonical runtime engine for continuous grilling, session modes, lens selection, and durable continuity |
| [SKILL-AWARE-GRILLING.md](references/SKILL-AWARE-GRILLING.md) | Stage-specific grilling lenses: gates, escalation paths, and pressure scenarios |
| [EVIDENCE-MODEL.md](references/EVIDENCE-MODEL.md) | Provenance lanes and evidence recording rules |
| [CONSEQUENCE-AUTHORITY.md](references/CONSEQUENCE-AUTHORITY.md) | Consequence levels, sensitivity classes, and authority gates |
| [CAPABILITY-DEGRADATION.md](references/CAPABILITY-DEGRADATION.md) | Three-tier capability classification (native/manual-fallback/unsupported) and degradation rules |

## Behavioral Fixtures

Fixtures specify observable behavior for skills and handoffs. They are the
regression suite for instruction changes; they do not prescribe hidden
reasoning.

| Fixture | Description |
|---------|-------------|
| [slice-2-design-tracer-bullet.md](fixtures/slice-2-design-tracer-bullet.md) | Bounded tracer-bullet recommendation, acceptance, risk treatment, rollback, and routing behavior |
| [slice-2-implement-bounded-change.md](fixtures/slice-2-implement-bounded-change.md) | Accepted bounded implementation, working-tree preservation, continuous verification, deviation, and degradation behavior |
| [slice-2-verify-release-evidence.md](fixtures/slice-2-verify-release-evidence.md) | Proportionate acceptance, recovery, dependency, privacy, security, and evidence-gap verification without release claims |
| [slice-3-investigate-live-question.md](fixtures/slice-3-investigate-live-question.md) | Primary-source investigation, reality contact, contradiction handling, unresolved outcomes, and Evidence Bridge gating |
| [slice-3-deploy-with-recovery.md](fixtures/slice-3-deploy-with-recovery.md) | Authorized incremental deployment, readiness gates, rollback, sanitized evidence, and Observe routing |
| [slice-3-diagnose-production-incident.md](fixtures/slice-3-diagnose-production-incident.md) | Evidence-safe intake, containment, affected-path recovery, ranked diagnosis, dependency gaps, and bounded prevention |

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
