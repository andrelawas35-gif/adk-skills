import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from director_console.workspace import DirectionConflict, WorkStudioWorkspace


def _scene_text(updated_at="2026-08-24T00:00:00Z"):
    return f"""---
schema_version: 1
id: 2026-08-23-004
title: SC030 - Mara and Leo market conversation
type: project
status: active
state: explore
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-23T00:00:00Z
updated_at: {updated_at}
next_action: Test scene.
---
## Intent

Scene tracer.

## Scene Thesis

- **want**: Mara wants Leo to say what he noticed.

## Screenplay

### Story

Mara and Leo talk in the market.

### Direction

Hold wide and quiet.

## Director Layer

| Beat | Screenplay | Director Intent | Performance | Production |
|------|------------|-----------------|-------------|------------|
| 01 | Mara waits. | Hold tension. | Still. | Wide. |

## Evidence ledger

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | test | Existing row |

## Open questions

- None.

## History

### 2026-08-23T00:00:00Z - Created

- **State:** explore
- **Status:** active
- **Actor:** test
- **Rationale:** fixture
"""


class DirectorConsoleWorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.workspace_root = Path(self.tmp.name)
        objects = self.workspace_root / ".work-studio" / "objects" / "2026" / "08"
        objects.mkdir(parents=True)
        self.scene_file = objects / "2026-08-23-004-sc030.md"
        self.scene_file.write_text(_scene_text(), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_workspace_rejects_paths_outside_root(self):
        workspace = WorkStudioWorkspace(self.workspace_root)

        with self.assertRaises(ValueError):
            workspace.resolve_workspace_path("../outside.txt")

    def test_get_scene_reads_sc030_shape(self):
        workspace = WorkStudioWorkspace(self.workspace_root)

        scene = workspace.get_scene("2026-08-23-004")

        self.assertEqual(scene["id"], "2026-08-23-004")
        self.assertEqual(scene["updated_at"], "2026-08-24T00:00:00Z")
        self.assertEqual(
            scene["thesis"]["want"],
            "Mara wants Leo to say what he noticed.",
        )
        self.assertEqual(scene["director_layer"][0]["Beat"], "01")

    def test_submit_direction_blocks_stale_update(self):
        workspace = WorkStudioWorkspace(self.workspace_root)

        with self.assertRaises(DirectionConflict) as caught:
            workspace.submit_direction(
                "2026-08-23-004",
                "Keep the wide frame.",
                "2026-08-23T00:00:00Z",
            )

        self.assertEqual(
            caught.exception.payload["actual_updated_at"],
            "2026-08-24T00:00:00Z",
        )

    def test_submit_direction_uses_sanctioned_cli_path(self):
        calls = []

        def runner(cmd, **kwargs):
            calls.append((cmd, kwargs))
            self.scene_file.write_text(
                _scene_text(updated_at="2026-08-24T00:01:00Z"),
                encoding="utf-8",
            )
            return subprocess.CompletedProcess(
                cmd,
                0,
                stdout="recorded",
                stderr="",
            )

        workspace = WorkStudioWorkspace(self.workspace_root, runner=runner)
        result = workspace.submit_direction(
            "2026-08-23-004",
            "Keep the wide frame.",
            "2026-08-24T00:00:00Z",
        )

        self.assertEqual(result["scene"]["updated_at"], "2026-08-24T00:01:00Z")
        self.assertEqual(
            calls[0][0][1:5],
            ["-m", "tools.ws", "direction", "--text"],
        )
        self.assertEqual(calls[0][1]["cwd"], self.workspace_root)

    def test_open_local_artifact_uses_macos_open_launcher(self):
        calls = []
        artifact = self.workspace_root / ".work-studio" / "scene-board.html"
        artifact.write_text("<html></html>", encoding="utf-8")

        def runner(cmd, **kwargs):
            calls.append((cmd, kwargs))
            return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

        workspace = WorkStudioWorkspace(self.workspace_root, runner=runner)
        with patch("director_console.workspace.platform.system", return_value="Darwin"):
            result = workspace.open_local_artifact(".work-studio/scene-board.html")

        self.assertEqual(result["launcher"], "open")
        self.assertEqual(calls[0][0][0], "open")


if __name__ == "__main__":
    unittest.main()
