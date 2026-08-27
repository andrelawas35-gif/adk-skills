---
schema_version: 1
id: 2026-08-22-033
title: Document the current Work Studio system and CLI workflows
type: project
status: closed
state: close
consequence: low
sensitivity: ordinary
domain: [research]
created_at: 2026-08-22T15:33:48Z
updated_at: 2026-08-22T15:39:39Z
next_action: Investigate the current architecture, workflows, command surfaces, setup, and verification; then produce and link the standalone report.




---
## Intent

Produce one comprehensible, standalone reference describing the current Work
Studio system, its operating workflow, CLI commands, installation,
verification, runtime graph surfaces, and recovery operations from current
repository evidence.

## Success evidence

- [x] The reference explains the current system architecture and source-of-truth hierarchy.
- [x] The reference explains the Work Object lifecycle, evidence, authority, and attention model.
- [x] The reference inventories every current top-level `ws` command and nested command group.
- [x] The reference covers adapter installation, runtime invocation, verification, backup, and recovery.
- [x] Current verification and dependency gaps are disclosed instead of silently omitted.


## Constraints and non-goals

**Constraints:**
- Describe implemented current behavior only.
- Ground command signatures in executable `--help` output and current source.
- Write the standalone deliverable inside `.work-studio/deliverables/`.
- Preserve unrelated working-tree changes.

**Non-goals:**
- Propose new architecture, roadmap items, or workflow decisions.
- Export or publish the reference outside `.work-studio/`.
- Repair verification failures discovered during documentation.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Produce a current-state report from executable and canonical evidence

| Field | Value |
|-------|-------|
| **Decision type** | authority |
| **Result** | pass |
| **Scope** | Create one standalone reference at `.work-studio/deliverables/2026-08-22-033-work-studio-system-reference.md`, grounded in the current repository and live CLI help. |
| **Authorization** | Director's explicit request in this session. |
| **Confidence** | high for current repository description and CLI inventory; medium for runtime operational examples because only help/import behavior was exercised, not every runtime route end to end. |
| **Actor** | director |
| **Revisit trigger** | Work Studio version, CLI parser, lifecycle schema, kernel manifest, adapter layout, or runtime command surface changes. |
| **Rationale** | A current-system reference is most reliable when canonical contracts and executable command surfaces override stale summaries, while observed gaps remain visible. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [decision] | Director activation | [decision] Director requested a comprehensible standalone reference describing the current system, its workflows, CLI commands, and related operational usage. |
| [system] | Current repository inspection and executable CLI help, 2026-08-22 | README.md, canonical contracts, kernel manifest, pyproject files, install scripts, tools/ws parser help, runtime graph help through uv, and verification tools were inspected. The report inventories current architecture, workflow, commands, setup, verification, and recovery. Observed gaps: plain Python runtime lacks langgraph outside the synced uv environment; verify-kernel reports three implemented design skills absent from the kernel manifest. |
## Open questions

None blocking delivery. The kernel-manifest omissions discovered during
verification remain a separate implementation gap.

## Next move

Use the reference as the current operator guide and refresh it when a listed
revisit trigger occurs.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T15:33:48Z — Started via ws start (created + evidence + explore + activate supporting)

- **State:** explore
- **Status:** active
- **Actor:** director
- **Rationale:** Create an evidence-grounded reference from the current repository rather than relying on remembered or prospective design.
### 2026-08-22T15:39:39Z — Closed: Produced and linked the 3,368-word, 13-section current-system reference. All four bounded investigations are answered; current dependency and kernel-manifest gaps are disclosed in the deliverable.

- **State:** close
- **Status:** closed
- **Actor:** codex
- **Rationale:** Produced and linked the 3,368-word, 13-section current-system reference. All four bounded investigations are answered; current dependency and kernel-manifest gaps are disclosed in the deliverable.
## artifacts

- `.work-studio/deliverables/2026-08-22-033-work-studio-system-reference.md` (fingerprint: `7ca23551fd46`, commit: uncommitted at record time) — Standalone current-system, workflow, CLI, runtime, installation, verification, and recovery reference
