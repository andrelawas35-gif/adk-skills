#!/usr/bin/env python3
"""Generate platform adapter SKILL.md files from canonical core + platform overlays.

Dependency-free — uses only Python 3 standard library.

Usage:
    python3 tools/generate-adapters.py              # generate all adapters
    python3 tools/generate-adapters.py --check      # verify generated files match

Architecture:
    skills/core/<skill>/SKILL.md  →  canonical source (the portable core)
    adapters/<platform>/overlay.yaml  →  platform-specific metadata + mappings
    adapters/<platform>/skills/<skill>/SKILL.md  →  generated adapter
    adapters/<platform>/manifest.json  →  checksums (generated)

The generator:
    1. Copies the core skill body unchanged (decision logic, authority rules, schema)
    2. Replaces the YAML frontmatter with platform-specific metadata
    3. Appends a Platform Adapter section with tool mappings + declared limitations
    4. Produces byte-for-byte identical output on regeneration
"""

import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = ROOT / "skills" / "core"
ADAPTERS_DIR = ROOT / "adapters"
PLATFORMS = ["codex", "claude-code", "github-copilot"]


# ── Minimal YAML parser ──────────────────────────────────────────────────────

def parse_yaml(text: str) -> dict:
    """Parse a minimal YAML subset: mappings, sequences, scalars, comments.

    Only handles the overlay file format. Not a general-purpose YAML parser.
    """
    lines = text.split("\n")
    root = {}
    # Stack of (indent, container) — container is a dict or list.
    # stack[0] is always (0, root).
    stack = [(0, root)]

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip empty lines and comments
        if not stripped or stripped.startswith("#"):
            i += 1
            continue

        indent = len(line) - len(line.lstrip())

        # Pop entries deeper than current indent, but never pop the root
        while len(stack) > 1 and stack[-1][0] >= indent:
            stack.pop()

        container = stack[-1][1]

        # Sequence item
        if stripped.startswith("- "):
            raw_value = stripped[2:].strip()

            # Check for inline mapping: "- key: value" or "- key:"
            if ":" in raw_value and not (raw_value.startswith('"') or raw_value.startswith("'")):
                k, _, v = raw_value.partition(":")
                k = k.strip()
                v = v.strip()
                inline_map = {k: _parse_scalar(v) if v else {}}

                if isinstance(container, list):
                    container.append(inline_map)
                # Push so subsequent lines at higher indent go into this map.
                # The indent of the "- " line is the base indent for this mapping.
                stack.append((indent, inline_map))
            else:
                value = _parse_scalar(raw_value)
                if isinstance(container, list):
                    container.append(value)
            i += 1
            continue

        # Mapping key: value
        if ":" in stripped:
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = val.strip()

            if val == "":
                # Nested block: peek ahead to determine list vs dict
                is_list = False
                for j in range(i + 1, len(lines)):
                    nline = lines[j]
                    nstripped = nline.strip()
                    if nstripped and not nstripped.startswith("#"):
                        if nstripped.startswith("- "):
                            is_list = True
                        break

                if is_list:
                    container[key] = []
                    stack.append((indent, container[key]))
                else:
                    container[key] = {}
                    stack.append((indent, container[key]))
            else:
                container[key] = _parse_scalar(val)

        i += 1

    return root


def _parse_scalar(val: str):
    """Parse a scalar YAML value."""
    if not val:
        return val
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        return val[1:-1]
    if val.lower() in ("true", "yes", "on"):
        return True
    if val.lower() in ("false", "no", "off"):
        return False
    if val.lower() in ("null", "none", "~"):
        return None
    try:
        return int(val)
    except ValueError:
        pass
    try:
        return float(val)
    except ValueError:
        pass
    return val


# ── Frontmatter generation ───────────────────────────────────────────────────

