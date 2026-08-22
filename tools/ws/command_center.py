"""Read-only Work Studio command center generator (WO 2026-08-22-006).

Renders .work-studio/objects/**/*.md + active.md into a static HTML file at
.work-studio/command-center.html. Never writes to any other file under
.work-studio/ -- a read-only projection, never a source (EVIDENCE-MODEL.md).
"""
import html
import re
from datetime import datetime, timezone
from pathlib import Path

from .component_ledger import domain_summary
from .design_assets import asset_record_paths, parse_asset_fields, validate_asset_record

FIELDS = ["id", "title", "type", "state", "status", "consequence", "sensitivity", "next_action", "updated_at"]

STATE_CLASS = {
    "notice": "c-gray", "explore": "c-blue", "design": "c-purple",
    "build": "c-amber", "verify": "c-teal", "release": "c-coral",
    "observe": "c-pink", "close": "c-gray",
}
CONS_CLASS = {"low": "cons-low", "meaningful": "cons-med", "high": "cons-high"}


def _parse_frontmatter(text: str):
    if not text.startswith("---"):
        return None, "does not start with '---'"
    end_idx = text.find("\n---", 3)
    if end_idx == -1:
        return None, "no closing '---' found"
    fm_block = text[3:end_idx]
    result = {}
    for line in fm_block.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        m = re.match(r"^([a-zA-Z_]+):\s*(.*)$", stripped)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip().strip('"')
        if key in FIELDS:
            result[key] = val
    missing = [f for f in FIELDS if f not in result]
    if missing:
        return result, f"missing fields: {missing}"
    return result, None


def _staleness(iso: str) -> str:
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    diff = datetime.now(timezone.utc) - dt
    mins = int(diff.total_seconds() / 60)
    if mins < 60:
        return f"{mins}m ago"
    hrs = mins // 60
    if hrs < 24:
        return f"{hrs}h ago"
    return f"{hrs // 24}d ago"


def _load_active_roles(active_md: Path):
    if not active_md.exists():
        return {}
    text = active_md.read_text(encoding="utf-8")
    roles = {}
    for line in text.splitlines():
        m = re.match(r"^-\s*`([\w-]+)`.*\((primary|supporting|paused)\)", line, re.IGNORECASE)
        if m:
            roles[m.group(1)] = m.group(2).lower()
    return roles


def _row_html(wo, role, dim):
    state = wo["state"]
    cons = wo["consequence"]
    opacity = "opacity:0.55;" if dim else ""
    return f"""<div class="row" style="{opacity}">
  <span class="pill {STATE_CLASS.get(state, 'c-gray')}">{html.escape(state)}</span>
  <span class="id">{html.escape(wo['id'])}</span>
  <span class="title">{html.escape(wo['title'])}</span>
  <span class="cons {CONS_CLASS.get(cons, '')}">{html.escape(cons)}</span>
  <span class="stale">{_staleness(wo['updated_at'])}</span>
  <span class="attn">{html.escape(role or '')}</span>
</div>"""


def _asset_summary(ws_root: Path) -> dict:
    """Status/validation counts over local design asset records."""
    paths = asset_record_paths(ws_root)
    by_status: dict[str, int] = {}
    gaps = 0
    for path in paths:
        fields = parse_asset_fields(path.read_text(encoding="utf-8"))
        status = fields.get("Status", "unknown")
        by_status[status] = by_status.get(status, 0) + 1
        if validate_asset_record(path):
            gaps += 1
    return {"total": len(paths), "by_status": by_status, "gaps": gaps}


def _status_pills_html(by_status: dict[str, int]) -> str:
    if not by_status:
        return '<span class="count-empty">none</span>'
    return " ".join(
        f'<span class="count-pill">{html.escape(status)}: {count}</span>'
        for status, count in sorted(by_status.items())
    )


def _summary_card_html(title: str, total: int, by_status: dict[str, int], flag_label: str, flag_count: int, link_text: str) -> str:
    flag_html = ""
    if flag_count:
        flag_html = f'<div class="card-flag">{flag_count} {html.escape(flag_label)}</div>'
    return f"""<div class="summary-card">
  <div class="card-head"><span class="card-title">{html.escape(title)}</span><span class="card-total">{total}</span></div>
  <div class="card-pills">{_status_pills_html(by_status)}</div>
  {flag_html}
  <div class="card-link">{html.escape(link_text)}</div>
</div>"""


