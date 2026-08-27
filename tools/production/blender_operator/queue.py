"""Pure-Python queue logic for the bounded Blender operator (COMP-042).

Implements the crash-durable file-based command queue contract documented in
``queue_schema.md`` (WO 2026-08-24-014 Decision 2). Deliberately has NO bpy
dependency so the schema, ID scheme, and replay semantics are unit-testable
without a live Blender process.

The add-on (``addon.py``) wires an ``execute(op, params)`` callable into this
logic. For tests, a fake executor can stand in for Blender.
"""

from __future__ import annotations

import json
import re
import tempfile
import time
import uuid
from pathlib import Path
from typing import Callable, Optional

SCHEMA_VERSION = 1

# Canonical command/result file name templates.
CMD_PREFIX = "CMD-"
RESULT_PREFIX = "result-"
CMD_GLOB = f"{CMD_PREFIX}*.json"
RESULT_GLOB = f"{RESULT_PREFIX}*.json"

# Stable, reserved command-ID scheme: CMD-<nonce8>-<seq4>.
_CMD_ID_RE = re.compile(rf"^{re.escape(CMD_PREFIX)}[0-9a-f]{{8}}-[0-9]{{4}}$")


def make_command_id(nonce: Optional[str] = None, seq: int = 1) -> str:
    """Build a reserved command ID ``CMD-<nonce8>-<seq4>``.

    ``nonce`` defaults to 8 hex chars derived from a uuid4; callers may pass
    their own. ``seq`` must be 1..9999 and is zero-padded to 4 digits.
    """
    if nonce is None:
        nonce = uuid.uuid4().hex[:8]
    if not re.fullmatch(r"[0-9a-f]{8}", nonce):
        raise ValueError("nonce must be exactly 8 lowercase hex chars")
    if not (1 <= seq <= 9999):
        raise ValueError("seq must be in 1..9999")
    return f"{CMD_PREFIX}{nonce}-{seq:04d}"


def is_command_id(value: str) -> bool:
    return bool(_CMD_ID_RE.fullmatch(value))


def command_file_path(queue_dir: Path, command_id: str) -> Path:
    return queue_dir / f"{CMD_PREFIX}{command_id}.json" if command_id.startswith("CMD-") \
        else queue_dir / f"{command_id}.json"


def result_file_path(queue_dir: Path, command_id: str) -> Path:
    return queue_dir / f"{RESULT_PREFIX}{command_id}.json"


def command_id_from_file_name(name: str) -> Optional[str]:
    """Extract the command ID from a ``CMD-<id>.json`` file name."""
    if name.startswith(CMD_PREFIX) and name.endswith(".json"):
        return name[len(CMD_PREFIX):-len(".json")]
    return None


def result_id_from_file_name(name: str) -> Optional[str]:
    """Extract the command ID from a ``result-<id>.json`` file name."""
    if name.startswith(RESULT_PREFIX) and name.endswith(".json"):
        return name[len(RESULT_PREFIX):-len(".json")]
    return None


def write_command(queue_dir: Path, op: str, params: Optional[dict] = None,
                  command_id: Optional[str] = None,
                  delay_ms: int = 0, created_at: Optional[str] = None) -> str:
    """Atomically write a command file; returns its command ID."""
    if command_id is None:
        command_id = make_command_id()
    if not is_command_id(command_id):
        raise ValueError(f"invalid command ID: {command_id!r}")
    cmd = {
        "schema_version": SCHEMA_VERSION,
        "command_id": command_id,
        "op": op,
        "params": params or {},
        "created_at": created_at or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "delay_ms": int(delay_ms),
    }
    queue_dir.mkdir(parents=True, exist_ok=True)
    _atomic_write(command_file_path(queue_dir, command_id), cmd)
    return command_id


def read_command(queue_dir: Path, command_id: str) -> Optional[dict]:
    path = command_file_path(queue_dir, command_id)
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def has_result(queue_dir: Path, command_id: str) -> bool:
    return result_file_path(queue_dir, command_id).exists()


def list_pending(queue_dir: Path) -> list[str]:
    """Return command IDs whose command file exists but result file does not."""
    queue_dir.mkdir(parents=True, exist_ok=True)
    pending: list[str] = []
    for path in sorted(queue_dir.glob(CMD_GLOB)):
        cid = command_id_from_file_name(path.name)
        if cid is None:
            continue
        if not has_result(queue_dir, cid):
            pending.append(cid)
    return pending


def write_result(queue_dir: Path, command_id: str, status: str,
                 data=None, error: Optional[dict] = None,
                 started_at: Optional[str] = None,
                 completed_at: Optional[str] = None) -> Path:
    """Atomically write the durable result file (ack) for a command ID."""
    result = {
        "schema_version": SCHEMA_VERSION,
        "command_id": command_id,
        "status": status,
        "data": data,
        "error": error,
        "started_at": started_at,
        "completed_at": completed_at or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    queue_dir.mkdir(parents=True, exist_ok=True)
    return _atomic_write(result_file_path(queue_dir, command_id), result)


def read_result(queue_dir: Path, command_id: str) -> Optional[dict]:
    path = result_file_path(queue_dir, command_id)
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def process_once(queue_dir: Path, execute: Callable[[str, dict], tuple],
                 poll_delay_s: float = 0.05,
                 log=None) -> list[str]:
    """Process exactly one pass over the queue: execute every pending command.

    ``execute(op, params)`` must return ``(ok: bool, data, error_dict)``.
    Replays are safe: a command whose result file already exists is skipped.
    Returns the list of command IDs processed (executed) this pass.
    """
    processed: list[str] = []
    for cid in list_pending(queue_dir):
        cmd = read_command(queue_dir, cid)
        if cmd is None:
            continue
        started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        delay_ms = int(cmd.get("delay_ms") or 0)
        if delay_ms > 0:
            time.sleep(delay_ms / 1000.0)
        try:
            ok, data, err = execute(cmd.get("op"), cmd.get("params") or {})
        except Exception as exc:  # noqa: BLE001 — a command must never wedge the queue
            ok, data, err = False, None, {"code": "executor_error", "message": str(exc)}
        if ok:
            write_result(queue_dir, cid, "ok", data=data, started_at=started)
        else:
            write_result(queue_dir, cid, "error", error=err, started_at=started)
        if log:
            log(f"processed {cid}: op={cmd.get('op')} status={'ok' if ok else 'error'}")
        processed.append(cid)
        time.sleep(poll_delay_s)
    return processed


def _atomic_write(path: Path, payload: dict) -> Path:
    """Write a JSON payload atomically (temp file + rename)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with open(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
        tmp_path = Path(tmp_name)
        tmp_path.replace(path)
    except BaseException:
        Path(tmp_name).unlink(missing_ok=True)
        raise
    return path
