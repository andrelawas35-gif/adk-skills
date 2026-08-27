# Work Studio System Reference

> **Status:** Current-system reference for Work Studio v0.1.0, inspected 2026-08-22.  
> **Work Object:** `2026-08-22-033`  
> **Deliverable type:** Report  
> **Scope:** Implemented repository structure, operating workflow, deterministic `ws` CLI, runtime graph CLIs, adapter installation, maintenance, verification, backup, and recovery.  
> **Not a roadmap:** This document describes observable current behavior. It does not propose new architecture.

## 1. What Work Studio is

Work Studio is a local-first system for carrying work from an incoming signal through inquiry, decision, design, implementation, verification, release, observation, and review. Its durable unit of continuity is the **Work Object**: a Markdown record containing validated YAML frontmatter plus intent, success evidence, constraints, decisions, evidence, questions, next move, and append-only history. `[system: README.md; references/WORK-OBJECT.md; tools/ws/schema.py]`

The system has four cooperating layers: `[system: work-studio/kernel-manifest.yaml; pyproject.toml]`

1. **Canonical protocol and skills** — portable rules in `skills/core/`, shared contracts in `references/`, and the artifact registry in `WORKSPACE-DOCUMENTATION-CONTRACT.md`.
2. **Generated platform adapters** — platform-specific skill packages in `adapters/codex/`, `adapters/claude-code/`, and `adapters/github-copilot/`.
3. **Deterministic state tooling** — the dependency-free `ws` CLI in `tools/ws/`, which validates and mutates `.work-studio/` records.
4. **Optional checkpointed runtime** — LangGraph-based orchestration in `runtime/`, with SQLite checkpoints, resumable/forkable threads, research routing, engineering handoffs, and a business operating router.

The repository also includes an MCP server package in `mcp_server/`, static operational views (`command-center.html` and `asset-workbench.html`), behavioral fixtures, tests, ADRs, and design records. `[system: repository tree; pyproject.toml]`

## 2. Source-of-truth hierarchy

Use these sources in this order when determining current behavior:

| Concern | Canonical location | Notes |
|---|---|---|
| Documentation discovery and lifecycle | `WORKSPACE-DOCUMENTATION-CONTRACT.md` | Registry of canonical artifact types and owners. |
| Work Object schema and lifecycle | `references/WORK-OBJECT.md` | Identity, required fields, states, status, history. |
| Consequence, sensitivity, authority | `references/CONSEQUENCE-AUTHORITY.md` | Gates writes and external effects. |
| Evidence and provenance | `references/EVIDENCE-MODEL.md`, `references/AGREEMENT-LOOP.md` | Separates system facts, decisions, inference, gaps, testimony, and memory. |
| Skill behavior | `skills/core/<skill>/SKILL.md` | Canonical portable skill logic. |
| Platform capability mapping | `adapters/<platform>/overlay.yaml` | Platform-specific tool names and degradation. |
| CLI behavior | `tools/ws/` and live `ws ... --help` | The authoritative mutation implementation. |
| Runtime behavior | `runtime/` and its tests | Checkpointed graph implementation. |
| Architecture decisions | `docs/adr/` | Accepted hard-to-reverse decisions. |
| Current work state | `.work-studio/objects/`, `.work-studio/active.md` | Durable operational records. |

Generated adapters, installed skill copies, derived domain indexes, and static HTML views are outputs. Edit their canonical generators or sources, then regenerate. `[system: work-studio/kernel-manifest.yaml; WORKSPACE-DOCUMENTATION-CONTRACT.md]`

## 3. Repository map

```text
andrelawas-work-studio/
├── skills/core/                 Canonical portable skill definitions
├── references/                  Shared operating contracts and taxonomies
├── capabilities/                Reusable capability contracts
├── adapters/
│   ├── codex/                   Generated Codex skills, manifest, checksums
│   ├── claude-code/             Generated Claude Code skills
│   └── github-copilot/          Generated GitHub Copilot skills
├── tools/ws/                    Dependency-free deterministic state CLI
├── runtime/                     Optional LangGraph checkpointed runtime
├── mcp_server/                  Work Studio MCP package
├── work-studio/                 Kernel manifest and generated skill map
├── .work-studio/                Local operational state and deliverables
├── docs/adr/                    Architecture Decision Records
├── docs/design/                 Accepted plans and designs
├── docs/verification/           Verification evidence
├── fixtures/                    Behavioral/conformance fixtures
└── tests/                       CLI, protocol, runtime, and skill tests
```

