"""YAML frontmatter generation and validation.

Uses only Python 3 standard library. Generates frontmatter for new Work Objects
and validates enum membership and required fields.
"""

from datetime import datetime, timezone
from pathlib import PurePosixPath
from typing import Dict, Optional

# ── Enums ─────────────────────────────────────────────────────────────────────

VALID_TYPES = frozenset({"change", "inquiry", "project", "incident"})
VALID_CONSEQUENCES = frozenset({"low", "meaningful", "high"})
VALID_SENSITIVITIES = frozenset({"ordinary", "private", "restricted"})
VALID_STATES = frozenset({
    "notice", "explore", "design", "build",
    "verify", "release", "observe", "close",
})
VALID_STATUSES = frozenset({"active", "waiting", "paused", "closed"})


# ── Validation ────────────────────────────────────────────────────────────────

def validate_type(value: str) -> Optional[str]:
    """Return error message if type is invalid, or None."""
    if value not in VALID_TYPES:
        return f"Invalid type '{value}'. Must be one of: {', '.join(sorted(VALID_TYPES))}"
    return None


def validate_consequence(value: str) -> Optional[str]:
    """Return error message if consequence is invalid, or None."""
    if value not in VALID_CONSEQUENCES:
        return f"Invalid consequence '{value}'. Must be one of: {', '.join(sorted(VALID_CONSEQUENCES))}"
    return None


def validate_sensitivity(value: str) -> Optional[str]:
    """Return error message if sensitivity is invalid, or None."""
    if value not in VALID_SENSITIVITIES:
        return f"Invalid sensitivity '{value}'. Must be one of: {', '.join(sorted(VALID_SENSITIVITIES))}"
    return None


def validate_campaign(value: object) -> Optional[str]:
    """Return an error when a campaign is not a canonical design-doc anchor."""
    if not isinstance(value, str) or not value:
        return "Invalid campaign. Must be a repository-relative docs/design/*.md path"
    if value.startswith("/") or "\\" in value:
        return (
            f"Invalid campaign '{value}'. "
            "Must be a repository-relative docs/design/*.md path"
        )

    path = PurePosixPath(value)
    if (
        str(path) != value
        or len(path.parts) != 3
        or path.parts[:2] != ("docs", "design")
        or path.suffix != ".md"
        or any(part in {".", ".."} for part in path.parts)
    ):
        return (
            f"Invalid campaign '{value}'. "
            "Must be a repository-relative docs/design/*.md path"
        )
    return None


def validate_state(value: str) -> Optional[str]:
    """Return error message if state is invalid, or None."""
    if value not in VALID_STATES:
        return f"Invalid state '{value}'. Must be one of: {', '.join(sorted(VALID_STATES))}"
    return None


def validate_status(value: str) -> Optional[str]:
    """Return error message if status is invalid, or None."""
    if value not in VALID_STATUSES:
        return f"Invalid status '{value}'. Must be one of: {', '.join(sorted(VALID_STATUSES))}"
    return None


# ── Frontmatter generation ────────────────────────────────────────────────────

def generate_frontmatter(
    obj_id: str,
    title: str,
    obj_type: str,
    consequence: str,
    sensitivity: str,
    campaign: Optional[str] = None,
) -> str:
    """Generate YAML frontmatter for a new Work Object.

    Args:
        obj_id: Allocated immutable ID (e.g. 2026-07-21-010)
        title: Work Object title
        obj_type: One of change, inquiry, project, incident
        consequence: One of low, meaningful, high
        sensitivity: One of ordinary, restricted

    Returns:
        YAML frontmatter string (including --- delimiters)
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = [
        "---",
        f"schema_version: 1",
        f"id: {obj_id}",
        f"title: {title}",
        f"type: {obj_type}",
        f"status: active",
        f"state: notice",
        f"consequence: {consequence}",
        f"sensitivity: {sensitivity}",
    ]
    if campaign is not None:
        lines.append(f"campaign: {campaign}")
    lines.extend([
        f"created_at: {now}",
        f"updated_at: {now}",
        "---",
        "",
    ])

    return "\n".join(lines)


# ── Frontmatter parsing ──────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> Dict[str, object]:
    """Parse a minimal YAML frontmatter block.

    Handles scalar key: value pairs only — sufficient for Work Object
    frontmatter format. Reuses the pattern from generate-adapters.py.

    Returns a dict of parsed values or raises ValueError.
    """
    if not text.startswith("---"):
        raise ValueError("Frontmatter must start with '---'")

    end = text.find("---", 3)
    if end == -1:
        raise ValueError("Frontmatter must have closing '---'")

    fm_text = text[4:end].strip()
    result = {}

    for line in fm_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            result[key] = _parse_scalar(val)

    return result


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
