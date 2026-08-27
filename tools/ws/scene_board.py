"""Read-only Scene Board generator (V0 tracer, WO 2026-08-23-001).

Reads Scene Work Objects (those with a '## Screenplay' section) and renders
them into .work-studio/scene-board.html. Same read-only projection pattern
as command_center.py — never writes to objects/ or any source file.
"""
import html
import re
from pathlib import Path


FIELDS = ["id", "title", "type", "state", "status", "consequence",
          "updated_at", "next_action"]

STATE_COLOR = {
    "notice": "#94a3b8", "explore": "#3b82f6", "design": "#8b5cf6",
    "build": "#f59e0b", "verify": "#14b8a6", "release": "#f97316",
    "observe": "#ec4899", "close": "#94a3b8",
}


def _parse_frontmatter(text: str):
    if not text.startswith("---"):
        return None, "no frontmatter"
    end = text.find("\n---", 3)
    if end == -1:
        return None, "unclosed frontmatter"
    result = {}
    for line in text[3:end].split("\n"):
        m = re.match(r"^([a-zA-Z_]+):\s*(.*)$", line.strip())
        if m:
            result[m.group(1)] = m.group(2).strip().strip('"')
    return result, None


def _extract_section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$", re.MULTILINE
    )
    m = pattern.search(text)
    if not m:
        return ""
    start = m.end()
    next_h2 = re.search(r"^## ", text[start:], re.MULTILINE)
    end = start + next_h2.start() if next_h2 else len(text)
    return text[start:end].strip()


def _extract_subsections(text: str, heading: str) -> list[tuple[str, str]]:
    section = _extract_section(text, heading)
    if not section:
        return []
    parts = re.split(r"^### (.+)$", section, flags=re.MULTILINE)
    results = []
    i = 1
    while i < len(parts) - 1:
        results.append((parts[i].strip(), parts[i + 1].strip()))
        i += 2
    return results


def _extract_table(text: str, heading: str) -> list[dict]:
    section = _extract_section(text, heading)
    if not section:
        return []
    lines = [l for l in section.split("\n") if l.strip().startswith("|")]
    if len(lines) < 3:
        return []
    headers = [h.strip() for h in lines[0].split("|")[1:-1]]
    rows = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))
    return rows


def _extract_thesis(text: str) -> dict:
    section = _extract_section(text, "Scene Thesis")
    if not section:
        return {}
    result = {}
    for line in section.split("\n"):
        # Accept both "**Key:** value" (colon inside the bold, the format SC030
        # uses) and "**Key**: value" (colon outside). A trailing colon on the
        # captured key is stripped so the label renders as "Key", not "Key:".
        # (Found by the focused regression test, WO 2026-08-23-001.)
        m = re.match(r"^-\s+\*\*(.+?)\*\*:?\s*(.+)$", line)
        if m:
            key = m.group(1).rstrip(":")
            result[key.lower()] = m.group(2)
    return result


def _scene_card_html(wo: dict, thesis: dict, layers: list,
                     beats: list) -> str:
    state = wo.get("state", "notice")
    color = STATE_COLOR.get(state, "#94a3b8")
    woid = html.escape(wo.get("id", "?"))
    title = html.escape(wo.get("title", "Untitled"))

    thesis_html = ""
    if thesis:
        items = "".join(
            f'<div class="thesis-item"><span class="thesis-key">'
            f'{html.escape(k)}</span> {html.escape(v)}</div>'
            for k, v in thesis.items()
        )
        thesis_html = f'<div class="thesis">{items}</div>'

    layers_html = ""
    if layers:
        tabs = []
        panels = []
        for i, (name, content) in enumerate(layers):
            active = " active" if i == 0 else ""
            tab_id = f"tab-{woid}-{i}"
            panel_id = f"panel-{woid}-{i}"
            tabs.append(
                f'<button class="layer-tab{active}" data-panel="{panel_id}" '
                f'id="{tab_id}">{html.escape(name)}</button>'
            )
            display = "block" if i == 0 else "none"
            panels.append(
                f'<div class="layer-panel" id="{panel_id}" '
                f'style="display:{display}">'
                f'{html.escape(content)}</div>'
            )
        layers_html = (
            f'<div class="layers"><div class="layer-tabs">{"".join(tabs)}'
            f'</div>{"".join(panels)}</div>'
        )

    beats_html = ""
    if beats:
        rows = []
        for b in beats:
            beat_num = html.escape(b.get("Beat", ""))
            screenplay = html.escape(b.get("Screenplay", ""))
            intent = html.escape(b.get("Director Intent", ""))
            perf = html.escape(b.get("Performance", ""))
            prod = html.escape(b.get("Production", ""))
            rows.append(
                f'<tr><td class="beat-num">{beat_num}</td>'
                f'<td>{screenplay}</td><td class="intent">{intent}</td>'
                f'<td class="perf">{perf}</td>'
                f'<td class="prod">{prod}</td></tr>'
            )
        beats_html = f"""<div class="beats">
<table>
<thead><tr><th>Beat</th><th>Screenplay</th><th>Director Intent</th>
<th>Performance</th><th>Production</th></tr></thead>
<tbody>{"".join(rows)}</tbody>
</table></div>"""

    return f"""<div class="scene-card">
<div class="scene-header">
  <span class="state-dot" style="background:{color}"></span>
  <span class="scene-id">{woid}</span>
  <span class="scene-title">{title}</span>
  <span class="scene-state">{html.escape(state)}</span>
</div>
{thesis_html}
{layers_html}
{beats_html}
</div>"""


