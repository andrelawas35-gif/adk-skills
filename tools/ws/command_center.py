"""Read-only Work Studio command center generator (WO 2026-08-22-006).

Renders .work-studio/objects/**/*.md + active.md into a static HTML file at
.work-studio/command-center.html. Never writes to any other file under
.work-studio/ -- a read-only projection, never a source (EVIDENCE-MODEL.md).
"""
import html
import re
from datetime import datetime, timezone
from pathlib import Path

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
.id {{ font-family: monospace; font-size: 12px; color: #888; flex-shrink: 0; width: 112px; }}
.title {{ flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.cons {{ font-size: 11px; flex-shrink: 0; width: 70px; color: #888; }}
.cons-high {{ color: #b91c1c; }}
.stale {{ font-size: 11px; color: #888; flex-shrink: 0; width: 56px; }}
.attn {{ font-size: 11px; color: #888; flex-shrink: 0; width: 64px; text-align: right; }}
.banner {{ display: flex; align-items: center; gap: 10px; padding: 10px 14px; background: #fff7ed; border-radius: 8px; margin-bottom: 1rem; font-size: 13px; color: #92400e; }}
.banner.danger {{ background: #fef2f2; color: #991b1b; }}
button {{ margin-top: 1rem; font-size: 12px; padding: 4px 10px; }}
#closed-wrap {{ display: none; margin-top: 8px; }}
</style></head>
<body>
<h1>Work Studio command center</h1>
{banner}
{failure_html}
<div class="section-label">Active — {len(active_rows)}</div>
{''.join(active_rows)}
<button id="toggle">Show closed ({len(closed_rows)})</button>
<div id="closed-wrap">{''.join(closed_rows)}</div>
<script>
document.getElementById('toggle').addEventListener('click', function() {{
  const w = document.getElementById('closed-wrap');
  const hidden = w.style.display === 'none' || !w.style.display;
  w.style.display = hidden ? 'block' : 'none';
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
        "out_path": out_path,
    }