## 4. Core operating model

### 4.1 Work Object identity

A Work Object ID has the form `YYYY-MM-DD-NNN`. Its file is stored at:

```text
.work-studio/objects/YYYY/MM/<id>-<slug>.md
```

Important frontmatter fields include `id`, `title`, `type`, `status`, `state`, `consequence`, `sensitivity`, `domain`, timestamps, and `next_action`. IDs and historical entries are not rewritten in place. `[system: references/WORK-OBJECT.md; tools/ws/schema.py]`

### 4.2 Types, states, and statuses

Work Object types are:

- `inquiry`
- `project`
- `change`
- `incident`

Lifecycle states are:

```text
notice → explore → design → build → verify → release → observe → close
```

States describe current reality; they are not mandatory ceremony. Status is independently one of `active`, `waiting`, `paused`, or `closed`. `[system: tools/ws --help; governance-conduct-work-object skill]`

### 4.3 Attention

`.work-studio/active.md` is an advisory attention register. Exactly one Work Object may be the current `primary` implementation/deployment focus; any number may be `supporting`; an object can also be `paused`. Attention does not change identity or lifecycle state. `[system: governance-conduct-work-object skill; tools/ws/lifecycle.py]`

### 4.4 Evidence and decisions

Evidence entries carry provenance, not truth scores. The canonical lanes are:

- `[system]` — code, configuration, tool output, or other system-observed fact
- `[decision]` — explicit human/accountable-owner decision
- `[inference]` — reasoned conclusion
- `[gap]` — unavailable or unresolved evidence
- `[testimony]` — attributable human observation
- `[memory]` — approved reusable context

Decisions belong in structured `### Decision N` blocks with result, scope, authorization, confidence, actor, revisit trigger, and rationale. History records what happened; it must not be used as a substitute for evidence or decision rationale. `[system: references/AGREEMENT-LOOP.md; references/EVIDENCE-MODEL.md]`

### 4.5 Consequence, sensitivity, and authority

Consequence is `low`, `meaningful`, or `high`. Sensitivity is `ordinary`, `private`, or `restricted`. Higher consequence and restricted content require narrower, explicit authority. External effects—deployment, communication, publication, money movement, production access, or sensitive-source access—are separately gated even if local analysis is allowed. `[system: references/CONSEQUENCE-AUTHORITY.md]`

### 4.6 Optimistic concurrency

Every mutating `ws` command except `init`, `create`, and the composite `start` requires the object’s current `updated_at` value through `--expect-updated`. A stale timestamp stops the write instead of silently overwriting another revision. `--force` exists on selected commands but bypasses a safety boundary and should be exceptional. `[system: live ws help; tools/ws/concurrency.py]`

## 5. End-to-end workflow

### 5.1 Start or resume work

1. From the target repository, locate `.work-studio/config.md` without scanning beyond the repository boundary.
2. Read `WORKSPACE-DOCUMENTATION-CONTRACT.md` to locate canonical artifacts.
3. Inspect `.work-studio/active.md` and recent Work Objects for a match.
4. Resume the matching object, or create/start a new one from explicit user intent.
5. Route substantive work to the skill matching the real lifecycle state.

Preferred one-command activation:

```powershell
python -m tools.ws start `
  --title "Describe the outcome" `
  --type project `
  --consequence low `
  --sensitivity ordinary `
  --domain engineering `
  --evidence "[decision] Director activated this work." `
  --role supporting `
  --next-action "Inspect the bounded implementation surface."
```

### 5.2 Explore and decide

- Record discriminating source evidence with `append-evidence`.
- Use the appropriate thinking/research skill for uncertainty.
- Put accepted choices in structured Decision blocks.
- Keep unresolved facts explicit as gaps.
- Update `next_action` so another session can continue without chat history.

### 5.3 Design and build

- Route an accepted design boundary to the relevant design skill.
- Implement only the bounded accepted change.
- Preserve unrelated dirty-worktree changes.
- Add typed relationships, artifact fingerprints, and claims where they improve traceability.