def generate(ws_root: Path) -> dict:
    """Generate the Scene Board HTML. Returns summary dict."""
    objects_dir = ws_root / ".work-studio" / "objects"
    out_path = ws_root / ".work-studio" / "scene-board.html"

    scenes = []
    for f in sorted(objects_dir.glob("**/*.md")):
        text = f.read_text(encoding="utf-8")
        if "## Screenplay" not in text:
            continue
        wo, err = _parse_frontmatter(text)
        if err or not wo:
            continue
        thesis = _extract_thesis(text)
        layers = _extract_subsections(text, "Screenplay")
        beats = _extract_table(text, "Director Layer")
        scenes.append(_scene_card_html(wo, thesis, layers, beats))

    html_doc = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Scene Board</title>
<style>
body {{ font-family: -apple-system, sans-serif; max-width: 1100px;
       margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; background: #fff; }}
h1 {{ font-size: 20px; font-weight: 500; margin-bottom: 1.5rem; }}
.scene-card {{ border: 1px solid #e5e5e5; border-radius: 10px;
              padding: 16px 20px; margin-bottom: 16px; }}
.scene-header {{ display: flex; align-items: center; gap: 10px;
                margin-bottom: 12px; }}
.state-dot {{ width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }}
.scene-id {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
            font-size: 12px; color: #666; }}
.scene-title {{ font-size: 15px; font-weight: 500; flex: 1; }}
.scene-state {{ font-size: 11px; padding: 2px 8px; border-radius: 6px;
               background: #f3f4f6; color: #666; }}
.thesis {{ margin-bottom: 12px; padding: 10px 12px; background: #f9fafb;
          border-radius: 6px; }}
.thesis-item {{ font-size: 13px; margin-bottom: 4px; }}
.thesis-key {{ font-weight: 600; text-transform: capitalize; margin-right: 4px; }}
.layers {{ margin-bottom: 14px; }}
.layer-tabs {{ display: flex; gap: 0; border-bottom: 1px solid #e5e5e5;
              margin-bottom: 10px; }}
.layer-tab {{ font-size: 12px; padding: 6px 14px; border: none;
             background: none; cursor: pointer; color: #666;
             border-bottom: 2px solid transparent; }}
.layer-tab.active {{ color: #1a1a1a; border-bottom-color: #1a1a1a; }}
.layer-panel {{ font-size: 13px; line-height: 1.6; white-space: pre-wrap;
               padding: 0 4px; }}
.beats {{ overflow-x: auto; }}
.beats table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
.beats th {{ text-align: left; padding: 6px 8px; border-bottom: 2px solid #e5e5e5;
            font-weight: 500; font-size: 11px; color: #666;
            text-transform: uppercase; letter-spacing: 0.5px; }}
.beats td {{ padding: 8px; border-bottom: 1px solid #f3f4f6;
            vertical-align: top; line-height: 1.5; }}
.beat-num {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
            font-weight: 600; width: 32px; text-align: center; }}
.intent {{ color: #6d28d9; }}
.perf {{ color: #0369a1; font-style: italic; }}
.prod {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 11px; color: #666; }}
.empty {{ text-align: center; padding: 3rem; color: #666; font-size: 14px; }}
</style></head>
<body>
<h1>Scene Board</h1>
{
    ''.join(scenes) if scenes
    else '<div class="empty">No scenes found. Create a Work Object with a ## Screenplay section.</div>'
}
<script>
document.querySelectorAll('.layer-tab').forEach(function(tab) {{
  tab.addEventListener('click', function() {{
    var card = this.closest('.scene-card');
    card.querySelectorAll('.layer-tab').forEach(function(t) {{ t.classList.remove('active'); }});
    card.querySelectorAll('.layer-panel').forEach(function(p) {{ p.style.display = 'none'; }});
    this.classList.add('active');
    document.getElementById(this.dataset.panel).style.display = 'block';
  }});
}});
</script>
</body></html>"""

    out_path.write_text(html_doc, encoding="utf-8")
    return {"scenes": len(scenes), "out_path": out_path}
