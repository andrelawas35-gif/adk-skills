# Missing Artifact Gap

An absent registered artifact is a **Missing Artifact Gap**, never evidence or
permission to invent content.

**Authoritative source:** `WORKSPACE-DOCUMENTATION-CONTRACT.md` (Operating
Rules). The contract document is the canonical registry of artifact types,
paths, ownership, stage triggers, provenance rules, and validation pointers.
This constitution file extracts the single behavioral rule that applies to
every skill: do not fabricate content when an expected artifact is missing.

## Application

When a skill or agent discovers that a registered artifact is absent from its
declared location:

1. **Report the gap** — name the missing artifact and its expected path as
   registered in `WORKSPACE-DOCUMENTATION-CONTRACT.md`.
2. **Stop the affected path** — do not substitute a plausible alternative,
   search for look-alike files, or invent content to fill the gap.
3. **Offer the correct route** — typically, request bootstrap authority
   (for the contract itself) or scoped creation authority (for other
   registered artifact types).

A Missing Artifact Gap is an explicit discovery outcome. It is not a failure
mode, a degraded state, or an invitation to work around the contract.

## Relationship to the Workspace Documentation Contract

The `WORKSPACE-DOCUMENTATION-CONTRACT.md` is the authoritative registry of
which artifacts exist, where they live, who owns them, and what evidence is
required to create or modify them. This constitution file carries only the
universal behavioral obligation — do not fabricate — and cites the contract
as its source.

If the behavioral rule itself changes, the contract document is the
authoritative source and this file must be updated to match. If the contract's
registry schema changes but the behavioral rule remains the same, this file
requires no update.