### 5.4 Verify, release, observe, close

- Verify against declared success evidence and recovery requirements.
- Release only with scoped authority and a rollback path.
- Observe expected versus actual outcomes.
- Close only when the close gate is satisfied, recording residual uncertainty and revisit triggers.

## 6. Installing and running the tooling

### 6.1 Prerequisites

- Adapter installer: PowerShell 5.1+ on Windows, or POSIX shell plus `sha256sum`/`shasum` on macOS/Linux.
- `ws` CLI: Python 3.9+; no runtime dependencies.
- Graph runtime and MCP package: Python 3.11+ managed by `uv`.

### 6.2 Reproduce the development environment

```powershell
uv sync --group test --group dev
```

Run the deterministic CLI from the repository without installing it:

```powershell
python -m tools.ws --help
```

Or use the workspace-installed console script after `uv sync`:

```powershell
uv run ws --help
```

Run runtime modules through `uv` so LangGraph and Pydantic are available:

```powershell
uv run python -m runtime.graph --help
uv run python -m runtime.business --help
```

Running `python -m runtime.graph` in an environment without synced dependencies fails at import time; this is expected dependency behavior, not a checkpoint failure. `[system: pyproject.toml; observed command result 2026-08-22]`

### 6.3 Install platform skills — Windows

```powershell
# Verify committed artifacts only
.\tools\install.ps1 -Platform codex -Verify

# Install globally
.\tools\install.ps1 -Platform codex -Global

# Pin to the current repository; project pin wins over global
.\tools\install.ps1 -Platform codex -Project -Dir .

# Show the effective installation
.\tools\install.ps1 -Platform codex -Resolve -Dir .

# Preview without writing
.\tools\install.ps1 -Platform codex -Project -Dir . -DryRun
```

Replace `codex` with `claude-code` or `github-copilot` as needed. `-Dest <path>` overrides the normal install destination.

### 6.4 Install platform skills — macOS/Linux

```sh
tools/install.sh --platform codex --verify
tools/install.sh --platform codex --global
tools/install.sh --platform codex --project .
tools/install.sh --platform codex --resolve .
tools/install.sh --platform codex --project . --dry-run
```

Default destinations:

| Platform | Global | Project pin |
|---|---|---|
| Codex | `~/.agents/skills/` | `.agents/skills/` |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| GitHub Copilot | `~/.copilot/skills/` | `.github/skills/` |

The installer verifies source checksums before copying and verifies the installed bytes afterward. Project selection is recorded in `.work-studio/adapter.<platform>.lock`. `[system: tools/install.ps1; tools/install.sh]`

## 7. `ws` CLI reference

General forms:

```powershell
python -m tools.ws <command> [options]
uv run ws <command> [options]
ws <command> [options]              # when installed on PATH
```

Always inspect exact options on the installed version:

```powershell
ws --help
ws <command> --help
ws <command> <subcommand> --help
```

### 7.1 Workspace and Work Object lifecycle

| Command | Purpose | Essential form |
|---|---|---|
| `ws init` | Bootstrap `.work-studio/` | `ws init --name <name>` |
| `ws create` | Allocate a Work Object in `notice` | `ws create --title <title> --type <type> --consequence <level> --sensitivity <class> [--domain <domain>]` |
| `ws start` | Composite create + first evidence + `explore` + attention registration | `ws start --title <title> --type <type> --consequence <level> --sensitivity <class> --evidence <text> [--role supporting] [--next-action <text>]` |
| `ws transition` | Change lifecycle state/status and append History | `ws transition <id> --state <state> --status <status> --expect-updated <timestamp> --action <text> --rationale <text> [--next-action <text>]` |
| `ws close` | Apply close gate and close an object | `ws close <id> --expect-updated <timestamp> --rationale <text>` |
| `ws activate` | Set attention role | `ws activate <id> --role primary|supporting|paused --expect-updated <timestamp>` |
| `ws attention` | Report active-register drift | `ws attention [--repair] [--default-role supporting]` |
| `ws members` | List objects sharing a campaign design anchor | `ws members docs/design/<campaign>.md` |
| `ws set-campaign` | Assign a campaign anchor | `ws set-campaign <id> docs/design/<campaign>.md --expect-updated <timestamp>` |

Allowed enum values:

