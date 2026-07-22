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
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = ROOT / "skills" / "core"
ADAPTERS_DIR = ROOT / "adapters"
VERSION_FILE = ROOT / "VERSION"
PLATFORMS = ["codex", "claude-code", "github-copilot"]
SKILL_NAMESPACE = "alawas"
SHARED_REFERENCES = [
    "../WORKSPACE-DOCUMENTATION-CONTRACT.md",
    "MISSING-ARTIFACT-GAP.md",
    "AGREEMENT-LOOP.md",
    "SKILL-AWARE-GRILLING.md",
    "CAPABILITY-DEGRADATION.md",
    "CONSEQUENCE-AUTHORITY.md",
    "EVIDENCE-MODEL.md",
    "SHARED-PROTOCOL.md",
]
SHARED_PROTOCOL_FILE = ROOT / "references" / "SHARED-PROTOCOL.md"


def read_version() -> str:
    """Read the release version, pinned in the VERSION file.

    Read from a file (never derived from a clock or environment) so that
    regeneration is byte-for-byte deterministic.
    """
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text().strip()
    return "0.0.0"


def read_protocol_version() -> str:
    """Read the released Shared Protocol version from its canonical reference."""
    match = re.search(r"Protocol version: `([^`]+)`", SHARED_PROTOCOL_FILE.read_text())
    if not match:
        raise ValueError("Shared Protocol version declaration is missing")
    return match.group(1)


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

def extract_canonical_description(core_skill_dir):
    """Extract the description field from a canonical SKILL.md frontmatter.

    Handles double-quoted strings, folded block scalars (``description: >``),
    and plain inline values.
    """
    text = (core_skill_dir / "SKILL.md").read_text()
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"No frontmatter found in {core_skill_dir}/SKILL.md")
    fm_text = parts[1]

    lines = fm_text.split("\n")
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("description:"):
            continue

        rest = stripped[len("description:"):].strip()

        # Double-quoted string
        if rest.startswith('"') and rest.endswith('"'):
            return rest[1:-1]

        # Block scalar: description: > or description: |
        if rest in (">", "|"):
            desc_lines = []
            key_indent = len(line) - len(line.lstrip())
            for j in range(i + 1, len(lines)):
                next_line = lines[j]
                next_stripped = next_line.strip()
                if not next_stripped or next_stripped.startswith("#"):
                    continue
                next_indent = len(next_line) - len(next_line.lstrip())
                if next_indent <= key_indent and ":" in next_stripped:
                    break
                desc_lines.append(next_stripped)
            return " ".join(desc_lines)

        # Plain inline value
        return rest

    raise ValueError(
        f"No description found in {core_skill_dir}/SKILL.md frontmatter")


def generate_frontmatter(core_skill_dir, overlay):
    """Generate platform-specific YAML frontmatter.

    Extracts the description from the canonical SKILL.md frontmatter — the
    single source of truth (Decision 87, Session 11).
    """
    description = extract_canonical_description(core_skill_dir)
    short_desc = " ".join(description.split())

    fm_add = overlay.get("frontmatter", {}).get("add", {})
    skill_name = core_skill_dir.name

    lines = ["---"]
    lines.append(f"name: {adapter_skill_name(skill_name)}")
    # JSON strings are valid quoted YAML scalars. Keeping the generated value
    # on one line avoids indentation-sensitive folded-block failures in skill
    # loaders while preserving quotes and Unicode deterministically.
    lines.append(f"description: {json.dumps(short_desc, ensure_ascii=False)}")
    for k, v in sorted(fm_add.items()):
        lines.append(f"{k}: {v}")
    lines.append("---")

    return "\n".join(lines) + "\n"


# ── Platform adapter section ─────────────────────────────────────────────────

def required_capabilities(core_skill_dir):
    """Return capabilities declared by one core skill, preserving first use order."""
    body = extract_body(core_skill_dir / "SKILL.md")
    try:
        section = body.split("## Required capabilities", 1)[1].split("\n## ", 1)[0]
    except IndexError as exc:
        raise ValueError(
            f"Missing Required capabilities section: {core_skill_dir / 'SKILL.md'}"
        ) from exc

    declared = []
    for line in section.splitlines():
        if not line.startswith("- "):
            continue
        declaration = line.split("—", 1)[0]
        for capability in re.findall(r"`([^`]+)`", declaration):
            if capability not in declared:
                declared.append(capability)
    if not declared:
        raise ValueError(f"No required capabilities declared: {core_skill_dir.name}")
    return declared


