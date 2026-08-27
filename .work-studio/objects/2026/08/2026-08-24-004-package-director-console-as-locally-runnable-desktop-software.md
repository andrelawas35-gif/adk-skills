---
schema_version: 1
id: 2026-08-24-004
title: Package Director Console as locally runnable Windows and macOS desktop software
type: project
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-24T22:58:03Z
updated_at: 2026-08-24T23:16:41Z
next_action: Verify the macOS desktop tracer path: launch pywebview on macOS, read a Scene Work Object, record one sanctioned Direction, confirm workspace-local artifact opening via macOS open, and capture separate macOS packaging evidence before release decisions.














---
## Intent

Plan and then implement a Windows and macOS desktop application that runs the
Director Console locally while preserving Work Studio as the file-first
governed source of truth. The application should make the existing Scene Board,
Direction input, artifact review, and later Blender/ComfyUI integrations feel
like one desktop product without creating a parallel persistence model.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] One bounded desktop tracer opens as a native Windows application without
      requiring the director to start a terminal manually.
- [ ] The same bounded desktop tracer opens as a native macOS application
      without requiring the director to start a terminal manually.
- [x] The tracer reads the existing SC030 Scene Work Object through the current
      Scene Board projection and records one Direction through the sanctioned
      `tools/ws` mutation path.
- [ ] macOS reads a Scene Work Object and records an equivalent Direction
      through the sanctioned `tools/ws` mutation path.
- [ ] Closing and reopening the application preserves all durable state in
      `.work-studio/` on Windows and macOS; no application database becomes
      canonical.
- [x] Packaging, logs, failure behavior, rollback, and focused verification are
      explicit enough for a different agent to implement and test on Windows.
- [ ] macOS packaging, logs, failure behavior, rollback, and focused
      verification are explicit enough for a different agent to implement and
      test.


## Constraints and non-goals

**Constraints:**
- Windows and macOS, locally runnable on both.
- File-first: `.work-studio/` and local artifacts remain canonical.
- Reuse the existing `ws direction`, `ws scene-board`, and Work Object lifecycle.
- Preserve human authority for canon-establishing actions.
- Keep ComfyUI and Blender as optional local instruments behind capability checks.
- Preserve unrelated dirty work already present in the repository.

**Non-goals:**
- Rebuilding Work Studio persistence in SQLite or another application database.
- Implementing Blender, ComfyUI, audio, animatic, or agentic-dailies features in
  the first desktop tracer.
- Auto-update, code signing, notarization, public distribution, or production
  deployment in the first tracer.
- Replacing the existing Director Console implementation plan.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — First desktop tracer uses a pywebview bridge

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Implement the first locally runnable Director Console as a Windows-first Python `pywebview` desktop shell that presents a narrow HTML interface and exposes only bounded Python bridge methods for workspace summary, scene loading, Direction submission, Scene Board rendering, and local artifact opening. `.work-studio/` remains canonical. The first tracer does not run a general-purpose local web service or add an application database; a loopback-only service is deferred unless the JS API bridge cannot support the required interface safely. |
| **Authorization** | Director accepted the immediately preceding recommendation with "accept" on 2026-08-24. |
| **Confidence** | medium-high for the tracer fit because the repository already has Python `tools/ws`, `ws direction`, `ws scene-board`, Scene Work Objects, and static HTML projection; unverified until a runnable shell records one Direction through the sanctioned path. |
| **Actor** | director |
| **Revisit trigger** | Reconsider if `pywebview` cannot package cleanly on Windows, cannot enforce a narrow bridge boundary, cannot render the required Scene Board and artifact review surface, cannot expose stale-update conflicts visibly, or fails the SC030 Direction tracer exit criteria. If so, evaluate a Tauri shell with a Python sidecar against the same file-first boundary. |
| **Rationale** | The smallest useful risk test is whether the existing V0 console can become a native local app without replacing Work Studio persistence or broadening authority. A Python desktop shell fits the current Python repository and lets the first tracer reuse sanctioned `tools/ws` write paths before investing in a heavier framework. |