def generate(ws_root: Path) -> dict:
    """Generate the command center HTML under ws_root/.work-studio/.

    Returns a summary dict: active, closed, failed, primary, supporting, out_path.
    """
    objects_dir = ws_root / ".work-studio" / "objects"
    active_md = ws_root / ".work-studio" / "active.md"
    out_path = ws_root / ".work-studio" / "command-center.html"

    roles = _load_active_roles(active_md)
    primary_count = sum(1 for r in roles.values() if r == "primary")
    supporting_count = sum(1 for r in roles.values() if r == "supporting")

    asset_summary = _asset_summary(ws_root)
    engineering_summary = domain_summary(ws_root, "engineering")

    summary_cards_html = (
        _summary_card_html(
            "Asset management", asset_summary["total"], asset_summary["by_status"],
            "validation gap(s)", asset_summary["gaps"],
            "See .work-studio/asset-workbench.html for detail",
        )
        + _summary_card_html(
            "Engineering", engineering_summary["total"], engineering_summary["by_status"],
            "with open findings", engineering_summary["open_findings"],
            "See .work-studio/component-ledger.md (governance domain: engineering) for detail",
        )
    )

    active_rows, closed_rows, failures = [], [], []
    for f in sorted(objects_dir.glob("**/*.md")):
        text = f.read_text(encoding="utf-8")
        wo, error = _parse_frontmatter(text)
        if error:
            failures.append((f, error))
            continue
        role = roles.get(wo["id"])
        if wo["status"] == "closed":
            closed_rows.append(_row_html(wo, role, dim=True))
        else:
            active_rows.append(_row_html(wo, role, dim=False))

    banner = ""
    if primary_count == 0:
        banner = (
            '<div class="banner"><i class="ti ti-alert-triangle" aria-hidden="true"></i> '
            f'No primary work object set — {supporting_count} supporting, 0 primary</div>'
        )

    failure_html = ""
    if failures:
        items = "".join(f"<li>{html.escape(str(f))}: {html.escape(e)}</li>" for f, e in failures)
        failure_html = f'<div class="banner danger">{len(failures)} file(s) failed to parse:<ul>{items}</ul></div>'

    html_doc = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Work Studio command center</title>
<style>
body {{ font-family: -apple-system, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; background: #fff; }}
h1 {{ font-size: 20px; font-weight: 500; }}
.section-label {{ font-size: 13px; font-weight: 500; color: #666; margin: 1.25rem 0 8px; }}
.row {{ display: flex; align-items: center; gap: 10px; padding: 8px 4px; border-bottom: 0.5px solid #ddd; font-size: 13px; }}
.pill {{ font-size: 11px; padding: 2px 8px; border-radius: 6px; flex-shrink: 0; background: #eee; }}
.id {{ font-family: monospace; font-size: 12px; color: #666; flex-shrink: 0; width: 112px; }}
.title {{ flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.cons {{ font-size: 11px; flex-shrink: 0; width: 70px; color: #666; }}
.cons-high {{ color: #b91c1c; font-weight: 600; }}
.stale {{ font-size: 11px; color: #666; flex-shrink: 0; width: 56px; }}
.attn {{ font-size: 11px; color: #666; flex-shrink: 0; width: 64px; text-align: right; }}
.banner {{ display: flex; align-items: center; gap: 10px; padding: 10px 14px; background: #fff7ed; border-radius: 8px; margin-bottom: 1rem; font-size: 13px; color: #92400e; }}
.banner.danger {{ background: #fef2f2; color: #991b1b; }}
button {{ margin-top: 1rem; font-size: 12px; padding: 4px 10px; }}
#closed-wrap {{ display: none; margin-top: 8px; }}
.summary-row {{ display: flex; gap: 12px; margin-bottom: 4px; }}
.summary-card {{ flex: 1; border: 1px solid #e5e5e5; border-radius: 8px; padding: 10px 12px; }}
.card-head {{ display: flex; align-items: baseline; justify-content: space-between; }}
.card-title {{ font-size: 13px; font-weight: 500; }}
.card-total {{ font-size: 18px; font-weight: 500; }}
.card-pills {{ margin-top: 6px; display: flex; flex-wrap: wrap; gap: 6px; }}
.count-pill {{ font-size: 11px; padding: 2px 8px; border-radius: 6px; background: #eee; color: #555; }}
.count-empty {{ font-size: 11px; color: #666; }}
.card-flag {{ margin-top: 6px; font-size: 11px; color: #b91c1c; }}
.card-link {{ margin-top: 8px; font-size: 11px; color: #666; }}
</style></head>
<body>
<h1>Work Studio command center</h1>
{banner}
{failure_html}
<div class="summary-row">
{summary_cards_html}
</div>
<div class="section-label">Active — {len(active_rows)}</div>
{''.join(active_rows)}
<button id="toggle" aria-controls="closed-wrap" aria-expanded="false">Show closed ({len(closed_rows)})</button>
<div id="closed-wrap">{''.join(closed_rows)}</div>
<script>
document.getElementById('toggle').addEventListener('click', function() {{
  const w = document.getElementById('closed-wrap');
  const hidden = w.style.display === 'none' || !w.style.display;
  w.style.display = hidden ? 'block' : 'none';
  this.setAttribute('aria-expanded', hidden ? 'true' : 'false');
  this.textContent = hidden ? 'Hide closed ({len(closed_rows)})' : 'Show closed ({len(closed_rows)})';
}});
</script>
</body></html>"""

    out_path.write_text(html_doc, encoding="utf-8")

    return {
        "active": len(active_rows),
        "closed": len(closed_rows),
        "failed": len(failures),
        "primary": primary_count,
        "supporting": supporting_count,
        "assets": asset_summary["total"],
        "asset_gaps": asset_summary["gaps"],
        "engineering_components": engineering_summary["total"],
        "out_path": out_path,
    }