```text
type:        change | inquiry | project | incident
consequence: low | meaningful | high
sensitivity: ordinary | private | restricted
state:       notice | explore | design | build | verify | release | observe | close
status:      active | waiting | paused | closed
domain:      business | architecture | asset | design | governance |
             engineering | research | ideation | operations
```

`--domain` is repeatable, with the primary discipline first.

### 7.2 Evidence, history, artifacts, and claims

```powershell
ws append-evidence <id> `
  --tag "[system]" `
  --source "tests/test_example.py" `
  --text "The bounded test passed." `
  --expect-updated <timestamp>

ws append-history <id> `
  --action "Recorded investigation outcome" `
  --state explore `
  --status active `
  --actor codex `
  --rationale "Primary-source inspection answered the question." `
  --next-action "Produce the report." `
  --expect-updated <timestamp>

ws append-artifact <id> `
  --path .work-studio/deliverables/<file>.md `
  --description "Standalone current-system reference" `
  --expect-updated <timestamp>
```

`append-artifact` computes and records a content fingerprint. `append-evidence --sha` accepts an optional commit SHA only for `[system]` evidence; `append-history --commit` records an optional commit reference. `[system: live ws help]`

Claims:

```powershell
ws claim register <id> `
  --text "Claim text" `
  --kind observation `
  --paths tools/ws/schema.py `
  --revisit-on "schema changes" `
  --expect-updated <timestamp>

ws claim inspect <id>
ws claim inspect <id> --state captured
```

Claim kinds are `observation`, `inference`, or `decision`. Inspection states include `captured`, `supported`, and `accepted_for_action`. Structured scope can include repeatable `--paths`, `--git-commit`, `--dirty-fingerprint`, and repeatable `--revisit-on`.

### 7.3 Relationships and graph trace

```powershell
ws relation add <id> `
  --type implements `
  --to <other-id> `
  --basis "Decision 2" `
  --expect-updated <timestamp>

ws graph trace <id>
ws graph trace <id> --direction downstream
```

Relationship types:

```text
responds_to, resulted_in, supersedes, depends_on, blocks, implements,
verifies, observes, revises, supports, counters, authorized_by,
generated_by, used, invalidates, hands_off_to
```

Targets may be Work Object IDs or explicit `external:<locator>` references.

### 7.4 Domain indexes

```powershell
ws domain sync
```

This regenerates `.work-studio/domain/<domain>.md` indexes from canonical Work Object frontmatter. The indexes are derived and should not be edited directly.

### 7.5 Engineering handoff

```powershell
ws engineering-handoff inspect <id> [--thread-id <thread>] [--checkpoint-db <db>]
ws engineering-handoff approve <id> [--thread-id <thread>] [--checkpoint-db <db>]
ws engineering-handoff reject  <id> [--thread-id <thread>] [--checkpoint-db <db>]
```

Default thread ID is the Work Object ID. Default checkpoint database is `runtime/checkpoints/tracer.sqlite`.

### 7.6 Epistemic, authority, baseline, and conflict controls

```powershell
# Lint provenance tags; default scans canonical sources
ws epistemic lint
ws epistemic lint "skills/core/**/*.md" --allowlist references/epistemic/lint-allowlist.yaml
ws epistemic lint --allowlist none

# Check whether an active, unexpired authority grant covers an action
ws authority check <id> --action "publish deliverable"

# Record/check the dirty-tree identity baseline
ws baseline capture
ws baseline check

# Register competing versions for a claim
ws conflict register <id> `
  --claim-id <claim-id> `
  --commit-sha <sha> `
  --file-path <path> `
  --dirty-hash <fingerprint> `
  --expect-updated <timestamp>

# Record accountable resolution
ws conflict resolve <id> `
  --conflict-id <conflict-id> `
  --resolver <owner> `
  --disposition superseded `
  --rationale <text> `
  --expect-updated <timestamp>
```

For multiple conflict versions, repeat the paired `--commit-sha`, `--file-path`, and `--dirty-hash` arguments.

### 7.7 Validation and generated operational views

```powershell
# All Work Objects and all checks
ws validate

# Selected checks
ws validate schema lifecycle claims

# Selected files
ws validate --files .work-studio/objects/2026/08/<file>.md