def generate_adapter_section(overlay, required):
    """Generate only invocation-relevant platform wiring for one skill."""

    lines = []
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Platform Adapter")
    lines.append("")
    lines.append("Invocation-relevant wiring only; installation and maintainer guidance live outside this file.")
    lines.append("")

    if overlay["platform"] == "codex":
        # Pin-resolution paragraph emitted for Codex only. Assumption: Claude
        # Code and GitHub Copilot skill loaders natively prefer project-pinned
        # over global without explicit prose instruction. UNVERIFIED — see
        # Decision 85 (Session 11). Verify per-platform before adding or
        # permanently omitting.
        lines.append("### Runtime pin resolution")
        lines.append("")
        lines.append("Codex can discover both user and repository skills with the same name.")
        lines.append("Before applying this skill, search upward from the current directory for")
        lines.append("`.work-studio/adapter.codex.lock`, stopping at the repository or filesystem")
        lines.append("boundary. Read its `dest` value and")
        lines.append("resolve `<dest>/<this-skill-name>/SKILL.md`. When that path differs from")
        lines.append("the currently loaded copy, **load and follow the pinned copy** before")
        lines.append("continuing. A matching legacy `adapter.lock` remains valid during migration.")
        lines.append("If the pinned file is unavailable, report the broken pin and")
        lines.append("stop instead of silently falling back to the global copy.")
        lines.append("")

    # Required capability mappings only.
    mappings = overlay.get("capability_mappings", {})
    caps = overlay.get("capabilities", {})
    lines.append("### Required capability mappings")
    lines.append("")
    lines.append("| Abstract capability | Platform tool | Classification |")
    lines.append("|---------------------|---------------|----------------|")
    for cap in required:
        if cap not in caps:
            raise ValueError(f"{overlay['platform']}: unclassified required capability: {cap}")
        tool = mappings.get(cap, "—")
        lines.append(f"| `{cap}` | `{tool}` | {caps[cap]} |")
    lines.append("")

    # Degradation behavior only for non-native capabilities this skill requires.
    non_native = {cap: caps[cap] for cap in required if caps[cap] != "native"}
    if non_native:
        lines.append("### Capability Degradation")
        lines.append("")
        lines.append("Apply `references/CAPABILITY-DEGRADATION.md`. Per-capability")
        lines.append("classifications and notes below.")
        lines.append("")

        for cap in non_native:
            classification = non_native[cap]
            tool = mappings.get(cap, "—")
            # Find matching declared limitation for the description
            desc = ""
            for lim in overlay.get("declared_limitations", []):
                if lim.get("capability") == cap:
                    desc = lim.get("description", "")
                    break
            lines.append(f"#### `{cap}` ({classification})")
            lines.append("")
            if tool and tool != "—":
                lines.append(f"- **Best-effort tool**: `{tool}`")
            if classification == "manual-fallback":
                lines.append("- **Behavior**: Pause and give one concrete manual instruction.")
                lines.append("- **Record**: Append History entry noting the capability gap, the")
                lines.append("  manual action taken, and what remains unverified.")
            elif classification == "unsupported":
                lines.append("- **Behavior**: Stop the affected path. Do not attempt or substitute.")
                lines.append("- **Record**: Note the platform limitation in the Work Object body.")
            if desc:
                lines.append(f"- **Note**: {desc}")
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


# ── Authority block validation ────────────────────────────────────────────────

# Skills that describe gated actions and MUST have inline authority blocks
# referencing CONSEQUENCE-AUTHORITY.md at their action points.
# Per Decision 57 (Grilling Session 8): authority checks must be inlined at
# the exact point where an irreversible or gated action is described.
AUTHORITY_GATED_SKILLS = {
    "conduct-work-object",
    "deploy-with-recovery",
    "implement-bounded-change",
    "verify-release-evidence",
    "review-outcome-and-adapt",
    "diagnose-production-incident",
    "maintain-working-method",
    "govern-scorecards",
}


