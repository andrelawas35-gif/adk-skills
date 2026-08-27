"""Read-only PRESERVED/CHANGED report generator (WO 2026-08-24-005).

Implements the accepted tracer-bullet design (Decision 2): given a Work
Object file, reads its frontmatter + append-only ``## History`` section and
emits a PRESERVED/CHANGED report — what the record shows as preserved (no
History entry records a change to it) vs. changed (the recorded trajectory:
state/status moves, decisions, evidence, next-action updates).

Follows the read-only projection pattern of ``scene_board.py`` /
``command_center.py``: never writes to the source Work Object or any other
canonical file. Grounded solely in existing ``updated_at`` + History — the
studio has no body-level baseline, so no diff-baseline mechanism is added.

The report is an inverse inference: "preserved" means "no History entry
records a change to this field/section". That limitation is the accepted
tracer's tested assumption; sparse History yields an explicit
"insufficient History" note rather than a fabricated classification.
"""

import re
from pathlib import Path

# Identity/classification fields the schema treats as immutable; reported as
# preserved when no History entry records a change to them.
IDENTITY_FIELDS = [
    "id", "title", "type", "consequence", "sensitivity", "domain", "created_at",
]

_TS = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"


def _extract_section(text: str, heading: str) -> str:
    """Return the body of a '## heading' section (scene_board-style)."""
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.MULTILINE)
    m = pattern.search(text)
    if not m:
        return ""
    start = m.end()
    next_h2 = re.search(r"^## ", text[start:], re.MULTILINE)
    end = start + next_h2.start() if next_h2 else len(text)
    return text[start:end].strip()


def _parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    result = {}
    for line in text[3:end].split("\n"):
        m = re.match(r"^([a-zA-Z_]+):\s*(.*)$", line.strip())
        if m:
            result[m.group(1)] = m.group(2).strip().strip('"')
    return result


def _parse_history_entries(history_text: str) -> list[dict]:
    """Parse '### <ISO> — <action>' subsections with '- **Field:** value' bullets."""
    entries = []
    for block in re.split(r"(?m)^### ", history_text):
        block = block.strip()
        if not block:
            continue
        lines = block.split("\n")
        header = lines[0]
        m = re.match(rf"^({_TS})\s*[—-]\s*(.+)$", header)
        if not m:
            continue
        entry = {
            "timestamp": m.group(1),
            "action": m.group(2).strip(),
            "state": None,
            "status": None,
            "actor": None,
            "rationale": None,
        }
        for line in lines[1:]:
            # Accept both "**Field:** value" (colon inside the bold, the format
            # generate_history_entry() writes) and "**Field**: value". A
            # trailing colon on the key is stripped. (Same root cause as the
            # scene_board thesis fix, WO 2026-08-23-001.)
            fm = re.match(r"^-\s+\*\*(.+?)\*\*:?\s*(.*)$", line)
            if fm:
                key = fm.group(1).strip().rstrip(":").lower()
                if key in ("state", "status", "actor", "rationale"):
                    entry[key] = fm.group(2).strip()
        entries.append(entry)
    return entries


def _trajectory(sequence: list) -> list:
    """Collapse consecutive repeats into a compact ordered trajectory."""
    out = []
    for item in sequence:
        if item is None:
            continue
        if not out or out[-1] != item:
            out.append(item)
    return out


def generate(path: Path) -> dict:
    """Generate a PRESERVED/CHANGED report for one Work Object file.

    Returns a dict with ``id``, ``title``, and ``out_text`` (the report).
    """
    text = path.read_text(encoding="utf-8")
    fm = _parse_frontmatter(text)
    obj_id = fm.get("id", "?")
    title = fm.get("title", "?")

    entries = _parse_history_entries(_extract_section(text, "History"))

    # Changed trajectory (from History-recorded state/status per entry).
    state_traj = _trajectory([e["state"] for e in entries])
    status_traj = _trajectory([e["status"] for e in entries])

    # Counts derived from the current record.
    decisions = len(re.findall(r"(?m)^### Decision\s+\d+", text))
    evidence_rows = len(re.findall(
        r"(?m)^\|\s*\[", _extract_section(text, "Evidence ledger"),
    ))
    next_action_updates = sum(
        1 for e in entries if "next" in (e["action"] or "").lower()
    )

    lines = [
        f"PRESERVED / CHANGED report — {obj_id}",
        f"Title: {title}",
        f"Type: {fm.get('type', '?')} · Consequence: {fm.get('consequence', '?')} · "
        f"Sensitivity: {fm.get('sensitivity', '?')}",
        f"Created: {fm.get('created_at', '?')} · Updated: {fm.get('updated_at', '?')}",
        "",
    ]

    if not entries:
        lines.append(
            "Insufficient History to classify preserved vs changed "
            "(no History entries recorded)."
        )
    else:
        preserved = [f for f in IDENTITY_FIELDS if f in fm]
        lines.append(
            f"PRESERVED (no recorded change across {len(entries)} History entries):"
        )
        lines.append(f"  {', '.join(preserved)}")
        lines.append("")
        lines.append("CHANGED (recorded trajectory):")
        lines.append(
            f"  State: {' -> '.join(state_traj) if state_traj else 'none recorded'}"
        )
        lines.append(
            f"  Status: {' -> '.join(status_traj) if status_traj else 'none recorded'}"
        )
        lines.append(f"  Decisions recorded: {decisions}")
        lines.append(f"  Evidence entries: {evidence_rows}")
        lines.append(
            f"  Next-action/next-move updates (from History action wording): "
            f"{next_action_updates}"
        )
        lines.append(
            f"  History entries: {len(entries)} "
            f"(earliest {entries[0]['timestamp']}, latest {entries[-1]['timestamp']})"
        )

    return {"id": obj_id, "title": title, "out_text": "\n".join(lines)}