def generate_frontmatter(core_skill_name, overlay):
    """Generate platform-specific YAML frontmatter."""
    platform_label = overlay.get("platform_label", overlay["platform"])
    platform_name = overlay["platform"]

    descriptions = {
        "conduct-work-object": (
            f"Detect, create, activate, resume, update, and close Work Objects — "
            f"the canonical continuity surface of Andrelawas Work Studio. "
            f"Use when the user asks to start or resume work, check what's active, "
            f"move work forward, record a decision, or close something out. "
            f"This skill owns the Work Object lifecycle and routes to specialists "
            f"for domain-specific work."
        ),
        "pressure-test-decision": (
            f"Resume an active Work Object, identify its highest-leverage unresolved "
            f"decision, recommend an answer before asking exactly one question, and "
            f"safely persist the confirmed decision. Use when the user says "
            f'"help me decide," "pressure-test this," "grill this," '
            f'"what should I do about X," or when conduct-work-object routes a '
            f"Work Object in the Decide state. Composes grilling and domain modeling. "
            f"Never performs implementation."
        ),
    }

    description = descriptions.get(core_skill_name, f"{core_skill_name} — {platform_label} adapter")
    short_desc = " ".join(description.split())

    fm_add = overlay.get("frontmatter", {}).get("add", {})

    lines = ["---"]
    lines.append(f"name: {core_skill_name}")
    lines.append(f"description: >")
    # Wrap description at ~80 chars for YAML folded block
    words = short_desc.split()
    current = "  "
    for w in words:
        if len(current) + len(w) + 1 > 80:
            lines.append(current.rstrip())
            current = "  " + w
        else:
            current += " " + w
    lines.append(current.rstrip())
    for k, v in sorted(fm_add.items()):
        lines.append(f"{k}: {v}")
    lines.append("---")

    return "\n".join(lines) + "\n"


# ── Platform adapter section ─────────────────────────────────────────────────

def generate_adapter_section(overlay):
    """Generate the Platform Adapter appendix."""
    platform_label = overlay.get("platform_label", overlay["platform"])
    install_dir = overlay.get("skill_install_dir", "N/A")

    lines = []
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Platform Adapter")
    lines.append("")
    lines.append(f"This skill is adapted for **{platform_label}** from the canonical core.")
    lines.append("Core decision logic, authority boundaries, and schema semantics are")
    lines.append("preserved unchanged. This section documents only platform-specific")
    lines.append("wiring and declared limitations.")
    lines.append("")
    lines.append(f"**Installation**: Copy this skill to `{install_dir}`.")
    lines.append("")

    # Discovery
    discovery = overlay.get("discovery", {})
    lines.append("### Discovery")
    lines.append("")
    lines.append(f"- Config path: `{discovery.get('config_path', '.work-studio/config.md')}`")
    for marker in discovery.get("boundary_markers", []):
        lines.append(f"- Boundary marker: `{marker}`")
    for condition in discovery.get("stop_conditions", []):
        lines.append(f"- Stop condition: {condition}")
    lines.append("")

    # Capability mappings
    mappings = overlay.get("capability_mappings", {})
    caps = overlay.get("capabilities", {})
    if mappings or caps:
        lines.append("### Capability Mappings")
        lines.append("")
        lines.append("| Abstract capability | Platform tool | Classification |")
        lines.append("|---------------------|---------------|----------------|")
        all_keys = sorted(set(list(mappings.keys()) + list(caps.keys())))
        for cap in all_keys:
            tool = mappings.get(cap, "—")
            classification = caps.get(cap, "—")
            lines.append(f"| `{cap}` | `{tool}` | {classification} |")
        lines.append("")

    # Limitations
    limitations = overlay.get("declared_limitations", [])
    if limitations:
        lines.append("### Declared Limitations")
        lines.append("")
        for lim in limitations:
            lines.append(f"- **{lim.get('capability', 'unknown')}**")
            lines.append(f"  ({lim.get('classification', 'manual-fallback')}):")
            lines.append(f"  {lim.get('description', 'No details provided.')}")
        lines.append("")

    lines.append("### Integrity")
    lines.append("")
    lines.append("This file is generated. Do not edit directly — edit the canonical core")
    lines.append(f"at `skills/core/<skill>/SKILL.md` or the overlay at")
    lines.append(f"`adapters/{overlay['platform']}/overlay.yaml`. Regenerate with")
    lines.append("`python3 tools/generate-adapters.py`.")
    lines.append("")

    return "\n".join(lines)


# ── Skill body extraction ────────────────────────────────────────────────────

def extract_body(filepath):
    """Extract the Markdown body after the YAML frontmatter.

    A SKILL.md file has:
        ---
        frontmatter
        ---
        body (everything after the second ---)
    """
    text = filepath.read_text()
    # Find the second ---
    parts = text.split("---", 2)
    if len(parts) >= 3:
        return parts[2].lstrip("\n")
    return text


# ── Generation ────────────────────────────────────────────────────────────────

def generate_skill(core_skill_dir, overlay, output_dir):
    """Generate one adapter skill from core + overlay."""
    core_file = core_skill_dir / "SKILL.md"
    skill_name = core_skill_dir.name

    if not core_file.exists():
        print(f"  SKIP {skill_name}: core file not found at {core_file}")
        return None

    body = extract_body(core_file)
    frontmatter = generate_frontmatter(skill_name, overlay)
    adapter_section = generate_adapter_section(overlay)

    output = frontmatter + body.rstrip("\n") + adapter_section
    # Ensure exactly one trailing newline
    output = output.rstrip("\n") + "\n"

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "SKILL.md"
    output_file.write_text(output)

    checksum = hashlib.sha256(output.encode()).hexdigest()
    return {
        "name": skill_name,
        "path": str(output_file.relative_to(ROOT)),
        "sha256": checksum,
    }


