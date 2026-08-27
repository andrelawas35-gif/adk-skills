# Director Console Desktop Software Implementation Plan

Work Object: `2026-08-24-004`
Parent Work Object: `2026-08-23-001`
Revised: 2026-08-24

## Accepted Boundary

Build the locally runnable Director Console as a Windows and macOS Python
desktop application using `pywebview`. The shell presents a narrow HTML
interface and talks to Python through an explicit JS API bridge. Work Studio
files remain the canonical state; the desktop app does not introduce SQLite, a
parallel store, a general-purpose local server, or a new authority path.

The tracer already proved the first half on Windows: the existing Director
Console V0 can become a native local app that reads Scene Board state and
records one Direction through the sanctioned `tools/ws` path. The revised plan
adds a second required proof: the same app must launch, read, write, and package
on macOS without changing canonical persistence or widening the bridge.

## Revision Basis

- [decision] The director revised the product requirement on 2026-08-24: the
  desktop software must work on both Windows and macOS.
- [system] The current implementation uses `pywebview`, which documents
  cross-platform support and direct JavaScript-to-Python communication without
  requiring HTTP or REST.
- [system] PyInstaller documentation says multi-OS distribution requires
  bundling separately on each target OS. This means Windows and macOS packaging
  are sibling build jobs, not one cross-compiled artifact.
- [inference] The accepted `pywebview` bridge remains the right first shell
  because it preserves the file-first Work Studio model and avoids a new local
  server; the main revision is platform verification and packaging, not a
  framework replacement.

## Product Shape

The first screen is the working console, not a landing page. It should open to a
dense, calm operational surface with:

- Scene Board navigation for available Scene Work Objects.
- Current scene detail, starting with SC030.
- Artifact review pane for existing local projections and image outputs.
- Direction composer for canon-establishing input.
- Visible status, conflict, and validation messages.
- Restart-safe behavior because durable state remains under `.work-studio/`.

## Proposed File Layout

```text
director_console/
  __init__.py
  __main__.py
  app.py
  bridge.py
  workspace.py
  static/
    index.html
    styles.css
    app.js
tests/
  test_director_console_bridge.py
  test_director_console_workspace.py
```

## Runtime Architecture

`director_console.__main__` launches the app on Windows and macOS. `app.py`
creates the `pywebview` window, loads the local HTML interface, and exposes a
single bridge object.

`bridge.py` owns the JS API surface. It must not expose arbitrary shell access.
Its methods call narrow Python functions that either read workspace files or
delegate mutations to existing `tools/ws` commands or equivalent sanctioned
internal APIs.

`workspace.py` discovers and validates the Work Studio root, resolves only
paths beneath that root, and rejects external path traversal.

The Scene Board path reuses current Work Studio projection behavior. The app may
read `.work-studio/scene-board.html` or call the existing Scene Board renderer,
but it must not fork a second canonical representation.

Platform-specific behavior stays behind the Python boundary. Opening a local
artifact uses Windows `startfile` on Windows and macOS `open` on macOS after the
path is proven to be workspace-local.

## Bridge Contract

The bridge exposes only these methods:

- `get_workspace_summary()` returns active Work Object identifiers, Scene Board
  availability, and diagnostic state.
- `get_scene(scene_id)` returns one scene summary, relevant artifact paths, and
  the current `updated_at` used for stale-write protection.
- `submit_direction(scene_id, text, expected_updated_at)` records one Direction
  through the sanctioned Work Studio path and returns the updated scene state or
  a structured conflict.
- `render_scene_board()` refreshes or reads the Scene Board projection.
- `open_local_artifact(path)` opens a workspace-local artifact after path
  validation.

Every bridge response should be structured JSON-like data with `ok`, `data`,
and `error` fields so the interface can present failure states without guessing.

## Write Path

Direction submission is the only canonical write in the tracer. It must
preserve these rules:

- Require non-empty human-authored text.
- Require `expected_updated_at` for stale-state detection.
- Use the existing `ws direction` behavior or its sanctioned internal path.
- Append evidence/history through Work Studio mechanisms, not direct table
  editing.
- Return conflict information instead of overwriting when the scene changed.

## Failure Behavior

On launch failure, show a diagnostic window or terminal-free error explaining
the missing workspace, missing Scene Board, missing Python runtime, invalid Work
Object state, or platform WebView issue.

On Direction failure, leave files unchanged where the underlying command
rejects the operation. The UI should keep the director's text in the composer
and display the exact recoverable next step.

On stale state, block the write and show the current scene timestamp versus the
submitted timestamp.

Logs should be local, minimal, and non-canonical. They can record command names,
exit status, workspace-relative paths, platform name, and exception classes, but
not secrets or full unrestricted environment output.

## Verification Plan

Windows verification:

- Run `uv run --python 3.11 python -m tools.ws direction --help`.
- Run `uv run --python 3.11 python -m tools.ws scene-board --help`.
- Unit-test workspace path validation, bridge response shape, stale-update
  rejection, and macOS artifact launcher selection.
- Launch the desktop app locally and confirm the window opens without a
  manually started terminal.
- Use SC030 to record one test Direction through the UI or bridge and verify
  the durable record appears under `.work-studio/`.
- Close and reopen the app and confirm the recorded state is still present.

macOS verification:

- Create a fresh Python 3.11 environment on macOS, preferably using Homebrew
  Python rather than the system Python.
- Run the repository's accepted dependency setup.
- Run the same bridge/workspace unit tests.
- Run `python -m director_console` and confirm the `pywebview` window opens,
  receives keyboard focus, and can read SC030 or an equivalent test fixture.
- Record one non-production test Direction against a disposable Scene Work
  Object or a fresh test fixture, then verify `.work-studio/` is the only
  canonical persistence path.
- Confirm local artifact opening uses macOS `open` and rejects paths outside
  the workspace.
- Record any macOS-only WebView, focus, permissions, quarantine, or signing
  issue before packaging.

## Packaging Plan

Phase 1 packages for local developer use on both platforms:

- Keep `python -m director_console` as the development launch command.
- Add Windows and macOS launcher scripts only if the repository already has a
  launcher convention or a packaging build script is accepted later.
- Keep packaging reversible and avoid signing, auto-update, public
  distribution, notarization, or installer decisions.

Phase 2 follows only after both platform tracers pass:

- Bundle separately on Windows and macOS with PyInstaller or an equivalent
  Python packager; do not assume one OS can produce the other's distributable.
- Produce a portable Windows build and a macOS `.app` bundle first.
- Decide Windows installer, macOS `.dmg`, code signing, notarization, icon,
  shortcuts, and update channel separately.
- Treat signing/notarization as a release decision, not part of the tracer.

## Rollback

Remove the `director_console/` package, its tests, and any launcher or packaging
entry added for the tracer. No migration is needed because the app does not own
canonical state. Any Direction intentionally recorded during verification
remains a Work Studio record unless separately reversed through sanctioned Work
Studio processes.

## Exit Criteria

The cross-platform tracer is complete when:

- A native Windows desktop window opens the Director Console without manually
  starting a terminal.
- A native macOS desktop window opens the Director Console without manually
  starting a terminal.
- SC030 or an equivalent fixture loads from existing Work Studio files on both
  platforms.
- One Direction is recorded through the sanctioned path on Windows and one
  equivalent write is verified on macOS.
- Restart preserves durable state in `.work-studio/` on both platforms.
- Stale updates produce a visible conflict rather than an overwrite.
- Workspace-local artifact opening works on Windows and macOS and rejects
  outside-workspace paths.
- Focused Direction, Scene Board, bridge, and workspace checks pass.

If these pass, route the Work Object toward broader desktop hardening and
packaging decisions. If macOS fails because the bridge is too narrow,
unpackageable, or unreliable under the native WebView, reopen the shell
decision and compare Tauri plus a Python sidecar against the same file-first
constraints.
