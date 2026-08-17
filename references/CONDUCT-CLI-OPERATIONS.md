# Conduct Work Object — CLI Operations

Exact `python3 -m tools.ws` invocations for `skills/core/governance-conduct-work-object/SKILL.md`.
Relocated verbatim (WO `2026-08-15-007` Decision 2) from that skill's `## Stage
workflow` — the deterministic CLI syntax lives here; the decision logic for
*when* to use each command stays in `SKILL.md`.

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
