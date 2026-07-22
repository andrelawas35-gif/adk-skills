# Deterministic CLI Component Plan

**Date:** 2026-07-21
**Source:** Grilling Session 9 (Decisions 63–70)
**Status:** Accepted — not yet executed
**Prior session:** Session 8 (Authority and Sensitivity) — see `docs/design/authority-sensitivity-component-plan.md`
**Evidence trail:** `docs/design/grilling-session-9-deterministic-cli.md`

---

## 1. Current-State Findings

### Mutation landscape

Every mutation to `.work-studio/` state is performed by agents reading prose instructions in `skills/core/*/SKILL.md` and `references/*.md`, then calling Write/Edit tools to modify Markdown files directly. No intermediary program exists for any integrity-critical operation.

### Existing deterministic tools

| Tool | Language | What it does |
|------|----------|--------------|
| `tools/generate-adapters.py` | Python 3, stdlib-only | Generate adapter SKILL.md from core + overlay. Byte-for-byte reproducible. |
| `tools/verify-conformance.py` | Python 3, stdlib-only | Verify behavioral matrix + adapter structure. |
| `tools/verify-append-only.py` | Python 3, stdlib-only + git | Verify History/Decisions/Evidence sections are append-only. |
| `tools/install.sh` | POSIX sh | Install checksummed adapters. |
| `tools/prompt_payload_tracer.py` | Python 3, stdlib-only | Analyze prompt payloads (read-only). |

All tools are dependency-free. Zero external packages.

### Integrity gaps

| Operation | Risk | Current protection |
|-----------|------|-------------------|
| Allocate immutable ID | Duplicate/out-of-sequence IDs; unrecoverable | None — agent scans directory, picks next number |
| Apply lifecycle transition | Invalid transitions (close-state escape, closed-status resurrection) | None — ADR 0015 defines rules, nothing enforces them |
| Update `updated_at` / optimistic concurrency | Stale-write overwrite between conductor and specialist | Described in `WORK-OBJECT.md:69-71`, not implemented |
| Set consequence level | Systematic under-assignment (18/20 meaningful, 0/20 high) | None — Decision 58 designed three-question prompt, not built |
| Set sensitivity | Restricted content written to body instead of pointer | None — ADR 0019 promises CLI enforcement |
| YAML frontmatter schema | Invalid enum values, missing required fields | None |
| Body section structure | Misspelled headings, missing required sections | Partial — `verify-append-only.py` checks 3 headings |
| Attention register consistency | `active.md` lists closed objects, misses active ones | None |

---

## 2. Contradictions and Risks

| # | Finding | Evidence |
|---|---------|----------|
| 1 | `WORK-OBJECT.md:34` says "Flexible movement" for state; ADR 0015 adds two terminal prohibitions | CLI encodes ADR 0015's rules |
| 2 | ADR 0015 gates check structured Decisions fields; real Work Objects use free text | Gates are currently uncheckable; Decision 65 addresses via grandfathering |
| 3 | Optimistic concurrency described but never implemented | `WORK-OBJECT.md:69-71`; every intra-session concurrent write silently overwrites |
| 4 | ADR 0019 promises CLI-level sensitivity enforcement that does not exist | `0019:105-107` |
| 5 | Session 8 designed a five-check pre-commit hook (Decision 55) that has not been built | Hook becomes a consumer of `ws validate` |

---

## 3. Accepted Decisions

| # | Decision | Key constraint |
|---|----------|---------------|
| 63 | Tier A/B split: CLI owns structural operations end-to-end; validates agent-supplied content for append operations | Tier A: agent never touches `.work-studio/` files directly for these operations |
| 64 | Python 3 stdlib-only package at `tools/ws/` with `__main__.py` | No external dependencies; continues established pattern |
| 65 | Gate enforcement against structured fields, with grandfathering for legacy objects | `ws create` generates structured Decisions template |
| 66 | Composed validation checks: `schema`, `sections`, `append-only`, `attention`, `sensitivity`, `lifecycle`, `structure` | `ws validate` with no args runs all; named checks invocable individually |
| 67 | Required `--expect-updated` on every mutation of existing files | `ws create` exempt; `--force` exists for recovery with warning |
| 68 | Structured argument flags for Tier B content; CLI assembles Markdown | Agent never constructs Markdown for protected sections |
| 69 | File-path arguments for targeted validation | Workspace-wide checks ignore file paths |
| 70 | Minimum 7 sections in creation template + structured Decisions template | Optional sections added when needed |

