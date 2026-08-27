"""Narrow JS API bridge exposed to the Director Console UI."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable

from .workspace import DirectionConflict, DirectionError, WorkStudioWorkspace


def _approvals_module():
    """Import the shared approvals helpers from tools/production.

    Importing (not copying) the gate logic keeps console-written records
    structurally byte-compatible with pipeline.record_approval.
    """
    prod = Path(__file__).resolve().parents[1] / "tools" / "production"
    if str(prod) not in sys.path:
        sys.path.insert(0, str(prod))
    from shot_pipeline import approvals  # noqa: PLC0415 — lazy, path-bootstrapped

    return approvals


class DirectorConsoleBridge:
    """Small, structured API surface for the desktop tracer."""

    def __init__(self, workspace: WorkStudioWorkspace | None = None) -> None:
        self.workspace = workspace or WorkStudioWorkspace.discover(Path.cwd())

    def _response(self, fn: Callable[[], Any]) -> dict[str, Any]:
        try:
            return {"ok": True, "data": fn(), "error": None}
        except DirectionConflict as exc:
            return {"ok": False, "data": exc.payload, "error": {
                "code": "stale_update",
                "message": str(exc),
            }}
        except DirectionError as exc:
            return {"ok": False, "data": None, "error": {
                "code": "direction_error",
                "message": str(exc),
            }}
        except Exception as exc:  # UI boundary: return structured diagnostics.
            return {"ok": False, "data": None, "error": {
                "code": exc.__class__.__name__,
                "message": str(exc),
            }}

    def get_workspace_summary(self) -> dict[str, Any]:
        return self._response(self.workspace.summary)

    def get_scene(self, scene_id: str) -> dict[str, Any]:
        return self._response(lambda: self.workspace.get_scene(scene_id))

    def submit_direction(
        self,
        scene_id: str,
        text: str,
        expected_updated_at: str,
    ) -> dict[str, Any]:
        return self._response(
            lambda: self.workspace.submit_direction(
                scene_id,
                text,
                expected_updated_at,
            )
        )

    def render_scene_board(self) -> dict[str, Any]:
        return self._response(self.workspace.render_scene_board)

    def open_local_artifact(self, path: str) -> dict[str, Any]:
        return self._response(lambda: self.workspace.open_local_artifact(path))

    def gate_status(self, work_dir: str) -> dict[str, Any]:
        approvals = _approvals_module()
        return self._response(lambda: approvals.status_payload(Path(work_dir)))

    def approve_gate(self, work_dir: str, tier: str,
                     approver: str = "director") -> dict[str, Any]:
        approvals = _approvals_module()

        def write() -> dict[str, Any]:
            path = approvals.approve_gate(Path(work_dir), tier, approver=approver)
            return {"record": path.name, "tier": tier}

        return self._response(write)

    def deny_gate(self, work_dir: str, tier: str, reason: str = "unspecified",
                  approver: str = "director") -> dict[str, Any]:
        approvals = _approvals_module()

        def write() -> dict[str, Any]:
            path = approvals.deny_gate(
                Path(work_dir), tier, reason=reason, approver=approver)
            return {"record": path.name, "tier": tier,
                    "shot_remains": "waiting_for_approval"}

        return self._response(write)
