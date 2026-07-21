# Use a Workspace Documentation Contract

## Status

Accepted

> **Partially superseded by ADR-0021** (2026-07-21): the consequence "adapter
> generation copies the contract so installed skills use the same rules" is
> narrowed. The behavioral rule (Missing Artifact Gap) now travels via a
> standalone constitution file (`references/MISSING-ARTIFACT-GAP.md`) copied
> into every adapter. The full contract document remains the authoritative
> registry for artifact types, paths, and ownership — a lookup table for
> `conduct-work-object` and `track-components`.

## Context

Skills could discover similarly named documents inconsistently, invent project
facts when records were absent, or create broad template trees in empty
workspaces. Generated adapters also needed a visible boundary from their
canonical sources.

## Decision

Use root-level `WORKSPACE-DOCUMENTATION-CONTRACT.md` as the sole bootstrap
artifact and canonical registry. It is Markdown with a versioned YAML registry
that declares the full artifact taxonomy, exact workspace paths, ownership,
stage triggers, provenance and freshness, mutation authority, supersession,
canonical/generated status, and validation for each type.

`conduct-work-object` owns discovery, bootstrap, persistence, and contract
conflicts. Specialists inspect the contract, disclose missing artifacts, and
recommend the smallest scoped mutation. A missing artifact is an evidence gap,
not a reason to fabricate content or silently create a template.

## Consequences

An explicit bootstrap request creates only the contract. Subsequent artifacts,
legacy migrations, generated-output cleanup, and contract changes require their
own authority. Taxonomy and schema changes require a separate ADR. Adapter
generation copies the contract so installed skills use the same rules.
