#!/usr/bin/env python3
"""Verify kernel manifest path and boundary integrity.

Checks that every kernel entry declared in work-studio/kernel-manifest.yaml
exists at its declared path, respects repository boundary rules, and is
internally consistent. This is the first verifier — it checks path existence
and boundary integrity only, not content correctness.

Usage:
    python3 tools/verify-kernel.py           # Full check
    python3 tools/verify-kernel.py --paths   # Path existence only
    python3 tools/verify-kernel.py --boundary # Boundary rules only
    python3 tools/verify-kernel.py --quiet   # Exit code only (0 = pass)

Exit codes:
    0 — all checks passed
    1 — one or more checks failed
    2 — manifest is missing or unparseable
"""

from __future__ import annotations

import sys
import os
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "work-studio" / "kernel-manifest.yaml"
VERSION_PATH = ROOT / "VERSION"

# ── Minimal YAML parser (stdlib only, no PyYAML dependency) ──────────────────

def _coerce_value(value: str):
    """Coerce a string value to int, float, bool, or leave as str."""
    if value.lower() in ("true", "yes", "on"):
        return True
    if value.lower() in ("false", "no", "off"):
        return False
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def parse_simple_yaml(path: Path) -> dict | None:
    """Parse a simple YAML file into nested dicts/lists.

    Handles only the subset used by kernel-manifest.yaml: scalars,
    sequences (bare dashes), nested mappings, and block scalars (>).
    Does not handle anchors, aliases, tags, flow style, or multi-doc.
    """
    if not path.exists():
        return None

    with open(path) as f:
        lines = f.readlines()

    result = {}
    current_section = result
    # Each frame restores the context active before a nested mapping or a
    # dict-shaped list item was entered: (key, parent section, its indent,
    # the list that was active in the parent, if any). The parent list must
    # be restored on pop — not just the parent section — because parsing a
    # dict-shaped list item's own fields (e.g. `purpose: "..."` inside a
    # `- path: VERSION` entry) reassigns current_list to None or to a nested
    # sub-list, and popping back out must undo that so the next sibling
    # list item still appends to the right list.
    stack: list[tuple[str, dict, int, list | None]] = []
    current_key: str | None = None
    current_list: list | None = None
    block_scalar_key: str | None = None
    block_scalar_lines: list[str] = []
    block_scalar_indent: int = 0

    for line in lines:
        raw = line.rstrip("\n")
        if not raw or raw.strip().startswith("#"):
            if block_scalar_key is not None and raw.strip():
                block_scalar_lines.append(raw.strip())
            continue

        indent = len(line) - len(line.lstrip(" "))
        stripped = raw.strip()

        # Block scalar continuation: compare against the block scalar's own
        # key indent, not the enclosing mapping's stacked indent — the two
        # differ whenever the block scalar is nested (e.g. `description: >`
        # under `kernel:`), and using the wrong one swallows every following
        # line as continuation text.
        if block_scalar_key is not None:
            if indent > block_scalar_indent:
                block_scalar_lines.append(stripped)
                continue
            else:
                current_section[block_scalar_key] = " ".join(block_scalar_lines).strip()
                block_scalar_key = None
                block_scalar_lines = []

        # Pop stack for dedent
        while stack and indent <= stack[-1][2]:
            _, parent, _, parent_list = stack.pop()
            current_section = parent
            current_list = parent_list

        # Block scalar indicator (>)
        if stripped.endswith(": >") or ": >" in stripped:
            key = stripped.split(": >")[0].strip()
            block_scalar_key = key
            block_scalar_lines = []
            block_scalar_indent = indent
            continue

        # Key-value with colon
        if ": " in stripped or ":" == stripped[-1]:
            # List item (starts with -)
            if stripped.startswith("- "):
                item_body = stripped[2:]
                if ": " in item_body:
                    # Dict-shaped list item ("- path: VERSION"): starts a new
                    # mapping, appended to the enclosing list. Its own
                    # further fields (purpose:, required_for_bootstrap:, ...)
                    # arrive as ordinary deeper-indented key-value lines and
                    # attach to it because current_section now points at it.
                    item_key, item_value = item_body.split(": ", 1)
                    item_key = item_key.strip()
                    item_value = item_value.strip()
                    new_item: dict = {}
                    if current_list is not None:
                        current_list.append(new_item)
                    stack.append((item_key, current_section, indent, current_list))
                    current_section = new_item
                    if item_value == "":
                        new_sub_list: list = []
                        current_section[item_key] = new_sub_list
                        current_list = new_sub_list
                        current_key = item_key
                    else:
                        current_section[item_key] = _coerce_value(
                            item_value.strip('"').strip("'")
                        )
                        current_list = None
                else:
                    value = item_body
                    if current_list is not None:
                        current_list.append(value)
                continue

            parts = stripped.split(": ", 1)
            key = parts[0].rstrip(":").strip()
            value = parts[1].strip() if len(parts) > 1 else None

            if value is None:
                # Nested mapping
                new_section: dict = {}
                current_section[key] = new_section
                stack.append((key, current_section, indent, current_list))
                current_section = new_section
                current_list = None
            elif value == "":
                # Start of a list
                new_list: list = []
                current_section[key] = new_list
                current_list = new_list
                current_key = key
            else:
                current_section[key] = _coerce_value(value.strip('"').strip("'"))
                current_list = None

        # Bare list item (no key context, just "- value")
        elif stripped.startswith("- "):
            value = stripped[2:]
            if current_list is not None:
                current_list.append(value)
            elif current_key and isinstance(current_section.get(current_key), list):
                current_section[current_key].append(value)

    # Flush any trailing block scalar
    if block_scalar_key is not None:
        current_section[block_scalar_key] = " ".join(block_scalar_lines).strip()

    return result


