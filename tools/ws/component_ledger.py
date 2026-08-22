"""Read-only parsing helpers for .work-studio/component-ledger.md.

Used by the command center to surface per-governance-domain component
counts without duplicating the ledger's full detail (ADR 0014;
`alawas-design-track-components` owns the ledger's content).
"""
from __future__ import annotations

import re
from pathlib import Path

_ENTRY_RE = re.compile(r"^##\s+(?P<comp_id>COMP-\d+)\s", re.MULTILINE)
_FIELD_RE = re.compile(r"^-\s+\*\*(?P<name>[^*]+):\*\*\s*(?P<value>.+?)\s*$", re.MULTILINE)


def parse_component_entries(text: str) -> list[dict[str, str]]:
    """Return one dict per COMP-### entry with its top-level bullet fields."""
    starts = [(m.start(), m.group("comp_id")) for m in _ENTRY_RE.finditer(text)]
    entries = []
    for i, (start, comp_id) in enumerate(starts):
        end = starts[i + 1][0] if i + 1 < len(starts) else len(text)
        body = text[start:end]
        fields = {m.group("name").strip(): m.group("value").strip() for m in _FIELD_RE.finditer(body)}
        fields["id"] = comp_id
        entries.append(fields)
    return entries


def domain_summary(workspace_root: Path, domain: str) -> dict:
    """Return status counts and open-findings count for one governance domain."""
    ledger_path = workspace_root / ".work-studio" / "component-ledger.md"
    if not ledger_path.exists():
        return {"total": 0, "by_status": {}, "open_findings": 0}

    entries = parse_component_entries(ledger_path.read_text(encoding="utf-8"))
    matched = [e for e in entries if e.get("governance domain") == domain]

    by_status: dict[str, int] = {}
    open_findings = 0
    for e in matched:
        status = e.get("status", "unknown")
        by_status[status] = by_status.get(status, 0) + 1
        findings = e.get("open findings", "")
        if findings and not findings.lower().startswith("none"):
            open_findings += 1

    return {"total": len(matched), "by_status": by_status, "open_findings": open_findings}
