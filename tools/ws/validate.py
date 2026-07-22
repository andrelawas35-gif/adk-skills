"""Composed validation checks for Work Objects.

Runs named validation checks against Work Object files or the full
workspace. Each check is independently invocable. With no args, runs
all checks against all objects.

Checks:
  schema      — YAML frontmatter field validation
  sections    — Required section presence and ordering
  append-only — History/Evidence/Decisions are append-only
  attention   — active.md consistency cross-check
  sensitivity — Restricted content in body vs pointer check
  lifecycle   — No terminal-state violations
  structure   — Composite: schema + sections
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional

from .schema import (
    parse_frontmatter,
    validate_consequence,
    validate_sensitivity,
    validate_state,
    validate_status,
    validate_type,
)
from .sections import (
    REQUIRED_SECTION_ORDER,
    parse_sections,
    validate_section_order,
)
from .lifecycle import (
    VALID_STATES,
    VALID_STATUSES,
    validate_transition,
)
from .attention import check_attention_consistency


# ── Schema check ──────────────────────────────────────────────────────────────


def check_schema(file_path: Path) -> List[str]:
    """Validate YAML frontmatter for a single Work Object.

    Checks: presence of required fields, enum membership, immutable
    field consistency.
    """
    errors = []

    try:
        content = file_path.read_text()
    except Exception as e:
        return [f"{file_path}: Cannot read file: {e}"]

    try:
        fm = parse_frontmatter(content)
    except ValueError as e:
        return [f"{file_path}: Invalid frontmatter: {e}"]

    # Required fields
    required_fields = [
        "schema_version", "id", "title", "type",
        "status", "state", "consequence", "sensitivity",
        "created_at", "updated_at",
    ]
    for field in required_fields:
        if field not in fm:
            errors.append(f"{file_path}: Missing required field: {field}")

    # Enum validation
    for field, validator, valid_set in [
        ("type", validate_type, {"change", "inquiry", "project", "incident"}),
        ("status", validate_status, {"active", "waiting", "paused", "closed"}),
        ("state", validate_state, VALID_STATES),
        ("consequence", validate_consequence, {"low", "meaningful", "high"}),
        ("sensitivity", validate_sensitivity, {"ordinary", "restricted"}),
    ]:
        value = fm.get(field)
        if value is not None:
            err = validator(str(value))
            if err:
                errors.append(f"{file_path}: {err}")

    # Immutable field check: id in filename must match id in frontmatter
    fm_id = str(fm.get("id", ""))
    if fm_id and not file_path.name.startswith(fm_id):
        errors.append(
            f"{file_path}: Frontmatter id '{fm_id}' does not match filename"
        )

    return errors


# ── Sections check ────────────────────────────────────────────────────────────


def check_sections(file_path: Path) -> List[str]:
    """Validate required section presence and ordering."""
    try:
        content = file_path.read_text()
    except Exception as e:
        return [f"{file_path}: Cannot read file: {e}"]

    # Extract body (everything after frontmatter)
    if content.startswith("---"):
        end = content.find("---", 3)
        if end == -1:
            return [f"{file_path}: Unclosed frontmatter"]
        body = content[end + 3:].strip()
    else:
        body = content

    section_errors = validate_section_order(body)
    return [f"{file_path}: {e}" for e in section_errors]


# ── Append-only check ─────────────────────────────────────────────────────────


def check_append_only(file_path: Path) -> List[str]:
    """Check that append-only sections haven't lost content.

    Uses a structural heuristic: the file's History section (if present)
    should not be empty for objects beyond the notice state. Also checks
    that Evidence ledger entries follow the table format.

    Note: Full append-only verification requires git history comparison
    (as verify-append-only.py does). This check provides structural
    validation only.
    """
    errors = []

    try:
        content = file_path.read_text()
    except Exception as e:
        return [f"{file_path}: Cannot read file: {e}"]

    fm = parse_frontmatter(content)

    # Extract body
    if content.startswith("---"):
        end = content.find("---", 3)
        if end == -1:
            return [f"{file_path}: Unclosed frontmatter"]
        body = content[end + 3:].strip()
    else:
        body = content

    sections = parse_sections(body)

    # History section structural check
    history = sections.get("history", "")
    if not history or history.strip() == "## History":
        # Empty history is fine for notice-state objects
        state = str(fm.get("state", "notice"))
        if state != "notice":
            errors.append(
                f"{file_path}: History section is empty but object state is '{state}'"
            )

    # Evidence ledger structural check
    evidence = sections.get("evidence ledger", "")
    if evidence:
        lines = evidence.strip().split("\n")
        # Skip heading and table header (first 3 lines)
        for i, line in enumerate(lines):
            if i < 3:
                continue
            if line.strip() and not line.strip().startswith("|"):
                errors.append(
                    f"{file_path}: Evidence ledger line {i+1} does not follow table format"
                )

    return errors


# ── Sensitivity check ─────────────────────────────────────────────────────────


def check_sensitivity(file_path: Path) -> List[str]:
    """Check that restricted-content objects use pointers, not inline body.

    Per ADR 0019: restricted sensitivity objects should not contain
    restricted content directly in the body.
    """
    errors = []

    try:
        content = file_path.read_text()
    except Exception as e:
        return [f"{file_path}: Cannot read file: {e}"]

    fm = parse_frontmatter(content)
    sensitivity = str(fm.get("sensitivity", "ordinary"))

    if sensitivity == "restricted":
        # Check for common restricted-content patterns
        restricted_patterns = [
            "password", "secret", "token", "api_key",
            "credential", "private_key",
        ]
        body_lower = content.lower()
        for pattern in restricted_patterns:
            if pattern in body_lower:
                errors.append(
                    f"{file_path}: Restricted object may contain sensitive "
                    f"content (found '{pattern}'). Use pointer references instead."
                )
                break  # One warning per file is sufficient

    return errors


# ── Lifecycle check ───────────────────────────────────────────────────────────


def check_lifecycle(file_path: Path) -> List[str]:
    """Check for terminal-state violations in Work Objects."""
    errors = []

    try:
        content = file_path.read_text()
    except Exception as e:
        return [f"{file_path}: Cannot read file: {e}"]

    fm = parse_frontmatter(content)
    state = str(fm.get("state", ""))
    status = str(fm.get("status", ""))

    # Check: state 'close' but status not 'closed'
    if state == "close" and status != "closed":
        errors.append(
            f"{file_path}: State is 'close' but status is '{status}'. "
            "Objects in close state should have closed status."
        )

    # Check: status 'closed' with state that implies active work
    closed_incompatible = {"notice", "explore", "design", "build", "verify"}
    if status == "closed" and state in closed_incompatible:
        errors.append(
            f"{file_path}: Status is 'closed' but state is '{state}'. "
            "Closed objects should be in 'close', 'release', or 'observe' state."
        )

    return errors


# ── Structure check ───────────────────────────────────────────────────────────


def check_structure(file_path: Path) -> List[str]:
    """Composite check: schema + sections."""
    return check_schema(file_path) + check_sections(file_path)


# ── Check registry ────────────────────────────────────────────────────────────

CHECK_REGISTRY: Dict[str, callable] = {
    "schema": check_schema,
    "sections": check_sections,
    "append-only": check_append_only,
    "attention": None,  # Special: workspace-level check
    "sensitivity": check_sensitivity,
    "lifecycle": check_lifecycle,
    "structure": check_structure,
}

DEFAULT_CHECKS = ["schema", "sections", "append-only", "sensitivity", "lifecycle"]


# ── Entry point ───────────────────────────────────────────────────────────────


def run_checks(
    check_names: Optional[List[str]],
    file_paths: List[Path],
    active_md_path: Optional[Path] = None,
    objects_dir: Optional[Path] = None,
) -> int:
    """Run named validation checks.

    Args:
        check_names: List of check names, or None for defaults.
        file_paths: Files to validate.
        active_md_path: Path to active.md (for attention check).
        objects_dir: Path to objects/ directory.

    Returns:
        Exit code: 0 if all checks pass, 1 if any fail.
    """
    if check_names is None:
        check_names = list(DEFAULT_CHECKS)

    all_errors: List[str] = []

    for name in check_names:
        if name not in CHECK_REGISTRY:
            print(f"Error: Unknown check '{name}'", file=sys.stderr)
            print(f"Available: {', '.join(sorted(CHECK_REGISTRY.keys()))}",
                  file=sys.stderr)
            return 1

        if name == "attention":
            # Workspace-level check
            if active_md_path and objects_dir:
                errs = check_attention_consistency(active_md_path, objects_dir)
                all_errors.extend(errs)
            else:
                all_errors.append(
                    "Attention check requires active.md and objects/ directory"
                )
            continue

        check_fn = CHECK_REGISTRY[name]
        for fp in file_paths:
            errs = check_fn(fp)
            all_errors.extend(errs)

    for err in all_errors:
        print(err, file=sys.stderr)

    if all_errors:
        print(f"\n{len(all_errors)} validation error(s) found.", file=sys.stderr)
        return 1

    print("All validation checks passed.")
    return 0