# ── Checks ───────────────────────────────────────────────────────────────────

def check_paths(manifest: dict) -> tuple[bool, list[str]]:
    """Verify every kernel entry exists at its declared path."""
    errors: list[str] = []
    entries = manifest.get("kernel", {}).get("entries", [])

    for entry in entries:
        path_str = entry.get("path", "")
        # Handle glob patterns (adapters/*/overlay.yaml)
        if "*" in path_str:
            glob_pattern = path_str.replace("*/", "*/")
            matches = list(ROOT.glob(path_str))
            if not matches:
                errors.append(f"MISSING: {path_str} — no files match glob")
            continue

        full_path = ROOT / path_str
        if not full_path.exists():
            errors.append(f"MISSING: {path_str}")

        # Check sub-files
        for file_name in entry.get("files", []):
            sub_path = full_path / file_name
            if not sub_path.exists():
                errors.append(f"MISSING: {path_str}/{file_name}")

        # Check sub-directories
        for dir_name in entry.get("directories", []):
            sub_path = full_path / dir_name
            if not sub_path.is_dir():
                errors.append(f"MISSING: {path_str}/{dir_name}/")

        # Check skill directories
        for skill_name in entry.get("skills", []):
            skill_path = full_path / skill_name / "SKILL.md"
            if not skill_path.exists():
                errors.append(f"MISSING: {path_str}{skill_name}/SKILL.md")

        # Reverse check: flag a canonical skill directory that exists on disk
        # but is not declared in the manifest's skills list. A passing forward
        # check only certifies declared-completeness, not inventory-completeness.
        if "skills" in entry and full_path.is_dir():
            declared = set(entry.get("skills", []))
            actual = {
                child.name
                for child in full_path.iterdir()
                if child.is_dir() and (child / "SKILL.md").exists()
            }
            for undeclared in sorted(actual - declared):
                errors.append(
                    f"UNDECLARED: {path_str}{undeclared}/SKILL.md exists but is not "
                    f"listed in the manifest's skills: entry for {path_str}"
                )

    return len(errors) == 0, errors


def check_boundary(manifest: dict) -> tuple[bool, list[str]]:
    """Verify no kernel entry references a path outside the repository root."""
    errors: list[str] = []

    def _check_path(path_str: str) -> None:
        resolved = (ROOT / path_str).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"BOUNDARY: {path_str} resolves outside repository root ({resolved})")

    entries = manifest.get("kernel", {}).get("entries", [])
    for entry in entries:
        path_str = entry.get("path", "")
        if "*" not in path_str:
            _check_path(path_str)

    return len(errors) == 0, errors


def check_version_consistency(manifest: dict) -> tuple[bool, list[str]]:
    """Verify schema_version is a positive integer.

    schema_version is the manifest format version, not the product version
    (which lives in the VERSION file). These are separate versioning axes.
    """
    errors: list[str] = []

    manifest_version = manifest.get("schema_version")
    if manifest_version is None:
        errors.append("VERSION: schema_version field is missing")
    elif not isinstance(manifest_version, int) or manifest_version < 1:
        errors.append(
            f"VERSION: schema_version must be a positive integer, got {manifest_version!r}"
        )

    return len(errors) == 0, errors


def check_bootstrap_completeness(manifest: dict) -> tuple[bool, list[str]]:
    """Verify every required_for_bootstrap entry resolves to an existing path."""
    errors: list[str] = []
    entries = manifest.get("kernel", {}).get("entries", [])

    for entry in entries:
        if not entry.get("required_for_bootstrap", False):
            continue
        path_str = entry.get("path", "")
        if "*" in path_str:
            matches = list(ROOT.glob(path_str))
            if not matches:
                errors.append(f"BOOTSTRAP GAP: required entry {path_str} has no matching files")
            continue

        full_path = ROOT / path_str
        if not full_path.exists():
            errors.append(f"BOOTSTRAP GAP: required entry {path_str} does not exist")

    return len(errors) == 0, errors


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    quiet = "--quiet" in sys.argv
    paths_only = "--paths" in sys.argv
    boundary_only = "--boundary" in sys.argv

    if not MANIFEST_PATH.exists():
        if not quiet:
            print(f"FAIL: Manifest not found at {MANIFEST_PATH}")
        sys.exit(2)

    manifest = parse_simple_yaml(MANIFEST_PATH)
    if manifest is None:
        if not quiet:
            print(f"FAIL: Cannot parse manifest at {MANIFEST_PATH}")
        sys.exit(2)

    all_passed = True

    if boundary_only:
        checks = [("Boundary integrity", check_boundary)]
    elif paths_only:
        checks = [
            ("Path existence", check_paths),
            ("Bootstrap completeness", check_bootstrap_completeness),
        ]
    else:
        checks = [
            ("Path existence", check_paths),
            ("Boundary integrity", check_boundary),
            ("Version consistency", check_version_consistency),
            ("Bootstrap completeness", check_bootstrap_completeness),
        ]

    for name, check_fn in checks:
        passed, errors = check_fn(manifest)
        if not quiet:
            status = "PASS" if passed else "FAIL"
            print(f"  {status}: {name}")
            for err in errors:
                print(f"    - {err}")
        if not passed:
            all_passed = False

    if not quiet:
        if all_passed:
            print("\nAll kernel integrity checks passed.")
        else:
            print("\nOne or more kernel integrity checks FAILED.")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
