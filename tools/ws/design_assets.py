"""Validation helpers for local Work Studio design asset records."""

from __future__ import annotations

import re
from pathlib import Path


VALID_ASSET_STATUSES = {"tracer", "draft", "active", "deprecated", "retired"}
VALID_ASSET_KINDS = {
    "foundation",
    "token-set",
    "theme",
    "component-family",
    "ux-pattern",
    "flow",
    "projection",
}

REQUIRED_FIELDS = (
    "Work Object",
    "Pipeline",
    "Status",
    "Asset ID",
    "Asset kind",
    "Source of truth",
    "Projection status",
)

REQUIRED_SECTIONS = (
    "Asset Summary",
    "Lifecycle",
    "Verification Notes",
    "Rollback",
)

_FIELD_RE = re.compile(r"^\*\*(?P<name>[^*]+):\*\*\s*(?P<value>.+?)\s*$", re.MULTILINE)
_SECTION_RE = re.compile(r"^##\s+(?P<name>.+?)\s*$", re.MULTILINE)


def asset_slug(asset_id: str) -> str:
    """Return a stable filename slug for a design asset ID."""
    normalized = asset_id.strip().strip("`")
    if not normalized.startswith("asset.design."):
        raise ValueError("asset ID must start with asset.design.")
    slug = normalized.removeprefix("asset.design.")
    if not re.fullmatch(r"[a-z0-9][a-z0-9.-]*", slug):
        raise ValueError("asset ID suffix must be lowercase letters, digits, dots, or hyphens")
    return slug.replace(".", "-")


def compose_draft_asset_record(
    *,
    asset_id: str,
    asset_kind: str,
    work_object: str,
    summary: str,
    source_note: str,
    frontier: str = "identity",
    pipeline: str = "references/DESIGN-ASSET-PIPELINE.md",
) -> str:
    """Compose a draft asset record proposal from explicit ingest inputs."""
    bare_asset_id = asset_id.strip().strip("`")
    if asset_kind not in VALID_ASSET_KINDS:
        raise ValueError(f"asset kind must be one of {sorted(VALID_ASSET_KINDS)}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}-\d{3}", work_object):
        raise ValueError("work_object must look like YYYY-MM-DD-NNN")
    asset_slug(bare_asset_id)
    clean_summary = " ".join(summary.strip().split())
    clean_source = " ".join(source_note.strip().split())
    if not clean_summary:
        raise ValueError("summary is required")
    if not clean_source:
        raise ValueError("source_note is required")

    return f"""# {bare_asset_id} Asset Record

**Work Object:** `{work_object}`  
**Pipeline:** `{pipeline}`  
**Status:** draft  
**Asset ID:** `{bare_asset_id}`  
**Asset kind:** {asset_kind}  
**Source of truth:** draft ingest proposal from explicit input: {clean_source}  
**Projection status:** projections are read-only and must not be edited as asset truth.

## Asset Summary

{clean_summary}

## Lifecycle

| Step | Owning skill | Evidence |
|------|--------------|----------|
| Intake and identity | `design-manage-assets` | Draft asset record proposed from explicit ingest input; current frontier is `{frontier}`. |

## Verification Notes

- This is a draft ingest proposal, not an accepted canonical asset.
- `design-manage-assets` must classify the record and route the next frontier.
- Creative approval, implementation, component registration, external sync, and projection publishing remain separate authority boundaries.

## Rollback

Delete this draft asset record if it has not been accepted. If accepted later,
retire it through the governing Work Object instead of deleting history.
"""


def asset_record_paths(workspace_root: Path) -> list[Path]:
    """Return local design asset record paths, excluding the template."""
    asset_dir = workspace_root / ".work-studio" / "design-assets"
    if not asset_dir.is_dir():
        return []
    return sorted(
        path
        for path in asset_dir.glob("*.asset.md")
        if path.name != "asset-template.asset.md"
    )


def parse_asset_fields(text: str) -> dict[str, str]:
    """Parse top-level bold field labels used by asset records."""
    return {match.group("name").strip(): match.group("value").strip() for match in _FIELD_RE.finditer(text)}


def parse_sections(text: str) -> set[str]:
    """Return second-level section names from an asset record."""
    return {match.group("name").strip() for match in _SECTION_RE.finditer(text)}


def validate_asset_record(path: Path) -> list[str]:
    """Validate one design asset record."""
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    fields = parse_asset_fields(text)
    sections = parse_sections(text)

    for field in REQUIRED_FIELDS:
        if field not in fields:
            errors.append(f"{path}: missing required field {field!r}")

    for section in REQUIRED_SECTIONS:
        if section not in sections:
            errors.append(f"{path}: missing required section '## {section}'")

    asset_id = fields.get("Asset ID", "")
    if asset_id and not re.fullmatch(r"`asset\.design\.[a-z0-9][a-z0-9.-]*`", asset_id):
        errors.append(
            f"{path}: Asset ID must be backtick-wrapped and start with asset.design."
        )

    status = fields.get("Status", "")
    if status and status not in VALID_ASSET_STATUSES:
        errors.append(
            f"{path}: Status {status!r} must be one of {sorted(VALID_ASSET_STATUSES)}"
        )

    asset_kind = fields.get("Asset kind", "")
    if asset_kind and asset_kind not in VALID_ASSET_KINDS:
        errors.append(
            f"{path}: Asset kind {asset_kind!r} must be one of {sorted(VALID_ASSET_KINDS)}"
        )

    projection_status = fields.get("Projection status", "").lower()
    if projection_status and ("read-only" not in projection_status or "truth" not in projection_status):
        errors.append(
            f"{path}: Projection status must state that projections are read-only and not asset truth"
        )

    lifecycle = _section_body(text, "Lifecycle")
    owner_rows = [
        line
        for line in lifecycle.splitlines()
        if line.startswith("|") and "`" in line and "Owning skill" not in line
    ]
    if not owner_rows:
        errors.append(f"{path}: Lifecycle must include at least one owning-skill row")

    return errors


def validate_asset_registry(workspace_root: Path) -> list[str]:
    """Validate all local design asset records in a workspace."""
    errors: list[str] = []
    paths = asset_record_paths(workspace_root)
    if not paths:
        return [f"{workspace_root / '.work-studio' / 'design-assets'}: no asset records found"]
    for path in paths:
        errors.extend(validate_asset_record(path))
    return errors


def _section_body(text: str, section_name: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(section_name)}\s*$"
        rf"(?P<body>.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group("body") if match else ""