def generate_platform(platform_name):
    """Generate all adapter skills for one platform."""
    overlay_file = ADAPTERS_DIR / platform_name / "overlay.yaml"

    if not overlay_file.exists():
        print(f"SKIP {platform_name}: overlay not found")
        return []

    overlay_text = overlay_file.read_text()
    overlay = parse_yaml(overlay_text)

    output_base = ADAPTERS_DIR / platform_name / "skills"
    manifest_entries = []

    for skill_dir in sorted(CORE_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        output_dir = output_base / skill_dir.name
        entry = generate_skill(skill_dir, overlay, output_dir)
        if entry:
            manifest_entries.append(entry)
            print(f"  Generated: {entry['path']} ({entry['sha256'][:12]}...)")

    return manifest_entries


# ── Manifest ──────────────────────────────────────────────────────────────────

def write_manifest(platform_name, entries):
    """Write per-platform manifest.json with checksums."""
    manifest_dir = ADAPTERS_DIR / platform_name
    manifest_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "platform": platform_name,
        "generated_by": "tools/generate-adapters.py",
        "files": entries,
    }
    manifest_path = manifest_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"  Manifest: {manifest_path.relative_to(ROOT)}")


# ── Check mode ────────────────────────────────────────────────────────────────

def check_platform(platform_name):
    """Verify generated files match what would be regenerated. Returns True if clean."""
    overlay_file = ADAPTERS_DIR / platform_name / "overlay.yaml"
    if not overlay_file.exists():
        print(f"SKIP {platform_name}: overlay not found")
        return True

    overlay_text = overlay_file.read_text()
    overlay = parse_yaml(overlay_text)

    output_base = ADAPTERS_DIR / platform_name / "skills"
    all_clean = True

    for skill_dir in sorted(CORE_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_name = skill_dir.name
        output_dir = output_base / skill_name
        output_file = output_dir / "SKILL.md"

        # Generate expected content
        body = extract_body(skill_dir / "SKILL.md")
        frontmatter = generate_frontmatter(skill_name, overlay)
        adapter_section = generate_adapter_section(overlay)
        expected = frontmatter + body.rstrip("\n") + adapter_section
        expected = expected.rstrip("\n") + "\n"

        if not output_file.exists():
            print(f"  MISSING: {output_file.relative_to(ROOT)}")
            all_clean = False
            continue

        actual = output_file.read_text()
        if actual != expected:
            print(f"  DRIFT: {output_file.relative_to(ROOT)}")
            all_clean = False
        else:
            print(f"  OK: {output_file.relative_to(ROOT)}")

    # Check manifest
    manifest_path = ADAPTERS_DIR / platform_name / "manifest.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text())
            expected_entries = []
            for skill_dir in sorted(CORE_DIR.iterdir()):
                if not skill_dir.is_dir():
                    continue
                skill_name = skill_dir.name
                output_file = output_base / skill_name / "SKILL.md"
                if output_file.exists():
                    checksum = hashlib.sha256(output_file.read_bytes()).hexdigest()
                    expected_entries.append({
                        "name": skill_name,
                        "path": str(output_file.relative_to(ROOT)),
                        "sha256": checksum,
                    })
            if manifest.get("files") != expected_entries:
                print(f"  MANIFEST DRIFT: {manifest_path.relative_to(ROOT)}")
                all_clean = False
            else:
                print(f"  MANIFEST OK: {manifest_path.relative_to(ROOT)}")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  MANIFEST ERROR: {manifest_path.relative_to(ROOT)}: {e}")
            all_clean = False

    return all_clean


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if "--check" in sys.argv:
        print("Checking generated adapters...")
        all_clean = True
        for platform in PLATFORMS:
            print(f"\n[{platform}]")
            if not check_platform(platform):
                all_clean = False
        if all_clean:
            print("\nAll generated files match. No drift detected.")
            sys.exit(0)
        else:
            print("\nDRIFT DETECTED. Run 'python3 tools/generate-adapters.py' to regenerate.")
            sys.exit(1)
    else:
        print("Generating adapters...")
        for platform in PLATFORMS:
            print(f"\n[{platform}]")
            entries = generate_platform(platform)
            if entries:
                write_manifest(platform, entries)
        print("\nDone. Run 'python3 tools/generate-adapters.py --check' to verify.")


if __name__ == "__main__":
    main()
