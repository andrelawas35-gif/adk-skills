"""Read-only routing helpers for local design asset records."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .design_assets import parse_asset_fields, validate_asset_record


FRONTIER_OWNERS = {
    "identity": "design-manage-assets",
    "foundation": "design-compose-design-system",
    "tokens": "design-compose-design-system",
    "theme": "design-compose-design-system",
    "variant": "design-compose-design-system",
    "component-family": "design-compose-design-system",
    "ux-pattern": "design-steward-experience-patterns",
    "flow": "design-steward-experience-patterns",
    "creative-direction": "design-apply-design-direction",
    "implementation": "alawas-engineering-implement-bounded-change",
    "verification": "design-verify-design-implementation",
    "accessibility": "design-audit-accessibility",
    "critique": "design-critique-usability",
    "component-registration": "design-track-components",
    "projection": "design-project-asset-workbench",
}


@dataclass(frozen=True)
class AssetRoute:
    asset_id: str
    asset_kind: str
    status: str
    owner: str
    frontier: str
    gaps: tuple[str, ...]


def route_asset_record(path: Path, frontier: str = "identity") -> AssetRoute:
    """Classify one asset record and route its current frontier."""
    text = path.read_text(encoding="utf-8")
    fields = parse_asset_fields(text)
    validation_errors = tuple(validate_asset_record(path))

    if frontier not in FRONTIER_OWNERS:
        return AssetRoute(
            asset_id=fields.get("Asset ID", ""),
            asset_kind=fields.get("Asset kind", ""),
            status=fields.get("Status", ""),
            owner="",
            frontier=frontier,
            gaps=(f"unknown design asset frontier: {frontier}",) + validation_errors,
        )

    return AssetRoute(
        asset_id=fields.get("Asset ID", ""),
        asset_kind=fields.get("Asset kind", ""),
        status=fields.get("Status", ""),
        owner=FRONTIER_OWNERS[frontier],
        frontier=frontier,
        gaps=validation_errors,
    )
