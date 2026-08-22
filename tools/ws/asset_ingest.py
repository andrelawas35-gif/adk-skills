"""Controlled local ingest for draft design asset records."""

from __future__ import annotations

from pathlib import Path

from .design_assets import asset_slug, compose_draft_asset_record, validate_asset_record


def ingest_asset(
    workspace_root: Path,
    *,
    asset_id: str,
    asset_kind: str,
    work_object: str,
    summary: str,
    source_note: str,
    frontier: str = "identity",
) -> dict:
    """Create one draft asset record from explicit inputs.

    The command is intentionally conservative: it never scans folders, imports
    external tools, overwrites an existing record, or marks an asset active.
    """
    asset_dir = workspace_root / ".work-studio" / "design-assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    path = asset_dir / f"{asset_slug(asset_id)}.asset.md"
    if path.exists():
        raise FileExistsError(f"asset record already exists: {path}")

    text = compose_draft_asset_record(
        asset_id=asset_id,
        asset_kind=asset_kind,
        work_object=work_object,
        summary=summary,
        source_note=source_note,
        frontier=frontier,
    )
    path.write_text(text, encoding="utf-8")
    errors = validate_asset_record(path)
    return {"path": path, "errors": errors}