---

## 4. Target Component Boundary

### What the CLI owns

The CLI (`tools/ws`) is the sole write path for `.work-studio/` state files. Agents call it as an external tool. The CLI:

- **Creates** Work Objects with validated frontmatter and correct body template
- **Allocates** immutable IDs with collision detection
- **Enforces** lifecycle transition rules (2 prohibitions, 5 gates)
- **Enforces** optimistic concurrency via `--expect-updated`
- **Validates** frontmatter schema, section structure, append-only invariants, attention register consistency, sensitivity rules
- **Assembles** Markdown entries for append operations from structured flags

### What the CLI does not own

- Semantic content: the agent decides what to write (evidence text, rationale, intent)
- Provenance tag accuracy: the agent chooses `[observed]` vs `[inferred]`; the CLI validates the tag is an allowed value but not whether it's correct
- Consequence judgment: the agent supplies `--consequence`; the CLI validates it's a valid enum but not whether the assessment is accurate
- Adapter generation and installation: remains with existing tools
- Skill prose instructions: the CLI enforces structural invariants, skills govern agent behavior

---

## 5. Recommended Architecture

### Package structure

```
tools/ws/
  __init__.py          # version, shared constants
  __main__.py          # argparse dispatch to subcommands
  schema.py            # YAML frontmatter parse, validate, write
  sections.py          # Markdown body section parse, append, validate
  lifecycle.py         # 8-state transition graph, 5 prerequisite gates
  concurrency.py       # updated_at read-compare-reject
  identity.py          # ID allocation with collision detection
  attention.py         # active.md read, consistency check, update
  validate.py          # composed validation checks
  template.py          # Work Object body template generation
tools/ws               # thin executable wrapper (#!/usr/bin/env python3)
```

### Command surface (8 commands)

| Command | Tier | Arguments | What it does |
|---------|------|-----------|--------------|
| `ws init` | A | `--name <workspace-name>` | Create `.work-studio/config.md`, `active.md`, `inbox.md`, `objects/`. Idempotent — refuses to overwrite existing workspace. |
| `ws create` | A | `--title <title> --type <type> --consequence <level> --sensitivity <class>` | Allocate ID, generate YAML frontmatter, write body template with 7 required sections + structured Decisions template. `--consequence` required, no default. Prints created file path and ID. |
| `ws transition` | A | `<id> --state <state> [--status <status>] --expect-updated <ts> --action <text> --rationale <text>` | Validate transition against lifecycle graph, check prerequisite gates, write new state/status + updated_at, append History entry. |
| `ws close` | A | `<id> --expect-updated <ts> --rationale <text>` | Consequence-scaled closure. Low/meaningful: set `status: closed` from any state. High: requires routing through `state: close` first. Append History. |
| `ws activate` | A | `<id> --role <primary\|supporting\|paused> --expect-updated <ts>` | Update `active.md` entry. Cross-check: object must exist, status must not be `closed`. |
| `ws validate` | — | `[check-names...] [file-paths...]` | Run named checks. No args = all checks, full workspace. With file paths = validate only those files. Exit nonzero on failure. |
| `ws append-evidence` | B | `<id> --tag <tag> --text <text> --source <source> --expect-updated <ts>` | Validate tag is allowed value, validate timestamp format, append to Evidence ledger section, update `updated_at`. |
| `ws append-history` | B | `<id> --action <text> --state <state> --status <status> --actor <actor> --rationale <text> --expect-updated <ts>` | Validate fields, append to History section, update `updated_at`. |

### Entry point

```
python3 -m tools.ws <command> [args...]
```

This is the canonical entry point. A wrapper script at `tools/ws` was
planned (step 16) but skipped: the `tools/ws/` Python package directory
occupies that path, creating a filesystem collision. The `python3 -m`
invocation is equivalent and is used in all skills, adapters, and the
pre-commit hook.

### Optimistic concurrency

Every write command (except `ws create` and `ws init`):
1. Reads the target file
2. Extracts `updated_at` from YAML frontmatter
3. Compares against `--expect-updated` argument
4. If mismatch: prints error with both timestamps, exits 1
5. If match: performs the write, sets `updated_at` to current time

`--force` bypasses the comparison with a stderr warning.

### Lifecycle enforcement

