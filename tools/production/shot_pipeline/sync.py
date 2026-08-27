"""StateSync: mirror gated-pipeline progress into a real Shot Work Object.

WO 2026-08-25-008 slice 3 (Decision recorded 2026-08-26). Drives the public
``ws shot-status`` CLI (optimistic-concurrency guarded) for production-status
transitions, plus one supplementary atomic frontmatter update for ``shot_tier``
reusing the repo's own helpers. ``ws validate`` runs after every write; only
errors NEW against a captured baseline count as failures.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(REPO))  # import tools.ws.* as the CLI package does

TIER_TO_STATUS = {"tier_a": "blocking", "tier_b": "render", "tier_c": "review"}
FINAL_STATUS = "approved"


class SyncError(RuntimeError):
    pass


class StateSync:
    """Keep a Shot WO's frontmatter in step with pipeline progression."""

    def __init__(self, wo_id: str):
        self.wo_id = wo_id
        self._updated_at = self._read_updated_at()
        self._synced: set[str] = set()

    # ── low-level helpers ────────────────────────────────────────────
    def _wo_path(self) -> Path:
        matches = sorted(
            (REPO / ".work-studio" / "objects").glob(f"**/{self.wo_id}*.md")
        )
        if not matches:
            raise SyncError(f"Shot WO not found: {self.wo_id}")
        return matches[0]

    def _read_updated_at(self) -> str:
        content = self._wo_path().read_text(encoding="utf-8")
        m = re.search(r"(?m)^updated_at:\s*(\S+)", content)
        if not m:
            raise SyncError("no updated_at in Shot WO frontmatter")
        return m.group(1)

    def _run_cli(self, args: list[str], expect_ok: bool = True) -> subprocess.CompletedProcess:
        proc = subprocess.run(
            [sys.executable, "-m", "tools.ws", *args],
            cwd=str(REPO), capture_output=True, text=True,
        )
        if expect_ok and proc.returncode != 0:
            raise SyncError(
                f"ws {' '.join(args)} failed ({proc.returncode}): "
                f"{proc.stdout.strip()} {proc.stderr.strip()}"
            )
        return proc

    def validate(self, baseline_errors: int) -> int:
        proc = self._run_cli(["validate"], expect_ok=False)
        output = proc.stdout + proc.stderr
        m = re.search(r"(\d+) validation error", output)
        errors = int(m.group(1)) if m else (1 if proc.returncode else 0)
        if errors > baseline_errors:
            raise SyncError(
                f"ws validate regressed: {errors} validation errors "
                f"(baseline {baseline_errors})\n{output[-2000:]}"
            )
        return errors

    # ── public sync API ──────────────────────────────────────────────
    def on_tier_executed(self, tier: str) -> dict | None:
        if tier in self._synced:
            return None
        status = TIER_TO_STATUS[tier]
        self._transition_status(status)
        self._set_shot_tier(tier)
        self._synced.add(tier)
        return {"tier": tier, "shot_status": status}

    def on_complete(self) -> dict:
        self._transition_status(FINAL_STATUS)
        self._set_shot_tier("final")
        return {"tier": "final", "shot_status": FINAL_STATUS}

    # ── internals ────────────────────────────────────────────────────
    def _transition_status(self, new_status: str) -> None:
        proc = self._run_cli(
            ["shot-status", self.wo_id, "--shot-status", new_status,
             "--actor", "shot-pipeline",
             "--expect-updated", self._updated_at],
        )
        m = re.search(r"updated_at (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)", proc.stdout)
        if not m:
            raise SyncError(f"could not parse new updated_at: {proc.stdout!r}")
        self._updated_at = m.group(1)

    def _set_shot_tier(self, tier: str) -> None:
        from tools.ws.atomic import atomic_write_text
        from tools.ws.shot_status import (
            _update_frontmatter_fields,
            compose_object_text,
        )

        path = self._wo_path()
        content = path.read_text(encoding="utf-8")
        current = re.search(r"(?m)^updated_at:\s*(\S+)", content).group(1)
        if current != self._updated_at:
            raise SyncError(
                f"concurrency drift before tier write: file {current} != "
                f"cached {self._updated_at}"
            )
        new_fm = _update_frontmatter_fields(
            content, {"shot_tier": tier, "updated_at": self._updated_at}
        )
        body = content[content.find("---", 3) + 3:].strip()
        atomic_write_text(path, compose_object_text(new_fm, body))
