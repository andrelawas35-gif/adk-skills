# Conduct Work Object — CLI Operations

Exact `python3 -m tools.ws` invocations for `skills/core/governance-conduct-work-object/SKILL.md`.
Relocated verbatim (WO `2026-08-15-007` Decision 2) from that skill's `## Stage
workflow` — the deterministic CLI syntax lives here; the decision logic for
*when* to use each command stays in `SKILL.md`.

**Two equivalent invocation forms** (WO `2026-08-21-003`): `python3 -m
tools.ws <command>` when run from inside this repository (or any checkout
that vendors `tools/ws`), or the packaged console script `ws <command>` when
`tools/ws` has been installed as `work-studio-ws` (`pip install -e ./tools`
from this repo, or `uv sync` in a workspace that declares it — see root
`pyproject.toml`). The installed `ws` resolves its target workspace the same
way either form does: it walks upward from the current working directory for
`.work-studio/`. This is what makes the CLI usable from a target repo that
does not, and never needs to, vendor a copy of `tools/ws` itself. Both forms
are interchangeable below; examples use `python3 -m tools.ws`.

## Critical: Always read `updated_at` before mutating

**Before running ANY mutating command** (transition, close, activate,
append-history, append-evidence, append-artifact, etc.), you MUST first
read the current `updated_at` timestamp:

```sh
UPDATED_AT=$(python3 -m tools.ws get-updated-at <id>)
```

Then use that exact value in `--expect-updated`. Never estimate, guess, or
reuse a stale timestamp. The CLI uses optimistic concurrency control and
will reject writes with mismatched timestamps.

## Bootstrap workspace (Stage workflow, step 1)

**Only after the workspace-discovery search in `SKILL.md` step 1 finds no
`.work-studio/` anywhere between the current directory and the repository
root or filesystem boundary, and after the user has confirmed they want one
created.** This is a Missing Artifact Gap (`references/MISSING-ARTIFACT-GAP.md`)
until that confirmation is given — do not run `init` speculatively, and never
hand-write `.work-studio/config.md`, `active.md`, or `inbox.md` directly; the
CLI is the only sanctioned writer, exactly as for every other mutation this
skill performs.

**Confirm the CLI is reachable** before proposing bootstrap. Try `ws
--version` (or `python3 -m tools.ws --version` from inside a checkout of this
repository, e.g. `andrelawas-work-studio/`, if one is locatable). If neither
resolves, this is a capability gap, not a blocker to solve by hand: report it
per `## Failure and degradation behavior` in `SKILL.md` and give the one
manual instruction (install via `pip install -e <path-to-andrelawas-work-studio>/tools`,
or `uv sync` from that repo if it declares the workspace) rather than
fabricating workspace files.

**Bootstrap, once the CLI is confirmed reachable and the user has confirmed:**

```sh
python3 -m tools.ws init --name "<workspace-name>"
```

Run from the target project's root — the directory that should own
`.work-studio/` (typically the repository root, i.e. the directory containing
`.git`). The command is idempotent: if `.work-studio/config.md` already
exists, it reports that and makes no change, so it is safe to re-run rather
than re-checking by hand. It creates `.work-studio/`, `.work-studio/objects/`,
`config.md`, an empty `active.md`, and an empty `inbox.md` — nothing else.
`config.md` records `workspace_name`, `created_at`, and `cli_version`; no
frontmatter schema applies to it. This step alone does not create
`WORKSPACE-DOCUMENTATION-CONTRACT.md` — that remains a separate Missing
Artifact Gap with its own bootstrap authority, per `references/MISSING-ARTIFACT-GAP.md`,
since it registers artifact types and ownership beyond what a bare workspace
needs.

Report the created path and proceed to `## Detect or create` (Stage workflow,
step 2) as if the workspace had already existed — do not create a first Work
Object as part of bootstrap unless the user's original request already
supplies the signal or intent for one.

## Create Work Object (Stage workflow, step 4)

**Create:**

```sh
python3 -m tools.ws create \
  --title "<human-readable-title>" \
  --type <type> \
  --consequence <consequence> \
  --sensitivity <sensitivity>
```

The CLI handles: immutable ID allocation with collision detection, YAML
frontmatter generation with validated enums, body template with 7 required
sections plus structured Decisions template, file write to the correct
`objects/YYYY/MM/<id>-<slug>.md` path. It prints the created file path and
allocated ID.

**Append the creation History entry:**

```sh
python3 -m tools.ws append-history <id> \
  --action "Created" \
  --state notice \
  --status active \
  --actor "<platform>" \
  --rationale "<creation rationale>" \
  --expect-updated <updated_at>
```

**Update `active.md` if this is the first active object or the user confirms it as Primary:**

```sh
python3 -m tools.ws activate <id> \
  --role primary \
  --expect-updated <updated_at>
```

## Update Work Object (Stage workflow, step 5)

**IMPORTANT: Before ANY mutating command, read the current timestamp first:**

```sh
UPDATED_AT=$(python3 -m tools.ws get-updated-at <id>)
```

Then use `$UPDATED_AT` in the `--expect-updated` parameter. Never estimate or guess.

**State/status transitions:**

```sh
python3 -m tools.ws transition <id> \
  --state <target-state> \
  --status <target-status> \
  --expect-updated <current-updated_at> \
  --action "<description>" \
  --actor "<platform>" \
  --rationale "<reason>"
```

**Closing a Work Object:**

```sh
python3 -m tools.ws close <id> \
  --expect-updated <current-updated_at> \
  --rationale "<reason>"
```

**Appending History (without state change):**

```sh
python3 -m tools.ws append-history <id> \
  --action "<description>" \
  --state <current-state> \
  --status <current-status> \
  --actor "<platform>" \
  --rationale "<reason>" \
  --expect-updated <current-updated_at>
```

**Appending Evidence:**

```sh
python3 -m tools.ws append-evidence <id> \
  --tag "[system]|[decision]|[inference]|[gap]|[testimony]|[memory]" \
  --source "<source>" \
  --text "<entry>" \
  --expect-updated <current-updated_at>
```

## Manage attention (Stage workflow, step 7)

```sh
python3 -m tools.ws activate <id> \
  --role primary|supporting|paused \
  --expect-updated <current-updated_at>
```

The CLI cross-checks that the object exists and is not closed before
updating `active.md`.

## Get current updated_at (concurrency helper)

**Before any mutating command**, read the current `updated_at` value:

```sh
python3 -m tools.ws get-updated-at <id>
```

This prints the current `updated_at` timestamp to stdout. Use it in
subsequent commands:

```sh
# 1. Get current timestamp
UPDATED_AT=$(python3 -m tools.ws get-updated-at <id>)

# 2. Use it in a mutating command
python3 -m tools.ws append-history <id> \
  --action "..." \
  --state <state> \
  --status <status> \
  --expect-updated "$UPDATED_AT" \
  ...
```

**Why this matters:** The CLI uses optimistic concurrency control. Every
mutating command (except `create` and `init`) requires `--expect-updated`
to match the file's current `updated_at`. If you pass a stale value, the
CLI rejects the write with a "Concurrent write detected" error. Always
read the current value immediately before the mutating command.
