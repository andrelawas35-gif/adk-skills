"""Read-only design asset workbench generator."""

from __future__ import annotations

import html
import re
from datetime import datetime, timezone
from pathlib import Path

from .design_assets import asset_record_paths, parse_asset_fields, validate_asset_record
from .design_asset_routing import FRONTIER_OWNERS

# Short, plain-language descriptions so the Frontier Ownership table is
# readable without already knowing the pipeline's internal vocabulary
# (design-critique-usability tracer finding, WO 2026-08-22-030).
FRONTIER_DESCRIPTIONS = {
    "identity": "asset intake, lifecycle status, and provenance",
    "foundation": "base design-system tokens and structure",
    "tokens": "semantic token definitions",
    "theme": "theme recipes built on tokens",
    "variant": "component variant relationships",
    "component-family": "related component groupings",
    "interaction-motion": "motion recipes, timing/easing, per-state interaction behavior",
    "ux-pattern": "reusable user goals, flows, and states",
    "flow": "multi-step user flows",
    "creative-direction": "confirmed creative interpretation and execution",
    "implementation": "reversible code implementation of an accepted change",
    "verification": "browser-visible parity against a confirmed direction",
    "accessibility": "WCAG conformance against a stewarded or generic baseline",
    "critique": "usability-heuristic evaluation independent of a confirmed direction",
    "component-registration": "durable shipped-component tracking and governance",
    "projection": "read-only catalog, graph, or comparison views",
}


def _section_body(text: str, section: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(section)}\s*$"
        rf"(?P<body>.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group("body").strip() if match else ""


def _plain(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`"):
        return value[1:-1]
    return value


def _asset_card(path: Path, ws_root: Path) -> tuple[str, list[str]]:
    text = path.read_text(encoding="utf-8")
    fields = parse_asset_fields(text)
    errors = validate_asset_record(path)
    rel = path.relative_to(ws_root).as_posix()
    asset_id = _plain(fields.get("Asset ID", "missing"))
    kind = fields.get("Asset kind", "missing")
    status = fields.get("Status", "missing")
    work_object = _plain(fields.get("Work Object", "missing"))
    source = fields.get("Source of truth", "missing")
    summary = _section_body(text, "Asset Summary")
    summary = re.sub(r"\s+", " ", summary).strip()
    lifecycle = _section_body(text, "Lifecycle")
    owner_names = []
    for line in lifecycle.splitlines():
        if not (line.startswith("|") and "`" in line and "Owning skill" not in line):
            continue
        match = re.search(r"`([^`]+)`", line)
        if match:
            owner_names.append(match.group(1))
    owners_display = ", ".join(f"<code>{html.escape(name)}</code>" for name in owner_names) if owner_names else "none"
    validation_class = "ok" if not errors else "bad"
    validation_text = "valid" if not errors else f"{len(errors)} gap(s)"

    card = f"""<section class="asset">
  <div class="asset-head">
    <div>
      <h2>{html.escape(asset_id)}</h2>
    </div>
    <span class="status {validation_class}">{html.escape(validation_text)}</span>
  </div>
  <p class="summary">{html.escape(summary)}</p>
  <dl>
    <dt>Asset kind</dt><dd>{html.escape(kind)}</dd>
    <dt>Status</dt><dd>{html.escape(status)}</dd>
    <dt>Work Object</dt><dd>{html.escape(work_object)}</dd>
    <dt>Source of truth</dt><dd>{html.escape(source)}</dd>
    <dt>Record</dt><dd>{html.escape(rel)}</dd>
    <dt>Lifecycle owners ({len(owner_names)})</dt><dd>{owners_display}</dd>
  </dl>
</section>"""
    return card, errors


def generate(ws_root: Path) -> dict:
    """Generate .work-studio/asset-workbench.html as a read-only projection."""
    out_path = ws_root / ".work-studio" / "asset-workbench.html"
    cards: list[str] = []
    all_errors: list[str] = []
    paths = asset_record_paths(ws_root)

    for path in paths:
        card, errors = _asset_card(path, ws_root)
        cards.append(card)
        all_errors.extend(f"{path.relative_to(ws_root).as_posix()}: {err}" for err in errors)

    owner_rows = "".join(
        f"<tr><td>{html.escape(frontier)}</td>"
        f"<td>{html.escape(FRONTIER_DESCRIPTIONS.get(frontier, 'no description recorded'))}</td>"
        f"<td><code>{html.escape(owner)}</code></td></tr>"
        for frontier, owner in sorted(FRONTIER_OWNERS.items())
    )
    error_html = ""
    if all_errors:
        items = "".join(f"<li>{html.escape(error)}</li>" for error in all_errors)
        error_html = f"<section class=\"gaps\"><h2>Validation Gaps</h2><ul>{items}</ul></section>"

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    html_doc = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Design Asset Workbench</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; max-width: 1040px; margin: 2rem auto; padding: 0 1rem; color: #1f2933; background: #fbfbfa; }}
h1 {{ font-size: 24px; margin: 0 0 6px; }}
h2 {{ font-size: 16px; margin: 0; }}
p {{ line-height: 1.45; }}
.meta {{ color: #667085; font-size: 13px; margin-bottom: 20px; }}
.notice {{ border: 1px solid #d8dee8; background: #fff; padding: 12px 14px; border-radius: 8px; font-size: 13px; margin-bottom: 18px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; }}
.asset {{ background: #fff; border: 1px solid #d8dee8; border-radius: 8px; padding: 14px; }}
.asset-head {{ display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }}
.summary {{ font-size: 13px; }}
.status {{ border-radius: 6px; padding: 3px 8px; font-size: 12px; }}
.ok {{ background: #ecfdf3; color: #027a48; }}
.bad {{ background: #fff1f3; color: #c01048; }}
dl {{ display: grid; grid-template-columns: 110px 1fr; gap: 6px 10px; font-size: 12px; }}
dt {{ color: #667085; }}
dd {{ margin: 0; overflow-wrap: anywhere; }}
table {{ width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #d8dee8; border-radius: 8px; overflow: hidden; font-size: 13px; }}
td, th {{ text-align: left; padding: 8px 10px; border-bottom: 1px solid #eaecf0; }}
code {{ font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 12px; }}
.gaps {{ margin-top: 18px; background: #fff; border: 1px solid #fecdd3; border-radius: 8px; padding: 14px; }}
</style></head>
<body>
<h1>Design Asset Workbench</h1>
<div class="meta">Generated {html.escape(generated_at)} from local asset records. Assets: {len(paths)}. Validation gaps: {len(all_errors)}.</div>
<div class="notice">Read-only projection. Edit asset truth in <code>.work-studio/design-assets/*.asset.md</code> through the appropriate Work Object route, then regenerate this page.</div>
<div class="grid">{''.join(cards)}</div>
{error_html}
<h2 style="margin-top: 24px;">Frontier Ownership</h2>
<table><thead><tr><th>Frontier</th><th>What it covers</th><th>Owner</th></tr></thead><tbody>{owner_rows}</tbody></table>
</body></html>"""

    out_path.write_text(html_doc, encoding="utf-8")
    return {
        "assets": len(paths),
        "gaps": len(all_errors),
        "out_path": out_path,
    }