# Advisory outcome-review coverage
ws outcomes

# Regenerate static views
ws command-center
ws asset-workbench

# Rebuild generated skill index
ws skill-map build

# Show content inputs cited by an object
ws inputs <id>
```

Named validation checks currently include:

```text
schema, sections, append-only, next-action, sensitivity,
sensitivity-policy, lifecycle, claims, lanes, authority,
protected-fields, history-integrity, file-integrity, incident-routing,
prerequisites, dashboard-signals, contract-drift
```

Generated outputs:

- `ws command-center` → `.work-studio/command-center.html`
- `ws asset-workbench` → `.work-studio/asset-workbench.html`
- `ws skill-map build` → `work-studio/skill-map.yaml`

### 7.8 Design asset ingestion

```powershell
ws asset-ingest `
  --asset-id <id> `
  --asset-kind component-family `
  --work-object <work-object-id> `
  --summary <text> `
  --source-note <text> `
  --frontier identity
```

Asset kinds:

```text
foundation, token-set, theme, component-family, ux-pattern,
flow, projection, motion
```

The command creates one draft design-asset record from explicit local input. It does not make the record settled or canonical by itself.

### 7.9 Backup and restore

```powershell
ws backup
ws restore <timestamp>
```

`backup` copies `.work-studio/objects/` into a timestamped local backup. `restore` restores from the named timestamp printed by `backup`. Restore is destructive to the current object set; inspect the target backup and preserve current state before using it. `[system: live ws help; tools/ws/backup.py]`

## 8. Runtime graph CLI reference

The runtime is optional and dependency-bearing. Invoke it with `uv run` from the repository root:

```powershell
uv run python -m runtime.graph --help
```

Top-level commands:

| Command | Purpose |
|---|---|
| `run` | Run a fresh two-node checkpointed graph. |
| `inspect` | Inspect one thread’s latest checkpoint state. |
| `resume` | Resume without fresh input. |
| `fork` | Copy latest state into a sibling thread. |
| `backup` | Back up a checkpoint database. |
| `restore` | Restore a backup into an isolated path. |
| `run-phase6` | Run the two-branch/join engineering graph. |
| `inspect-phase6` | Inspect a Phase 6 thread. |
| `fork-phase6` | Fork a Phase 6 checkpoint thread. |
| `run-research` | Run the single-URL, approval-gated research graph. |
| `inspect-research` | Inspect a research thread. |
| `run-business-router` | Run the checkpointed business operating router. |
| `inspect-business-router` | Inspect a business-router thread. |

Discover the exact signature of any runtime command:

```powershell
uv run python -m runtime.graph run-phase6 --help
uv run python -m runtime.graph run-research --help
uv run python -m runtime.graph run-business-router --help
```

Business-router-only surface:

```powershell
uv run python -m runtime.business run-router --help
uv run python -m runtime.business inspect-router --help
```

Runtime operations use explicit thread IDs and SQLite checkpoint paths. Reuse the exact same resolved absolute database path across processes on Windows; mixing Git Bash `/tmp/...` translation with Python-resolved paths can point at different physical files. `[system: Work Object 2026-08-21-006 evidence]`

## 9. Adapter generation and maintenance commands

Canonical skills are edited under `skills/core/`. Do not edit generated adapter skills directly.

```powershell
# Generate adapters, manifests, and checksums
python tools/generate-adapters.py

# Detect drift without rewriting
python tools/generate-adapters.py --check

# Rebuild the generated skill map
python -m tools.ws skill-map build