```
Allowed: any state → any state (permissive default)
Prohibited: close → any other state
Prohibited: closed status → any other status

Gates (check ## Decisions and revisit triggers):
  build gate (high consequence only):   requires type: decision record
  release gate (all consequence levels): requires result: pass + scope field
  close gate (all consequence levels):   requires outcome record
  observe gate (all consequence levels): requires result: pass (deployment/recovery)
```

### Pre-commit hook integration

The pre-commit hook (Session 8 Decision 55) is a thin shell script that calls `ws validate`:

```sh
#!/bin/sh
# Installed by: tools/ws hook install
staged=$(git diff --cached --name-only -- '.work-studio/**')
[ -z "$staged" ] && exit 0
echo "$staged" | xargs tools/ws validate schema append-only sensitivity lifecycle
```

Plus two git-specific checks not in the CLI:
1. Warn if `.work-studio/objects/` files are staged
2. Check constitutional files against a declared protected list

---

## 6. Migration Steps

| # | Step | What changes | Depends on |
|---|------|-------------|------------|
| 1 | Create `tools/ws/` package structure with `__init__.py`, `__main__.py` | New directory, new files | — |
| 2 | Implement `schema.py`: YAML frontmatter parser (reuse `generate-adapters.py:72-151` pattern), validator (enum membership, required fields, immutable field checks) | New module | Step 1 |
| 3 | Implement `identity.py`: ID allocation with collision detection (scan `objects/YYYY/MM/`, derive next NNN, verify no existing file) | New module | Step 1 |
| 4 | Implement `template.py`: body template generation (7 required sections + structured Decisions template) | New module | Step 1 |
| 5 | Implement `ws create` command: wire schema + identity + template, write file to correct path, print ID | New command in `__main__.py` | Steps 2, 3, 4 |
| 6 | Implement `concurrency.py`: `updated_at` read-compare-reject | New module | Step 2 |
| 7 | Implement `sections.py`: body section parser (extract sections by heading, append to section, validate section order) | New module | Step 1 |
| 8 | Implement `lifecycle.py`: transition graph (2 prohibitions), 5 prerequisite gates (read Decisions section, check structural fields) | New module | Step 7 |
| 9 | Implement `ws transition` and `ws close` commands | New commands | Steps 6, 7, 8 |
| 10 | Implement `ws append-evidence` and `ws append-history` commands | New commands | Steps 6, 7 |
| 11 | Implement `attention.py`: `active.md` parser, consistency checker, updater | New module | Step 2 |
| 12 | Implement `ws activate` command | New command | Steps 6, 11 |
| 13 | Implement `validate.py`: composed checks (`schema`, `sections`, `append-only`, `attention`, `sensitivity`, `lifecycle`, `structure`) | New module; subsumes `verify-append-only.py` and partially `verify-conformance.py` | Steps 2, 7, 8, 11 |
| 14 | Implement `ws validate` command | New command | Step 13 |
| 15 | Implement `ws init` command | New command | Step 4 |
| 16 | Create wrapper script `tools/ws` | Skipped — filesystem collision with `tools/ws/` package directory. `python3 -m tools.ws` is canonical entry point. | Step 5 |
| 17 | Add pre-commit hook installer (`ws hook install` or standalone script) | New functionality | Step 14 |
| 18 | Deprecate `tools/verify-append-only.py` — replace body with call to `ws validate append-only` | Modified file | Step 14 |
| 19 | Update `references/WORK-OBJECT.md` — remove "Flexible movement" imprecision, reference ADR 0015 for lifecycle rules, document CLI as write path | Modified file | Step 9 |
| 20 | Update ADR 0019 — change "Planned enforcement" to reference `ws` commands | Modified file | Step 10 |
| 21 | Update skill SKILL.md files — add CLI invocation instructions at mutation points, regenerate adapters | Modified files | Steps 5, 9, 10, 12 |

---

## 7. Tests and Evidence Required

