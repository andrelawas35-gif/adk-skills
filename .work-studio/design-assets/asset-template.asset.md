# Asset Template

**Work Object:** `YYYY-MM-DD-NNN`  
**Pipeline:** `references/DESIGN-ASSET-PIPELINE.md`  
**Status:** draft  
**Asset ID:** `asset.design.example`  
**Asset kind:** component-family  
**Source of truth:** this asset record  
**Projection status:** projections may read this record; they are read-only and must not be edited as asset truth.

## Asset Summary

Describe the reusable design asset and the user, system, or studio purpose it
serves.

## Lifecycle

| Step | Owning skill | Evidence |
|------|--------------|----------|
| Intake and identity | `design-manage-assets` | Asset ID, kind, source of truth, lifecycle status, provenance, and current frontier are recorded here. |

## Verification Notes

- The asset record has one owning skill for each lifecycle frontier.
- Projections point back to this record instead of becoming a source of truth.

## Rollback

Retire or delete this draft record if it has not been accepted; for accepted
assets, preserve history and route retirement through the owning Work Object.