# Verify platform artifacts
.\tools\install.ps1 -Platform codex -Verify
```

Cross-platform equivalents use `python3` and `tools/install.sh`.

Other maintainer tools:

```powershell
python tools/verify-conformance.py --all
python tools/verify-kernel.py
python tools/verify-append-only.py
python tools/prompt_payload_tracer.py trace --root . --scenario capture
python tools/prompt_payload_tracer.py package --root . --scenario capture --output <path>
python tools/repair-evidence-ledgers.py --help
```

`tools/generate-adapters.py` does not implement a conventional `--help`; invoking it without `--check` performs generation. `[system: observed command behavior 2026-08-22]`

## 10. Verification workflow

Proportionate fast checks:

```powershell
python tools/generate-adapters.py --check
python -m tools.ws validate
uv run python -m pytest tests/test_ws_cli.py
```

Repository-wide gates:

```powershell
python tools/generate-adapters.py --check
python -m tools.ws validate
python tools/verify-conformance.py --all
python tools/verify-kernel.py
uv run python -m pytest tests/
uv run python -m pytest runtime/tests/
```

Shell wrappers:

```powershell
.\tests\run.ps1
```

```sh
sh tests/run.sh
```

As inspected on 2026-08-22, `tools/verify-kernel.py` reports three current path-declaration gaps: `design-audit-accessibility`, `design-critique-usability`, and `design-govern-interaction-motion` exist under `skills/core/` but are not yet listed in `work-studio/kernel-manifest.yaml`. This report does not silently treat that gate as passing. `[system: observed verification output 2026-08-22]`

## 11. Common operational recipes

### Resume an existing object safely

```powershell
Get-Content .work-studio/active.md
Get-Content .work-studio/objects/2026/08/<id>-<slug>.md
python -m tools.ws inputs <id>
python -m tools.ws graph trace <id>
```

Read the current `updated_at` before any write.

### Add evidence and move the next action without changing state

```powershell
ws append-evidence <id> --tag "[system]" --source <source> --text <text> --expect-updated <timestamp>

# Re-read updated_at after the first mutation
ws append-history <id> --action <action> --state explore --status active --actor codex --rationale <reason> --next-action <next> --expect-updated <new-timestamp>
```

### Link a completed artifact

```powershell
ws append-artifact <id> --path .work-studio/deliverables/<file>.md --description <description> --expect-updated <timestamp>
```

### Diagnose state drift

```powershell
ws attention
ws baseline check
ws validate
python tools/generate-adapters.py --check
```

### Generate local dashboards

```powershell
ws command-center
ws asset-workbench
```

Then open:

- `.work-studio/command-center.html`
- `.work-studio/asset-workbench.html`

## 12. Safety rules and common pitfalls

- Never hand-edit Evidence Ledger rows or History entries; use the CLI append commands.
- Never edit generated adapters, the skill map, domain indexes, or generated HTML as canonical sources.
- Never reuse a stale `updated_at`; re-read after every object mutation.
- Never treat `--force` as normal conflict resolution.
- Never change a Work Object’s immutable identity to represent a new direction; link a successor.
- Never promote inference or remembered context to `[system]` evidence.
- Never assume local analysis authorizes deployment, publication, outreach, money movement, production access, or restricted-data use.
- Never run runtime modules outside their synced `uv` environment and interpret an import failure as workflow failure.
- On Windows, use one explicit absolute SQLite checkpoint path consistently across shells and processes.
- Preserve unrelated dirty-worktree changes; the Work Object and baseline systems exist partly to make that boundary visible.

## 13. Investigation outcomes and provenance

| Sub-question | Outcome | Evidence used |
|---|---|---|
| What is the implemented system and its architecture? | `answered` | `README.md`, `pyproject.toml`, `work-studio/kernel-manifest.yaml`, repository tree. |
| What is the operating workflow and governance model? | `answered` | `WORKSPACE-DOCUMENTATION-CONTRACT.md`, Work Object and authority/evidence references, conductor skill, CLI schema. |
| What CLI commands exist and what do they do? | `answered` | Live `python -m tools.ws ... --help`, nested subcommand help, `tools/ws/__main__.py`. |
| How is the system installed, verified, run, and recovered? | `answered with disclosed gaps` | Install scripts, root/tool pyprojects, live `uv run` help, verification output, backup implementation. |

### Supersession resolved

- Older documentation that lists fewer skills or omits newer CLI surfaces was not used as the complete command inventory; live parser help and current source take precedence. `[inference]`
- The README’s broad verification guidance was retained, but current kernel verification failure was added so the reference does not imply a presently clean gate. `[system + inference]`
- Plain-Python runtime invocation was narrowed to `uv run` because the current unsynced interpreter lacks `langgraph`. `[system]`

### Known gaps

- The kernel manifest currently omits three implemented design skills named in Section 10.
- The repository has substantial concurrent uncommitted work; this report describes the observed working tree, not necessarily the last commit.
- CLI signatures can evolve. Use the live `--help` commands as the final authority for an installed version.

