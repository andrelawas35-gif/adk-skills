# Command/Result File Schema + Command-ID Scheme — Bounded Blender Operator (COMP-042)

> WO `2026-08-24-014` Decision 2 (2026-08-25T02:30:00Z). Transport: crash-durable
> file-based command queue. This document is the accepted schema + command-ID
> scheme. It is the single source of truth for the queue contract; the add-on
> (`addon.py`) and the pure-Python queue logic (`queue.py`) implement it.

## Queue directories

- `queue_dir/` — caller drops **command files** here (`CMD-<id>.json`).
- Result files (`result-<id>.json`) are written **into the same directory**,
  keyed by the same command ID. Command files are never deleted by the add-on;
  the presence of a matching result file is the durable acknowledgement (ack).
- Default location: `<repo>/runtime/blender_queue/` (outside `.work-studio/`,
  which is reserved for Work Objects). Configurable via the `QUEUE_DIR`
  environment variable or the add-on's `queue_dir` preference.

## Command-ID scheme (stable, reserved)

```
CMD-<nonce8>-<seq4>
```

- `<nonce8>` — 8 lowercase hex chars from the caller's choice (timestamp- or
  random-based) so multiple callers can write without collision.
- `<seq4>` — zero-padded 4-digit sequence within that caller (0001, 0002, …).
- The same ID names the command file (`CMD-<id>.json`) and the result file
  (`result-<id>.json`).
- **Reserved for a future socket layer**: the ID scheme is the stable key a
  socket-based notification layer will reuse for live caller notification,
  without any queue redesign. The queue itself remains file-based and
  authoritative; a socket layer would be a non-authoritative enhancement only.

## Command file — `CMD-<id>.json`

```json
{
  "schema_version": 1,
  "command_id": "CMD-a1b2c3d4-0001",
  "op": "scene.get_objects",
  "params": {},
  "created_at": "2026-08-25T02:30:00Z",
  "delay_ms": 0
}
```

| Field | Type | Required | Meaning |
|-------|------|----------|---------|
| `schema_version` | int | yes | Queue schema version (currently 1). |
| `command_id` | string | yes | `CMD-<nonce8>-<seq4>`; keys the result file. |
| `op` | string | yes | Bounded operation name from the §4.2 tool surface (e.g. `scene.get_objects`). Unknown `op` → `status: "error"`, `error.code: "unknown_op"`. |
| `params` | object | yes | Operation-specific arguments (may be `{}`). |
| `created_at` | string | yes | ISO-8601 UTC timestamp of command creation. |
| `delay_ms` | int | no | Test seam only: sleep this long before executing, giving the tracer a controllable mid-command crash window. Default 0. Not part of the production tool surface. |

## Result file — `result-<id>.json`

```json
{
  "schema_version": 1,
  "command_id": "CMD-a1b2c3d4-0001",
  "status": "ok",
  "data": {"objects": ["Cube", "Camera"]},
  "error": null,
  "started_at": "2026-08-25T02:30:01Z",
  "completed_at": "2026-08-25T02:30:01Z"
}
```

| Field | Type | Meaning |
|-------|------|---------|
| `schema_version` | int | 1. |
| `command_id` | string | Echoes the command file's ID. |
| `status` | string | `"ok"` on success, `"error"` on failure. |
| `data` | any | Operation result on success; `null` otherwise. |
| `error` | object\|null | `{code, message}` on failure, else `null`. |
| `started_at` / `completed_at` | string | ISO-8601 UTC execution window. |

## Crash-durability semantics (the riskiest assumption)

- A command is durable the moment `CMD-<id>.json` is on disk (before any
  execution).
- The add-on writes the result file **atomically** (temp file + rename), so a
  partial result file is never observed.
- If Blender crashes mid-command (the TDR failure mode in WO `2026-08-23-002`),
  no result file exists for that ID; on restart the add-on **replays** the
  pending command from the still-present command file.
- Read-only commands (like `scene.get_objects`) are replay-safe by nature: a
  duplicate replay is harmless, which is why the tracer uses a read-only
  command to isolate the durability question from write-idempotency.

## Bounded tool surface (accepted §4.2; only read-only ops in the tracer)

```
scene.get_objects          object.get / set_transform / duplicate / delete
camera.get / set / lock    light.get / set        render.preview / final
rig.get_pose               rig.set_bone_rotation
animation.get_keyframes    animation.move_keyframe / set_interpolation
mesh.* (V3+, asset cleanup)   material.get / set / assign
image.import_as_plane      image.set_as_reference
execute_blender_python()   — escalation path, requires explicit director
                             authority (high-consequence gate); NOT in the
                             bounded queue surface.
```

## Rollback

Delete the queue directory and the add-on script; all local, no durable state
(Director Console constraint: file-first, no hosted dependency).
