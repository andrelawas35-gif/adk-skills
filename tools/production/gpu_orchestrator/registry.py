"""Local file-backed GPU claim registry for sequential VRAM discipline.

Tracer for WO 2026-08-24-013 / COMP-041. The registry deliberately launches
no GPU processes and makes no scheduling decisions. It only records one
current GPU owner, rejects competing live claims, and lets a stale owner be
recovered after an unclean release.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
import tempfile
import time
from pathlib import Path
from typing import Optional

SCHEMA_VERSION = 1
STATE_FILE = "gpu-claim-state.json"
LOCK_FILE = "gpu-claim-state.lock"
LOCK_STALE_AFTER_S = 30.0

OWNER_TO_STATE = {
    "blender": "blender_loaded",
    "comfyui_flux": "comfyui_flux_loaded",
    "comfyui_hunyuan": "comfyui_hunyuan_loaded",
}
GPU_STATES = ("idle", *OWNER_TO_STATE.values())


@dataclass(frozen=True)
class ClaimResult:
    granted: bool
    state: str
    owner: Optional[str]
    owner_id: Optional[str]
    reason: str
    recovered_from: Optional[dict] = None


def query(registry_dir: Path) -> dict:
    """Return the current GPU state without mutating it."""
    registry_dir.mkdir(parents=True, exist_ok=True)
    path = _state_path(registry_dir)
    if not path.exists():
        return _idle_state()
    return _read_state(path)


def claim(
    registry_dir: Path,
    owner: str,
    owner_id: str,
    *,
    stale_after_s: float,
    now_s: Optional[float] = None,
) -> ClaimResult:
    """Claim the single GPU slot for ``owner``.

    A live owner blocks the claim. A stale owner may be replaced, which models
    the accepted crash-recovery path without adding a scheduler or daemon.
    """
    if owner not in OWNER_TO_STATE:
        raise ValueError(f"unknown GPU owner: {owner!r}")
    if not owner_id:
        raise ValueError("owner_id is required")
    if stale_after_s <= 0:
        raise ValueError("stale_after_s must be positive")

    now = _now(now_s)
    with _file_lock(registry_dir, now_s=now):
        current = query(registry_dir)
        current_owner = current.get("owner")
        current_owner_id = current.get("owner_id")
        recovered_from = None

        if current["state"] != "idle":
            if current_owner == owner and current_owner_id == owner_id:
                refreshed = _claimed_state(owner, owner_id, now)
                _write_state(_state_path(registry_dir), refreshed)
                return _result(True, refreshed, "refreshed")

            if not _is_stale(current, stale_after_s, now):
                return ClaimResult(
                    granted=False,
                    state=current["state"],
                    owner=current_owner,
                    owner_id=current_owner_id,
                    reason="occupied",
                )

            recovered_from = {
                "state": current["state"],
                "owner": current_owner,
                "owner_id": current_owner_id,
                "claimed_at_s": current.get("claimed_at_s"),
                "heartbeat_at_s": current.get("heartbeat_at_s"),
            }

        claimed = _claimed_state(owner, owner_id, now)
        if recovered_from:
            claimed["recovered_from"] = recovered_from
        _write_state(_state_path(registry_dir), claimed)
        return _result(True, claimed, "claimed", recovered_from=recovered_from)


def release(
    registry_dir: Path,
    owner: str,
    owner_id: str,
    *,
    now_s: Optional[float] = None,
) -> ClaimResult:
    """Release the GPU slot when called by the current owner."""
    now = _now(now_s)
    with _file_lock(registry_dir, now_s=now):
        current = query(registry_dir)
        if current["state"] == "idle":
            return _result(True, current, "already_idle")
        if current.get("owner") != owner or current.get("owner_id") != owner_id:
            return ClaimResult(
                granted=False,
                state=current["state"],
                owner=current.get("owner"),
                owner_id=current.get("owner_id"),
                reason="owner_mismatch",
            )

        idle = _idle_state(now)
        _write_state(_state_path(registry_dir), idle)
        return _result(True, idle, "released")


def _state_path(registry_dir: Path) -> Path:
    return registry_dir / STATE_FILE


def _lock_path(registry_dir: Path) -> Path:
    return registry_dir / LOCK_FILE


def _now(now_s: Optional[float] = None) -> float:
    return float(time.time() if now_s is None else now_s)


def _idle_state(now_s: Optional[float] = None) -> dict:
    state = {
        "schema_version": SCHEMA_VERSION,
        "state": "idle",
        "owner": None,
        "owner_id": None,
        "claimed_at_s": None,
        "heartbeat_at_s": None,
    }
    if now_s is not None:
        state["released_at_s"] = now_s
    return state


def _claimed_state(owner: str, owner_id: str, now_s: float) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "state": OWNER_TO_STATE[owner],
        "owner": owner,
        "owner_id": owner_id,
        "claimed_at_s": now_s,
        "heartbeat_at_s": now_s,
    }


def _is_stale(state: dict, stale_after_s: float, now_s: float) -> bool:
    heartbeat = state.get("heartbeat_at_s")
    if heartbeat is None:
        heartbeat = state.get("claimed_at_s")
    if heartbeat is None:
        return True
    return now_s - float(heartbeat) >= stale_after_s


def _read_state(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        state = json.load(fh)
    if state.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported GPU claim registry schema_version")
    if state.get("state") not in GPU_STATES:
        raise ValueError(f"invalid GPU state: {state.get('state')!r}")
    return state


def _write_state(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, sort_keys=True)
        Path(tmp_name).replace(path)
    except BaseException:
        Path(tmp_name).unlink(missing_ok=True)
        raise


def _result(
    granted: bool,
    state: dict,
    reason: str,
    *,
    recovered_from: Optional[dict] = None,
) -> ClaimResult:
    return ClaimResult(
        granted=granted,
        state=state["state"],
        owner=state.get("owner"),
        owner_id=state.get("owner_id"),
        reason=reason,
        recovered_from=recovered_from,
    )


class _file_lock:
    """Tiny cross-process lock using exclusive file creation."""

    def __init__(self, registry_dir: Path, *, now_s: float):
        self.registry_dir = registry_dir
        self.path = _lock_path(registry_dir)
        self.now_s = now_s
        self.fd: Optional[int] = None

    def __enter__(self) -> "_file_lock":
        self.registry_dir.mkdir(parents=True, exist_ok=True)
        while True:
            try:
                self.fd = os.open(
                    str(self.path),
                    os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                )
                os.write(self.fd, str(self.now_s).encode("ascii"))
                return self
            except FileExistsError:
                self._clear_stale_lock()
                time.sleep(0.005)

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None
        self.path.unlink(missing_ok=True)

    def _clear_stale_lock(self) -> None:
        try:
            age = time.time() - self.path.stat().st_mtime
        except FileNotFoundError:
            return
        if age >= LOCK_STALE_AFTER_S:
            self.path.unlink(missing_ok=True)