| Test | What it proves | Fixture |
|------|---------------|---------|
| `test_create_allocates_unique_id` | No ID collision across sequential creates on same date | Empty `objects/YYYY/MM/` dir |
| `test_create_rejects_invalid_consequence` | Enum validation works | Bad `--consequence` value |
| `test_create_rejects_invalid_type` | Enum validation works | Bad `--type` value |
| `test_create_generates_correct_template` | Body has 7 required sections + structured Decisions template | Created file content |
| `test_transition_rejects_close_escape` | Terminal-state prohibition enforced | Object with `state: close` |
| `test_transition_rejects_closed_status_resurrection` | Terminal-status prohibition enforced | Object with `status: closed` |
| `test_transition_gate_blocks_without_evidence` | Prerequisite gate produces clear error | Object missing required Decisions fields |
| `test_transition_gate_passes_with_evidence` | Gate checks structural fields correctly | Object with required Decisions fields |
| `test_expect_updated_rejects_stale` | Optimistic concurrency works | Object modified between read and write |
| `test_expect_updated_accepts_current` | Non-stale writes succeed | Object not modified |
| `test_force_bypasses_staleness_with_warning` | Recovery path works but warns | Modified object + `--force` |
| `test_append_evidence_validates_tag` | Tag enum enforced | Bad `--tag` value |
| `test_append_evidence_preserves_prefix` | Append-only invariant maintained | Existing evidence entries |
| `test_append_history_validates_state` | State enum enforced in History | Bad `--state` value |
| `test_validate_schema_catches_invalid_enum` | Schema check works on bad frontmatter | Object with invalid `status` |
| `test_validate_append_only_catches_deletion` | Subsumes `verify-append-only.py` | Object with deleted History entry |
| `test_validate_attention_catches_stale_entry` | Cross-check works | `active.md` listing closed object |
| `test_validate_sensitivity_catches_restricted_body` | Sensitivity enforcement works | Object with restricted content |
| `test_validate_lifecycle_catches_terminal_escape` | Lifecycle check works | Object with invalid transition |
| `test_init_is_idempotent` | Won't overwrite existing workspace | Existing `.work-studio/config.md` |
| `test_close_consequence_scaled` | Low/meaningful close from any state; high requires close-routing | Objects at each consequence level |
| `test_grandfathered_legacy_object` | Gate produces "not yet satisfiable" message, not failure | Legacy object without structured Decisions |

---

## 8. Deferred Decisions

| Topic | Why deferred | Revisit trigger |
|-------|-------------|-----------------|
| `ws register-component` command | Lower frequency, lower risk than core CRUD operations | When component ledger mutations cause real integrity issues |
| `ws status` / `ws list` read-only commands | Convenience, not integrity-critical | When agents frequently fail to find or parse Work Objects |
| Promote working method via CLI | Not yet designed (no grilling session) | When working-method promotion produces data corruption |
| Schema migration command | No schema version changes planned | When `schema_version` increments |
| Structured authority History entries in `ws transition` | Decision 54 (Session 8) designed the format; CLI can enforce it | When implementing Session 8 component plan step 3 |
| Consequence re-evaluation prompt | CLI could prompt when effects escalate beyond declared level | When a real under-assignment causes harm |
| Adapter generation integration | `generate-adapters.py` remains standalone | When CLI is stable enough to absorb it |

---

## 9. Smallest Tracer Bullet

**Command:** `ws create`

**What it proves:**
- ID allocation with collision detection works
- YAML frontmatter generation with enum validation works
- Body template assembly with 7 required sections + structured Decisions template works
- File write to correct path (`objects/YYYY/MM/<id>-<slug>.md`) works
- `--consequence` is required with no default (enforces Decision 58)
- The `tools/ws/` package structure, import path, and wrapper script all work end-to-end

**Why this command first:**
- It's the natural first command in any workflow — you can't transition, validate, or append to an object that doesn't exist
- It exercises the highest-corruption-risk operation (ID allocation)
- It immediately delivers consequence enforcement (Session 8 Decision 58)
- It proves the delivery path without depending on lifecycle, gates, or concurrency modules

**Tracer bullet scope:**
1. `tools/ws/__init__.py` — version constant
2. `tools/ws/__main__.py` — argparse dispatch with `create` subcommand
3. `tools/ws/schema.py` — YAML frontmatter generator and validator
4. `tools/ws/identity.py` — ID allocator
5. `tools/ws/template.py` — body template
6. `tools/ws` — wrapper script
7. `tests/test_ws_create.py` — the 4 creation tests from §7

**Expected invocation:**
```sh
tools/ws create \
  --title "Fix auth middleware" \
  --type change \
  --consequence meaningful \
  --sensitivity ordinary
```

**Expected output:**
```
Created: .work-studio/objects/2026/07/2026-07-21-010-fix-auth-middleware.md
ID: 2026-07-21-010
```

**Reversibility:** The tracer bullet creates one file. `rm` removes it. Zero blast radius.
