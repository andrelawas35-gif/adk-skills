"""Workspace access for the Director Console desktop tracer."""

from __future__ import annotations

import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

from tools.ws.scene_board import (
    _extract_section,
    _extract_subsections,
    _extract_table,
    _extract_thesis,
    _parse_frontmatter,
    generate as generate_scene_board,
)


Runner = Callable[..., subprocess.CompletedProcess[str]]


class DirectionError(RuntimeError):
    """A Direction write failed without mutating through this bridge."""


class DirectionConflict(DirectionError):
    """The scene changed since the UI loaded it."""

    def __init__(self, scene_id: str, expected: str, actual: str) -> None:
        super().__init__(
            f"{scene_id} changed before the Direction could be recorded."
        )
        self.payload = {
            "scene_id": scene_id,
            "expected_updated_at": expected,
            "actual_updated_at": actual,
        }


class WorkStudioWorkspace:
    """File-first access to one Work Studio workspace."""

    def __init__(self, root: Path, runner: Runner | None = None) -> None:
        self.root = root.resolve()
        self.work_studio = self.root / ".work-studio"
        self.objects_dir = self.work_studio / "objects"
        self.runner = runner or subprocess.run
        if not self.work_studio.is_dir():
            raise FileNotFoundError(f"Missing .work-studio directory: {self.root}")

    @classmethod
    def discover(cls, start: Path, runner: Runner | None = None) -> "WorkStudioWorkspace":
        current = start.resolve()
        for candidate in [current] + list(current.parents):
            if (candidate / ".work-studio").is_dir():
                return cls(candidate, runner=runner)
        raise FileNotFoundError(".work-studio was not found from this directory")

    def summary(self) -> dict[str, Any]:
        scenes = self.list_scenes()
        board = self.work_studio / "scene-board.html"
        return {
            "workspace_root": str(self.root),
            "scene_board_exists": board.exists(),
            "scene_board_path": self._relative_or_none(board) if board.exists() else None,
            "scene_count": len(scenes),
            "scenes": scenes,
            "default_scene_id": "2026-08-23-004" if any(
                s["id"] == "2026-08-23-004" for s in scenes
            ) else (scenes[0]["id"] if scenes else None),
        }

    def list_scenes(self) -> list[dict[str, Any]]:
        scenes = []
        for path in sorted(self.objects_dir.glob("**/*.md")):
            text = path.read_text(encoding="utf-8")
            if "## Screenplay" not in text:
                continue
            frontmatter, error = _parse_frontmatter(text)
            if error or not frontmatter:
                continue
            scenes.append({
                "id": frontmatter.get("id", path.stem),
                "title": frontmatter.get("title", "Untitled"),
                "state": frontmatter.get("state", ""),
                "status": frontmatter.get("status", ""),
                "updated_at": frontmatter.get("updated_at", ""),
                "path": self._relative_or_none(path),
            })
        return scenes

    def get_scene(self, scene_id: str) -> dict[str, Any]:
        path = self._resolve_object(scene_id)
        text = path.read_text(encoding="utf-8")
        frontmatter, error = _parse_frontmatter(text)
        if error or not frontmatter:
            raise ValueError(f"Invalid frontmatter for {scene_id}: {error}")

        return {
            "id": frontmatter.get("id", scene_id),
            "title": frontmatter.get("title", "Untitled"),
            "state": frontmatter.get("state", ""),
            "status": frontmatter.get("status", ""),
            "updated_at": frontmatter.get("updated_at", ""),
            "next_action": frontmatter.get("next_action", ""),
            "path": self._relative_or_none(path),
            "thesis": _extract_thesis(text),
            "screenplay": [
                {"name": name, "content": content}
                for name, content in _extract_subsections(text, "Screenplay")
            ],
            "director_layer": _extract_table(text, "Director Layer"),
            "evidence": _extract_table(text, "Evidence ledger")[-8:],
            "open_questions": _extract_section(text, "Open questions"),
        }

    def submit_direction(
        self,
        scene_id: str,
        text: str,
        expected_updated_at: str,
    ) -> dict[str, Any]:
        direction_text = text.strip()
        if not direction_text:
            raise DirectionError("Direction text is required.")
        if not expected_updated_at:
            raise DirectionError("expected_updated_at is required.")

        current = self.get_scene(scene_id)
        actual_updated_at = str(current.get("updated_at", ""))
        if actual_updated_at != expected_updated_at:
            raise DirectionConflict(scene_id, expected_updated_at, actual_updated_at)

        cmd = [
            sys.executable,
            "-m",
            "tools.ws",
            "direction",
            "--text",
            direction_text,
            "--record",
            scene_id,
            "--expect-updated",
            expected_updated_at,
        ]
        result = self.runner(
            cmd,
            cwd=self.root,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            message = (result.stderr or result.stdout or "Direction command failed").strip()
            raise DirectionError(message)

        return {
            "scene": self.get_scene(scene_id),
            "command": "python -m tools.ws direction",
            "output": result.stdout.strip(),
        }

    def render_scene_board(self) -> dict[str, Any]:
        summary = generate_scene_board(self.root)
        out_path = Path(summary["out_path"])
        return {
            "scenes": summary["scenes"],
            "path": self._relative_or_none(out_path),
        }

    def open_local_artifact(self, path: str) -> dict[str, Any]:
        target = self.resolve_workspace_path(path)
        if not target.exists():
            raise FileNotFoundError(f"Artifact not found: {path}")
        system = platform.system()
        if system == "Windows" and hasattr(os, "startfile"):
            os.startfile(str(target))  # type: ignore[attr-defined]
            launcher = "startfile"
        elif system == "Darwin":
            self.runner(["open", str(target)], check=False)
            launcher = "open"
        else:
            self.runner(["xdg-open", str(target)], check=False)
            launcher = "xdg-open"
        return {
            "path": self._relative_or_none(target),
            "opened": True,
            "launcher": launcher,
        }

    def resolve_workspace_path(self, path: str) -> Path:
        raw = Path(path)
        target = raw if raw.is_absolute() else self.root / raw
        resolved = target.resolve()
        try:
            resolved.relative_to(self.root)
        except ValueError as exc:
            raise ValueError(f"Path is outside the workspace: {path}") from exc
        return resolved

    def _resolve_object(self, scene_id: str) -> Path:
        for path in sorted(self.objects_dir.glob("**/*.md")):
            if path.name.startswith(scene_id):
                return path
        raise FileNotFoundError(f"Scene Work Object not found: {scene_id}")

    def _relative_or_none(self, path: Path) -> str:
        try:
            return str(path.resolve().relative_to(self.root)).replace("\\", "/")
        except ValueError:
            return str(path)