def validate_authority_blocks():
    """Check that every gated skill has an inline authority block.

    Returns list of (skill_name, error_message) for each missing block.
    An authority block is identified by the pattern:
        **Authority gate:** ... references/CONSEQUENCE-AUTHORITY.md
    """
    errors = []
    for skill_dir in sorted(CORE_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_name = skill_dir.name
        if skill_name not in AUTHORITY_GATED_SKILLS:
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            errors.append((skill_name, "SKILL.md not found"))
            continue
        body = skill_file.read_text()
        if "**Authority gate:**" not in body:
            errors.append((skill_name, "missing inline authority gate block"))
        elif "CONSEQUENCE-AUTHORITY.md" not in body:
            errors.append((skill_name,
                          "authority gate present but does not reference CONSEQUENCE-AUTHORITY.md"))
    return errors


def validate_capability_classifications():
    """Check that every capability classified on any platform is classified on all platforms.

    Per Decision 84 (Session 11): prevents latent cross-platform gaps where a
    capability is declared in one overlay but silently missing from another.

    Returns list of (capability, platform, error_message) for each gap.
    """
    errors = []
    all_caps = {}  # {capability_name: {platform: classification}}

    for platform in PLATFORMS:
        overlay_file = ADAPTERS_DIR / platform / "overlay.yaml"
        if not overlay_file.exists():
            errors.append(("—", platform, "overlay.yaml not found"))
            continue
        overlay = parse_yaml(overlay_file.read_text())
        caps = overlay.get("capabilities", {})
        for cap in caps:
            all_caps.setdefault(cap, {})[platform] = caps[cap]

    for cap, platforms in sorted(all_caps.items()):
        for platform in PLATFORMS:
            if platform not in platforms:
                errors.append(
                    (cap, platform,
                     f"classified on {sorted(platforms.keys())} but missing from {platform} overlay")
                )

    return errors


# ── Generation ────────────────────────────────────────────────────────────────

def adapter_skill_name(core_skill_name):
    """Return the public, collision-safe adapter name for a core skill."""
    return f"{SKILL_NAMESPACE}-{core_skill_name}"


def namespace_skill_references(body):
    """Rewrite only backticked Work Studio skill references for adapters."""
    for skill_dir in sorted(CORE_DIR.iterdir(), key=lambda item: len(item.name), reverse=True):
        if skill_dir.is_dir():
            body = body.replace(
                f"`{skill_dir.name}`", f"`{adapter_skill_name(skill_dir.name)}`")
    return body


def build_skill_output(core_skill_dir, overlay):
    """Build the exact adapter SKILL.md text for a core skill + overlay.

    Single source of truth for both generation and drift checking, so the two
    paths can never diverge.
    """
    body = namespace_skill_references(extract_body(core_skill_dir / "SKILL.md"))
    frontmatter = generate_frontmatter(core_skill_dir, overlay)
    adapter_section = generate_adapter_section(
        overlay, required_capabilities(core_skill_dir))
    output = frontmatter + body.rstrip("\n") + adapter_section
    # Ensure exactly one trailing newline
    return output.rstrip("\n") + "\n"


def generate_skill(core_skill_dir, overlay, output_dir):
    """Generate one adapter skill from core + overlay."""
    core_file = core_skill_dir / "SKILL.md"
    skill_name = core_skill_dir.name
    output_skill_name = adapter_skill_name(skill_name)

    if not core_file.exists():
        print(f"  SKIP {skill_name}: core file not found at {core_file}")
        return None

    output = build_skill_output(core_skill_dir, overlay)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "SKILL.md"
    output_file.write_text(output)

    checksum = hashlib.sha256(output.encode()).hexdigest()
    return {
        "name": output_skill_name,
        "path": str(output_file.relative_to(ROOT)),
        "sha256": checksum,
    }


def build_reference_entries(skill_name, output_dir, core_skill_dir=None, write=False):
    """Include shared references that the skill body actually mentions.

    Scans the canonical skill body for each shared reference filename and
    only copies files the skill explicitly references (Decision 88, Session 11).
    When core_skill_dir is None (legacy path), includes all references.
    """
    entries = []
    reference_dir = output_dir / "references"

    if core_skill_dir is not None:
        body = extract_body(core_skill_dir / "SKILL.md")
        active_refs = [f for f in SHARED_REFERENCES if Path(f).name in body]
    else:
        active_refs = SHARED_REFERENCES

    if write:
        if active_refs:
            reference_dir.mkdir(parents=True, exist_ok=True)
            # Remove stale reference files no longer mentioned by this skill
            active_names = {Path(f).name for f in active_refs}
            for existing in reference_dir.iterdir():
                if existing.is_file() and existing.name not in active_names:
                    existing.unlink()
        elif reference_dir.exists():
            shutil.rmtree(reference_dir)
    for filename in active_refs:
        source = ROOT / "references" / filename
        destination = reference_dir / Path(filename).name
        content = source.read_bytes()
        if write:
            shutil.copyfile(source, destination)
        entries.append({
            "name": f"{skill_name}/references/{filename}",
            "path": str(destination.relative_to(ROOT)),
            "sha256": hashlib.sha256(content).hexdigest(),
        })
    return entries


def generate_platform(platform_name):
    """Generate all adapter skills for one platform."""
    overlay_file = ADAPTERS_DIR / platform_name / "overlay.yaml"

    if not overlay_file.exists():
        print(f"SKIP {platform_name}: overlay not found")
        return []

    overlay_text = overlay_file.read_text()
    overlay = parse_yaml(overlay_text)

    output_base = ADAPTERS_DIR / platform_name / "skills"
    expected_dirs = {adapter_skill_name(path.name) for path in CORE_DIR.iterdir()
                     if path.is_dir()}
    if output_base.exists():
        for child in output_base.iterdir():
            if child.is_dir() and child.name not in expected_dirs:
                shutil.rmtree(child)
    manifest_entries = []

    for skill_dir in sorted(CORE_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        output_skill_name = adapter_skill_name(skill_dir.name)
        output_dir = output_base / output_skill_name
        entry = generate_skill(skill_dir, overlay, output_dir)
        if entry:
            manifest_entries.append(entry)
            print(f"  Generated: {entry['path']} ({entry['sha256'][:12]}...)")
            manifest_entries.extend(
                build_reference_entries(output_skill_name, output_dir, core_skill_dir=skill_dir, write=True))

    return manifest_entries


# ── Manifest ──────────────────────────────────────────────────────────────────

def build_manifest(platform_name, entries):
    """Build the manifest dict for a platform. Deterministic (no timestamps)."""
    return {
        "platform": platform_name,
        "version": read_version(),
        "protocol_version": read_protocol_version(),
        "generated_by": "tools/generate-adapters.py",
        "files": entries,
    }


def write_manifest(platform_name, entries):
    """Write per-platform manifest.json with checksums."""
    manifest_dir = ADAPTERS_DIR / platform_name
    manifest_dir.mkdir(parents=True, exist_ok=True)

    manifest = build_manifest(platform_name, entries)
    manifest_path = manifest_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"  Manifest: {manifest_path.relative_to(ROOT)}")


def build_checksums(platform_name, entries):
    """Build SHA256SUMS text: `<sha256>  <path-relative-to-adapter-dir>`.

    Paths are relative to `adapters/<platform>/` so the installer can `cd`
    into the adapter directory and run `shasum -a 256 -c SHA256SUMS` with no
    other tooling. Sorted by path for deterministic output.
    """
    adapter_dir = ADAPTERS_DIR / platform_name
    rows = []
    for entry in entries:
        rel = Path(entry["path"]).relative_to(Path("adapters") / platform_name)
        rows.append((str(rel), entry["sha256"]))
    rows.sort()
    return "".join(f"{sha}  {rel}\n" for rel, sha in rows)


def write_checksums(platform_name, entries):
    """Write per-platform SHA256SUMS for dependency-free runtime verification."""
    manifest_dir = ADAPTERS_DIR / platform_name
    manifest_dir.mkdir(parents=True, exist_ok=True)
    sums_path = manifest_dir / "SHA256SUMS"
    sums_path.write_text(build_checksums(platform_name, entries))
    print(f"  Checksums: {sums_path.relative_to(ROOT)}")


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
    expected_entries = []

    for skill_dir in sorted(CORE_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_name = skill_dir.name
        output_skill_name = adapter_skill_name(skill_name)
        output_file = output_base / output_skill_name / "SKILL.md"

        expected = build_skill_output(skill_dir, overlay)

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

        expected_entries.append({
            "name": output_skill_name,
            "path": str(output_file.relative_to(ROOT)),
            "sha256": hashlib.sha256(expected.encode()).hexdigest(),
        })

        for entry in build_reference_entries(output_skill_name, output_file.parent, core_skill_dir=skill_dir):
            reference_file = ROOT / entry["path"]
            if not reference_file.exists():
                print(f"  MISSING: {reference_file.relative_to(ROOT)}")
                all_clean = False
            elif hashlib.sha256(reference_file.read_bytes()).hexdigest() != entry["sha256"]:
                print(f"  DRIFT: {reference_file.relative_to(ROOT)}")
                all_clean = False
            expected_entries.append(entry)

    # Check manifest
    manifest_path = ADAPTERS_DIR / platform_name / "manifest.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text())
            if manifest != build_manifest(platform_name, expected_entries):
                print(f"  MANIFEST DRIFT: {manifest_path.relative_to(ROOT)}")
                all_clean = False
            else:
                print(f"  MANIFEST OK: {manifest_path.relative_to(ROOT)}")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  MANIFEST ERROR: {manifest_path.relative_to(ROOT)}: {e}")
            all_clean = False
    else:
        print(f"  MANIFEST MISSING: {manifest_path.relative_to(ROOT)}")
        all_clean = False

    # Check SHA256SUMS
    sums_path = ADAPTERS_DIR / platform_name / "SHA256SUMS"
    expected_sums = build_checksums(platform_name, expected_entries)
    if not sums_path.exists():
        print(f"  CHECKSUMS MISSING: {sums_path.relative_to(ROOT)}")
        all_clean = False
    elif sums_path.read_text() != expected_sums:
        print(f"  CHECKSUMS DRIFT: {sums_path.relative_to(ROOT)}")
        all_clean = False
    else:
        print(f"  CHECKSUMS OK: {sums_path.relative_to(ROOT)}")

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
        # Validate authority blocks in core skills
        auth_errors = validate_authority_blocks()
        if auth_errors:
            print("\n[authority-blocks]")
            for skill, err in auth_errors:
                print(f"  FAIL: {skill}: {err}")
            all_clean = False
        else:
            print("\n[authority-blocks]")
            print("  OK: all gated skills have inline authority blocks")
        # Validate symmetric capability classifications across overlays
        cap_errors = validate_capability_classifications()
        if cap_errors:
            print("\n[capability-classifications]")
            for cap, platform, err in cap_errors:
                print(f"  FAIL: {cap}: {platform}: {err}")
            all_clean = False
        else:
            print("\n[capability-classifications]")
            print("  OK: all capabilities classified on all platforms")
        if all_clean:
            print("\nAll generated files match. No drift detected.")
            sys.exit(0)
        else:
            print("\nDRIFT DETECTED. Run 'python3 tools/generate-adapters.py' to regenerate.")
            sys.exit(1)
    else:
        # Validate authority blocks before generating
        auth_errors = validate_authority_blocks()
        if auth_errors:
            print("Authority block validation failed:")
            for skill, err in auth_errors:
                print(f"  FAIL: {skill}: {err}")
            print("Add inline authority gate blocks before regenerating.")
            sys.exit(1)
        # Validate symmetric capability classifications before generating
        cap_errors = validate_capability_classifications()
        if cap_errors:
            print("Capability classification validation failed (Decision 84):")
            for cap, platform, err in cap_errors:
                print(f"  FAIL: {cap}: {platform}: {err}")
            print("Classify every capability on all three platforms before regenerating.")
            sys.exit(1)
        print("Generating adapters...")
        for platform in PLATFORMS:
            print(f"\n[{platform}]")
            entries = generate_platform(platform)
            if entries:
                write_manifest(platform, entries)
                write_checksums(platform, entries)
        print("\nDone. Run 'python3 tools/generate-adapters.py --check' to verify.")


if __name__ == "__main__":
    main()
