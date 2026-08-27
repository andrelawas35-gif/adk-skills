"""Screenplay-breakdown to Shot Work Objects (COMP-049).

WO 2026-08-25-011 slice 2. Parses minimal screenplay-breakdown text into shot
specs, creates a real Shot Work Object per spec via the public ``ws create``
CLI, and optionally links each child->parent via ``ws relation add
--type depends_on`` (the V1 hierarchy verb). All writes go through the CLI so
optimistic concurrency and schema validation stay authoritative.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent.parent

_SHOT_LINE = re.compile(r"^SHOT\s+([A-Za-z0-9_\-]+)\s*:\s*(.+)$")


class BreakdownError(ValueError):
    pass


def _run_cli(args: list[str], expect_ok: bool = True) -> subprocess.CompletedProcess:
    proc = subprocess.run(
        [sys.executable, "-m", "tools.ws", *args],
        cwd=str(REPO), capture_output=True, text=True,
    )
    if expect_ok and proc.returncode != 0:
        raise BreakdownError(
            f"ws {' '.join(args)} failed ({proc.returncode}): "
            f"{proc.stdout.strip()} {proc.stderr.strip()}"
        )
    return proc


def parse_breakdown(text: str) -> list[dict]:
    """Parse breakdown text into ordered shot specs.

    Format: one shot per line — ``SHOT <key>: <description>``. Blank lines and
    ``#`` comments are ignored; any other non-empty line is a hard error
    naming the line (no silent skips).
    """
    shots: list[dict] = []
    errors: list[str] = []
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = _SHOT_LINE.match(line)
        if not m:
            errors.append(f"line {lineno}: unrecognized breakdown syntax: {raw!r}")
            continue
        key, description = m.group(1), m.group(2).strip()
        if any(s["key"] == key for s in shots):
            errors.append(f"line {lineno}: duplicate shot key {key!r}")
            continue
        shots.append({"key": key, "description": description})
    if errors:
        raise BreakdownError("breakdown parse failed:\n" + "\n".join(errors))
    return shots


def _wo_path(wo_id: str) -> Path:
    matches = sorted((REPO / ".work-studio" / "objects").glob(f"**/{wo_id}*.md"))
    if not matches:
        raise BreakdownError(f"WO not found: {wo_id}")
    return matches[0]


def read_updated_at(wo_id: str) -> str:
    content = _wo_path(wo_id).read_text(encoding="utf-8")
    m = re.search(r"(?m)^updated_at:\s*(\S+)", content)
    if not m:
        raise BreakdownError(f"no updated_at on {wo_id}")
    return m.group(1)


def create_shot_wos(
    text: str,
    parent_wo_id: str | None = None,
    title_prefix: str = "Shot",
) -> list[dict]:
    """Create one real Shot WO per parsed spec; optionally link to a parent.

    Returns ordered results: ``{key, wo_id, linked}``. Creation is
    all-or-nothing per shot at the CLI level; an error mid-way leaves earlier
    WOs in place (they remain valid records) and raises.
    """
    shots = parse_breakdown(text)
    if not shots:
        raise BreakdownError("breakdown contains no SHOT lines")
    results: list[dict] = []
    for spec in shots:
        title = f"{title_prefix} {spec['key']} — {spec['description'][:80]}"
        proc = _run_cli([
            "create", "--title", title,
            "--type", "change", "--consequence", "low",
            "--sensitivity", "ordinary",
        ])
        m = re.search(r"(?m)^ID:\s*(\S+)$", proc.stdout)
        if not m:
            raise BreakdownError(f"could not parse created WO id: {proc.stdout!r}")
        wo_id = m.group(1)
        linked = False
        if parent_wo_id:
            updated_at = read_updated_at(wo_id)
            _run_cli([
                "relation", "add", wo_id, "--type", "depends_on",
                "--to", parent_wo_id, "--expect-updated", updated_at,
            ])
            linked = True
        results.append({"key": spec["key"], "wo_id": wo_id, "linked": linked})
        print(f"[breakdown] {spec['key']} -> {wo_id} (linked={linked})")
    return results
