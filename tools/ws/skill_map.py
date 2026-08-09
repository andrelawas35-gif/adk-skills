"""Skill map generation for Work Studio.

One CLI command:
    - ``ws skill-map build`` — Generate ``work-studio/skill-map.yaml`` from
      ``skills/core/*/SKILL.md``.

The map is a generated index, never hand-authored. It projects three fields
from each core skill's prose contract:

    - ``responsibility``         — frontmatter ``description``
    - ``non_goals``              — the "does not" bullets from
                                   ``## Boundaries and non-goals``
    - ``requires_capabilities``  — the backticked capability identifiers from
                                   ``## Required capabilities``

Extraction is strict, matching ``required_capabilities()`` in
``tools/generate-adapters.py``: a missing section, a missing "does not" region,
or an empty list raises instead of being silently omitted. Capability
identifiers are the joinable keys already used by ``adapters/*/overlay.yaml``;
the map restates no controlled vocabulary.

The generated file carries no timestamp so regeneration is byte-identical when
no contract changed (success criterion: regenerating produces no diff).
"""

import argparse
import importlib.util
import json
import sys
from pathlib import Path

SKILL_MAP_FILENAME = "skill-map.yaml"
CORE_SKILLS_DIRNAME = "core"
MARKER_REQUIRED_SECTION = "## Boundaries and non-goals"
MARKER_DOES_NOT = "this skill does not"
MARKER_CAPABILITIES = "## Required capabilities"


def _find_work_studio_root() -> Path:
    """Walk upward from CWD to find .work-studio/ directory."""
    cwd = Path.cwd().resolve()
    for parent in [cwd] + list(cwd.parents):
        if (parent / ".work-studio").is_dir():
            return parent
    raise FileNotFoundError(
        ".work-studio/ not found in current directory or any parent. "
        "Run 'ws init' first to bootstrap the workspace."
    )


