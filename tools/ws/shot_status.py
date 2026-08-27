"""Shot status transition for the V1 shot state machine (WO 2026-08-24-006).

Moves a Shot Work Object through its production states
(blocking → animation → render → review → approved) by updating the
``shot_status`` frontmatter field and appending a History entry. Reuses the
studio's atomic-write / optimistic-concurrency / History helpers.

Shot state lives in metadata (the V1 tracer validated this, Decision 2),
NOT the fixed ``ws transition`` state enum — the shot's production status is
orthogonal to the Work Object's lifecycle state. This command never touches
the source's lifecycle state/status.
"""

import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from .atomic import atomic_write_text
from .sections import append_to_section, compose_object_text

SHOT_STATES = ["blocking", "animation", "render", "review", "approved"]


def _parse_frontmatter_fields(content: str) -> dict:
    result = {}
    if not content.startswith("---"):
        return result
    end = content.find("\n---", 3)
    if end == -1:
        return result
    for line in content[3:end].split("\n"):
        m = re.match(r"^([a-zA-Z_]+):\s*(.*)$", line.strip())
        if m:
            result[m.group(1)] = m.group(2).strip().strip('"')
    return result


def _update_frontmatter_fields(content: str, updates: dict) -> str:
    """Update (or append, if missing) scalar fields in the frontmatter."""
    if not content.startswith("---"):
        return content
    end = content.find("---", 3)
    if end == -1:
        return content
    fm_text = content[4:end]
    lines = fm_text.split("\n")
    new_lines = []
    updated_keys = set()
    for line in lines:
        stripped = line.strip()
        if ":" in stripped and not stripped.startswith("#"):
            key = stripped.split(":", 1)[0].strip()
            if key in updates:
                new_lines.append(f"{key}: {updates[key]}")
                updated_keys.add(key)
                continue
        new_lines.append(line)
    for key, val in updates.items():
        if key not in updated_keys:
            new_lines.append(f"{key}: {val}")
    new_fm = "\n".join(new_lines)
    return "---\n" + new_fm + "\n---"


def _history_timestamp(body: str, now: datetime) -> str:
    """Return a whole-second timestamp strictly after any existing History entry.

    History headings are '### <ISO> — <action>'; whole-second stamps must be
    unique (rapid shot-status transitions otherwise collide, and ws validate
    flags duplicate timestamps). Bumps forward by whole seconds until unused.
    """
    existing = set(
        re.findall(r"(?m)^### (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)", body)
    )
    dt = now
    ts = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    while ts in existing:
        dt = dt + timedelta(seconds=1)
        ts = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    return ts


def transition(
    path: Path,
    new_status: str,
    actor: str = "system",
) -> dict:
    """Transition a Shot Work Object to a new production status.

    The caller performs the optimistic-concurrency check before calling.
    Returns a result dict with ok/error or the resulting record.
    """
    if new_status not in SHOT_STATES:
        return {
            "ok": False,
            "error": f"Invalid shot status '{new_status}'. "
                     f"Must be one of: {', '.join(SHOT_STATES)}",
        }

    content = path.read_text(encoding="utf-8")
    fm = _parse_frontmatter_fields(content)
    old_status = fm.get("shot_status") or "none"
    now = datetime.now(timezone.utc)
    body = content[content.find("---", 3) + 3:].strip()
    ts = _history_timestamp(body, now)

    history_entry = (
        f"### {ts} — Shot status: {old_status} → {new_status}\n\n"
        f"- **State:** {fm.get('state', 'notice')}\n"
        f"- **Status:** {fm.get('status', 'active')}\n"
        f"- **Actor:** {actor}\n"
        f"- **Rationale:** Shot state machine transition (V1, WO 2026-08-24-006)."
    )

    new_body = append_to_section(body, "history", history_entry)
    new_fm = _update_frontmatter_fields(
        content, {"shot_status": new_status, "updated_at": ts},
    )
    atomic_write_text(path, compose_object_text(new_fm, new_body))
    return {
        "ok": True,
        "old_status": old_status,
        "new_status": new_status,
        "updated_at": ts,
    }