### Decision 2 — Desktop target expands to Windows and macOS

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Revise WO `2026-08-24-004` and its implementation plan so the Director Console desktop software is required to run locally on both Windows and macOS. Preserve the existing `pywebview` bridge and file-first Work Studio persistence, but add macOS launch, read, write, artifact-open, packaging, and verification requirements before release readiness. |
| **Authorization** | Director stated on 2026-08-24: "revise plan based on this `2026-08-24-004`, it will be a desktop software which works on both windows and mac". |
| **Confidence** | medium: current Windows tracer is implemented and verified; pywebview and PyInstaller both support Windows and macOS paths, but macOS launch and packaging are not verified from this Windows machine. |
| **Actor** | director |
| **Revisit trigger** | Reconsider the shell or packaging approach if macOS cannot launch the pywebview window reliably, cannot use the bridge without widening authority, cannot package as a `.app`, or requires release signing/notarization decisions earlier than the tracer boundary allows. |
| **Rationale** | The product target is now a two-platform local desktop app. The previous Windows-first plan is superseded for release readiness, while the verified Windows tracer remains valid evidence toward the broader cross-platform target. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [testimony] | director request 2026-08-24 | Director wants locally runnable desktop software for the Director Console and requested an implementation plan grounded in deliverable 2026-08-23-001-director-console-implementation-plan.md. |
| [system] | repository inspection 2026-08-24 | Current repository already exposes ws direction and ws scene-board, stores Scene Work Objects under .work-studio, and has no desktop shell or local application service. |
| [decision] | director acceptance 2026-08-24 | Director accepted the recommended pywebview desktop tracer boundary with 'accept'; acceptance authorizes recording the design and routing to bounded implementation, not deployment or broader packaging decisions. |
| [system] | bounded implementation 2026-08-24 | Implemented director_console package with pywebview launcher, narrow JS API bridge, workspace-local path validation, Scene Board/SC030 read path, sanctioned ws direction write path, stale-update conflict handling, static desktop UI, and focused unittest coverage. Real SC030 bridge write succeeded and updated SC030 to 2026-08-24T23:09:48Z. |
| [decision] | director revision 2026-08-24 | Director revised the desktop software target from Windows-first to Windows and macOS. Windows tracer evidence remains valid, but release readiness now requires macOS launch/read/write/package verification. |
| [system] | official pywebview and PyInstaller documentation 2026-08-24 | pywebview documents Windows and macOS-compatible desktop webview support and direct JavaScript-Python communication; PyInstaller documents that multi-OS distribution requires building separately on each target operating system. |
| [system] | cross-platform plan revision 2026-08-24 | Revised the implementation plan to require Windows and macOS support. Updated director_console.open_local_artifact to use Windows startfile, macOS open, or xdg-open after workspace-local path validation. Focused unittest suite now covers the macOS launcher branch and passes 7 tests. |
## Open questions

- Which Windows packaging format should follow the tracer if both platform
  checks pass: portable executable bundle first, installer first, or both in
  sequence?
- Which macOS distribution target should follow the tracer if both platform
  checks pass: unsigned local `.app` bundle first, `.dmg` first, or a signed and
  notarized build only after a separate release decision?

## Next move

Verify and implement the cross-platform delta: keep the Windows tracer evidence,
run macOS launch/read/write/artifact-open checks, produce separate Windows and
macOS packaging evidence, and route signing/notarization/installer choices as
separate release decisions.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-24T22:58:46Z — Consequence assessment

- **State:** notice
- **Status:** active
- **Actor:** codex
- **Rationale:** Reversible: yes, the planning artifact and later shell can be removed without changing canonical records. Affects beyond workspace: no during planning and local tracer. Failure affects safety/privacy/money: no for the bounded local tracer. Assigned consequence: meaningful because it guides durable implementation effort.
### 2026-08-24T22:58:47Z — Entered desktop tracer design

- **State:** design
- **Status:** active
- **Actor:** codex
- **Rationale:** The director explicitly requested implementation planning; desktop packaging adds architecture boundaries not accepted by the parent V0 build.
### 2026-08-24T23:03:01Z — Accepted desktop tracer design

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** Director accepted the pywebview bridge tracer; the detailed implementation plan is recorded as an artifact, so the next stage is bounded implementation.
### 2026-08-24T23:03:22Z — Aligned build next move

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** The implementation plan and accepted decision are recorded; body Next move now matches the frontmatter next_action for bounded implementation.
### 2026-08-24T23:10:45Z — Implemented desktop tracer

- **State:** verify
- **Status:** active
- **Actor:** system
- **Rationale:** The accepted pywebview desktop tracer is implemented and focused checks passed: unittest bridge/workspace tests, tools.ws direction and scene-board checks, Work Object validation, pywebview import, desktop launch event loop, and a real SC030 Direction write through the bridge.
### 2026-08-24T23:16:41Z — Revised plan for Windows and macOS desktop target

- **State:** verify
- **Status:** active
- **Actor:** system
- **Rationale:** Director expanded the desktop software target from Windows-first to Windows and macOS. The revised plan preserves the pywebview bridge and Windows tracer evidence while making macOS launch, read, write, artifact-open, and packaging verification required before release readiness.
## Relationships

  REL-2026_08_24_004-001:
    type: implements
    from: wo:2026-08-24-004
    to: wo:2026-08-23-001
    basis: "Desktop delivery scope derived from the accepted Director Console implementation plan"
    created_at: 2026-08-24T22:58:47Z

## artifacts

- `.work-studio/deliverables/2026-08-24-004-director-console-desktop-software-implementation-plan.md` (fingerprint: `f75ffd635b75`, commit: uncommitted at record time) — Detailed implementation plan for the accepted Director Console desktop tracer
- `.work-studio/deliverables/2026-08-24-004-director-console-desktop-software-implementation-plan.md` (fingerprint: `c58cd630ba05`, commit: uncommitted at record time) — Revised Windows and macOS implementation plan for the Director Console desktop software
