"""YAML frontmatter generation and validation.

Uses only Python 3 standard library. Generates frontmatter for new Work Objects
and validates enum membership and required fields.
"""

from datetime import datetime, timezone
from pathlib import PurePosixPath
from typing import Dict, List, Optional

# ── Enums ─────────────────────────────────────────────────────────────────────

VALID_TYPES = frozenset({"change", "inquiry", "project", "incident"})
VALID_CONSEQUENCES = frozenset({"low", "meaningful", "high"})
VALID_SENSITIVITIES = frozenset({"ordinary", "private", "restricted"})
# Domain is a SECOND axis independent of `type` (WO 2026-08-22-031 Decision 1):
# `type` describes the shape of work (change/inquiry/project/incident), while
# `domain` describes its discipline. List-shaped, not scalar (Decision 3):
# the corpus test found most recent objects genuinely span more than one
# domain (e.g. a business decision exposed through engineering dispatch).
VALID_DOMAINS = frozenset({
    "business", "architecture", "asset", "design",
    "governance", "engineering", "research", "ideation", "operations",
    "production",
})
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


def validate_domain(values: List[str]) -> Optional[str]:
    """Return error message if the domain list is invalid, or None.

    The field itself is optional (legacy objects may omit it entirely --
    no retro-migration required, WO 2026-08-22-031 Decision 1 non-goals).
    When present, it must be a non-empty list of values drawn from
    VALID_DOMAINS; an unknown value is rejected, not silently accepted.
    """
    if not values:
        return "Domain list, if present, must contain at least one value."
    unknown = [v for v in values if v not in VALID_DOMAINS]
    if unknown:
        return (
            f"Invalid domain value(s): {', '.join(unknown)}. "
            f"Must be one of: {', '.join(sorted(VALID_DOMAINS))}"
        )
    return None


def format_domain_field(values: List[str]) -> str:
    """Format a domain list as an inline flow list for frontmatter.

    e.g. ["business", "architecture"] -> "[business, architecture]"
    Order is preserved (primary domain first, per Decision 3) -- not sorted.
    """
    return "[" + ", ".join(values) + "]"


def parse_domain_field(raw_value: str) -> List[str]:
    """Parse a domain frontmatter value back into an ordered list of strings.

    `parse_frontmatter`'s generic scalar parser does not handle bracketed
    flow lists (see its docstring: "scalar key: value pairs only"), so
    `domain` is parsed with this dedicated helper wherever it is read,
    rather than by extending the shared generic parser for one field.
    Returns an empty list for an empty/missing value.
    """
    raw_value = raw_value.strip()
    if not raw_value:
        return []
    if raw_value.startswith("[") and raw_value.endswith("]"):
        raw_value = raw_value[1:-1]
    return [part.strip() for part in raw_value.split(",") if part.strip()]


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
    domain: Optional[List[str]] = None,
) -> str:
    """Generate YAML frontmatter for a new Work Object.

    Args:
        obj_id: Allocated immutable ID (e.g. 2026-07-21-010)
        title: Work Object title
        obj_type: One of change, inquiry, project, incident
        consequence: One of low, meaningful, high
        sensitivity: One of ordinary, restricted
        domain: Optional list of discipline values (a SECOND axis independent
            of obj_type, e.g. ["business", "architecture"]) -- omitted
            entirely on legacy/unclassified objects, no retro-migration.

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
    if domain:
        lines.append(f"domain: {format_domain_field(domain)}")
    lines.extend([
        f"created_at: {now}",
        f"updated_at: {now}",
        'next_action: "Awaiting activation/classification (notice state)"',
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
