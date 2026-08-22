# asset.design.studio-status-tokens Asset Record

**Work Object:** `2026-08-22-017`  
**Pipeline:** `references/DESIGN-ASSET-PIPELINE.md`  
**Status:** draft  
**Asset ID:** `asset.design.studio-status-tokens`  
**Asset kind:** token-set  
**Source of truth:** draft ingest proposal from explicit input: manual ingest slice from Work Object 2026-08-22-017  
**Projection status:** projections are read-only and must not be edited as asset truth.

## Asset Summary

Draft token-set asset for studio status colors used to test explicit asset ingest before canonization.

## Lifecycle

| Step | Owning skill | Evidence |
|------|--------------|----------|
| Intake and identity | `design-manage-assets` | Draft asset record proposed from explicit ingest input; current frontier is `tokens`. |

## Verification Notes

- This is a draft ingest proposal, not an accepted canonical asset.
- `design-manage-assets` must classify the record and route the next frontier.
- Creative approval, implementation, component registration, external sync, and projection publishing remain separate authority boundaries.

## Rollback

Delete this draft asset record if it has not been accepted. If accepted later,
retire it through the governing Work Object instead of deleting history.