def _load_adapter_generator():
    """Load tools/generate-adapters.py once for reuse of its strict extractors.

    The file is hyphenated (``generate-adapters.py``) so it cannot be imported
    by module name; importlib loads it without running ``main()`` (guarded).
    """
    root = _find_work_studio_root()
    spec = importlib.util.spec_from_file_location(
        "generate_adapters", root / "tools" / "generate-adapters.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _body_after_frontmatter(skill_file: Path) -> str:
    """Return the Markdown body after the YAML frontmatter."""
    text = skill_file.read_text()
    parts = text.split("---", 2)
    return parts[2].lstrip("\n") if len(parts) >= 3 else text


def extract_responsibility(core_skill_dir: Path) -> str:
    """Return the frontmatter description (single source of truth)."""
    gen = _load_adapter_generator()
    return gen.extract_canonical_description(core_skill_dir)


def extract_requires_capabilities(core_skill_dir: Path) -> list:
    """Return the declared capability identifiers in first-use order."""
    gen = _load_adapter_generator()
    return gen.required_capabilities(core_skill_dir)


def extract_non_goals(core_skill_dir: Path) -> list:
    """Return the 'does not' bullets from ## Boundaries and non-goals.

    Strict: raises on a missing section, a missing "does not" region, or an
    empty list — the same failure contract as ``required_capabilities()``.
    Bullet continuations (indented wrapped lines) are folded into the bullet.
    """
    skill_file = core_skill_dir / "SKILL.md"
    body = _body_after_frontmatter(skill_file)

    if MARKER_REQUIRED_SECTION not in body:
        raise ValueError(
            f"Missing Boundaries and non-goals section: {skill_file}"
        )

    section = body.split(MARKER_REQUIRED_SECTION, 1)[1].split("\n## ", 1)[0]
    lines = section.splitlines()

    marker_idx = None
    for i, line in enumerate(lines):
        candidate = line.strip().lstrip("*").rstrip("*").rstrip(":").strip().lower()
        if candidate == MARKER_DOES_NOT:
            marker_idx = i
            break

    if marker_idx is None:
        raise ValueError(
            f"No 'does not' region in Boundaries section: {core_skill_dir.name}"
        )

    non_goals = []
    current = None
    for line in lines[marker_idx + 1:]:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("## "):
            break
        # A new bullet or a sibling marker ends the current entry.
        if stripped.startswith("- "):
            if current is not None:
                non_goals.append(current)
            current = stripped[2:].strip()
            continue
        # Indented continuation of the current bullet.
        if current is not None and line.startswith(" ") and not stripped.startswith("**"):
            current = current + " " + stripped.strip()
            continue
        # Any other non-bullet line (e.g. a second "does" marker) ends the region.
        if current is not None:
            break

    if current is not None:
        non_goals.append(current)

    if not non_goals:
        raise ValueError(f"No non-goal bullets declared: {core_skill_dir.name}")

    return non_goals


def _json_quote(value: str) -> str:
    """Emit a JSON-quoted YAML scalar, matching the adapter generator."""
    return json.dumps(value, ensure_ascii=False)


def _render_skill_map(entries) -> str:
    """Render the deterministic skill-map.yaml document.

    ``entries`` is a list of dicts with keys name, responsibility,
    non_goals, requires_capabilities — already sorted and complete.
    """
    lines = []
    lines.append("# Skill Map — generated index over skills/core/*/SKILL.md")
    lines.append("# Generated by: ws skill-map build")
    lines.append("# Do not hand-edit. Prose contracts stay authoritative.")
    lines.append("")
    lines.append("schema_version: 1")
    lines.append("")
    lines.append("skills:")
    for entry in entries:
        lines.append(f"  - name: {entry['name']}")
        lines.append(
            f"    responsibility: {_json_quote(entry['responsibility'])}"
        )
        lines.append("    non_goals:")
        for bullet in entry["non_goals"]:
            lines.append(f"      - {_json_quote(bullet)}")
        lines.append("    requires_capabilities:")
        for cap in entry["requires_capabilities"]:
            lines.append(f"      - {cap}")
        lines.append("")
    return "\n".join(lines) + "\n"


def build_skill_map(ws_root: Path) -> tuple:
    """Generate skill-map.yaml for every core skill.

    Returns ``(written_entries, errors)`` where ``errors`` is a list of
    ``(skill_name, message)`` for skills that failed strict extraction.
    The file is written with the successfully parsed entries; any failure is
    reported loudly by the caller (non-zero exit), never silently omitted.
    """
    core_dir = ws_root / "skills" / CORE_SKILLS_DIRNAME
    skill_dirs = sorted(
        d for d in core_dir.iterdir() if d.is_dir()
    )

    entries = []
    errors = []
    for skill_dir in skill_dirs:
        name = skill_dir.name
        try:
            entries.append({
                "name": name,
                "responsibility": extract_responsibility(skill_dir),
                "non_goals": extract_non_goals(skill_dir),
                "requires_capabilities": extract_requires_capabilities(skill_dir),
            })
        except (ValueError, OSError) as exc:
            errors.append((name, str(exc)))

    if entries:
        out_dir = ws_root / "work-studio"
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / SKILL_MAP_FILENAME).write_text(
            _render_skill_map(entries)
        )

    return entries, errors


def cmd_skill_map_build(args: argparse.Namespace) -> int:
    """Build work-studio/skill-map.yaml; exit non-zero on any failure."""
    try:
        ws_root = _find_work_studio_root()
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    entries, errors = build_skill_map(ws_root)

    out_file = ws_root / "work-studio" / SKILL_MAP_FILENAME
    print(f"Generated {out_file} ({len(entries)} skills)")

    if errors:
        for name, message in errors:
            print(f"FAIL: {name}: {message}", file=sys.stderr)
        print(
            f"Error: {len(errors)} skill(s) failed strict extraction; "
            "repair or exclude them before the map is complete.",
            file=sys.stderr,
        )
        return 1

    return 0
