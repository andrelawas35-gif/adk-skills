"""Focused regression tests for the Director Console V0 foundation.

WO 2026-08-23-001 (Director Console) — bounded change under
alawas-engineering-implement-bounded-change, director-authorized on
2026-08-24 (option 2: add a focused regression test for the scene-board +
direction V0 path).

Covers the two V0 paths built by the SC030 tracer (plan section 7 V0 table):

  1. Direction input parsing: director prose -> structured Direction object
     (``ws direction``). Includes the single-line evidence serialization guard
     that fixes Incident WO 2026-08-23-005 / Change WO 2026-08-23-006.
  2. Scene Board HTML projection: Scene Work Objects (those with a
     ``## Screenplay`` section) -> ``.work-studio/scene-board.html``
     (``ws scene-board``), following the same read-only projection pattern as
     ``command_center.py``.
"""

import sys
import tempfile
import unittest
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS_DIR))

from ws.direction import (  # noqa: E402
    parse_direction,
    format_direction,
    format_direction_yaml,
    format_direction_single_line,
)
from ws.scene_board import generate as generate_scene_board  # noqa: E402


SCENE_FRONTMATTER = """---
schema_version: 1
id: 2099-01-01-001
title: Test Scene — alpha and beta exchange
type: project
status: active
state: explore
consequence: meaningful
sensitivity: ordinary
domain: [ideation]
created_at: 2099-01-01T00:00:00Z
updated_at: 2099-01-01T00:00:00Z
next_action: none
---"""

SCENE_BODY = """
## Intent

A minimal Scene Work Object for regression-testing the Scene Board projection.

## Scene Thesis

- **Thesis:** alpha hides recognition.
- **Turn:** beta reveals they already know.

## Screenplay

### Layer A — Story

A quiet room. Alpha pours tea. Beta enters.

### Layer B — Drama

Beta is testing whether Alpha reacts to the name.

### Layer C — Direction

The shift from ordinary to dangerous happens without anyone announcing it.

### Layer D — Realization

- **Location:** quiet room, warm light
- **Camera language:** wide to close as tension rises

## Director Layer

| Beat | Screenplay | Director Intent | Performance | Production |
|------|-----------|-----------------|-------------|------------|
| 01 | Alpha pours tea. | Ordinary day. | relaxed | camera: WS, audio: room tone |
| 02 | Beta enters. | Tension begins. | guarded | camera: MCU, audio: low drone |

## Evidence ledger

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | test | Scene fixture |

## Next move

Verify the Scene Board projection.
"""

NON_SCENE_FRONTMATTER = """---
schema_version: 1
id: 2099-01-01-002
title: Not a Scene Object
type: inquiry
status: active
state: notice
consequence: low
sensitivity: ordinary
domain: [ideation]
created_at: 2099-01-01T00:00:00Z
updated_at: 2099-01-01T00:00:00Z
next_action: none
---"""

NON_SCENE_BODY = """
## Intent

A Work Object without a Screenplay section — must be excluded from the board.

## Next move

Nothing.
"""


def _write_scene_wo(ws_root: Path) -> Path:
    """Create a Scene Work Object (with ## Screenplay) in a temp workspace."""
    objects_dir = ws_root / ".work-studio" / "objects" / "2099" / "01"
    objects_dir.mkdir(parents=True, exist_ok=True)
    path = objects_dir / "2099-01-01-001-alpha-beta.md"
    path.write_text(SCENE_FRONTMATTER + "\n" + SCENE_BODY, encoding="utf-8")
    return path


def _write_non_scene_wo(ws_root: Path) -> Path:
    """Create a Work Object with no Screenplay section in a temp workspace."""
    objects_dir = ws_root / ".work-studio" / "objects" / "2099" / "01"
    objects_dir.mkdir(parents=True, exist_ok=True)
    path = objects_dir / "2099-01-01-002-not-a-scene.md"
    path.write_text(NON_SCENE_FRONTMATTER + "\n" + NON_SCENE_BODY, encoding="utf-8")
    return path


class TestDirectionParsing(unittest.TestCase):
    """V0 Direction input parsing: prose -> structured Direction object."""

    def test_parses_protect_change_avoid_from_director_prose(self):
        """The SC030-style direction structures into the expected fields."""
        d = parse_direction(
            "Keep the wide framing and silence, but make the recognition "
            "less obvious. Avoid melodrama."
        )
        self.assertEqual(d["mode"], "command")
        self.assertIn("wide framing", d["protect"])
        self.assertIn("silence", d["protect"])
        self.assertIn("less obvious", d["change"])
        self.assertIn("melodrama", d["avoid"])

    def test_detects_direction_mode_for_prose_without_verb_prefix(self):
        """Free-form direction prose defaults to 'direction' mode."""
        d = parse_direction("This scene feels too sentimental.")
        self.assertEqual(d["mode"], "direction")

    def test_detects_inquiry_mode_for_question(self):
        """A 'why' question is classified as an inquiry, not a command."""
        d = parse_direction("Why is this scene so slow?")
        self.assertEqual(d["mode"], "inquiry")

    def test_protect_from_dont_change(self):
        """'Don't change X' populates the protect field."""
        d = parse_direction("Don't change the framing.")
        self.assertIn("the framing", d["protect"])

    def test_format_direction_readable_form(self):
        """Human-readable form carries the structured fields."""
        d = parse_direction(
            "Keep the wide framing and silence, but make the recognition "
            "less obvious. Avoid melodrama."
        )
        text = format_direction(d)
        self.assertIn("Protect: wide framing, silence", text)
        self.assertIn("Change: less obvious", text)
        self.assertIn("Avoid: melodrama", text)

    def test_format_direction_yaml_block(self):
        """YAML form is embeddable as a structured block."""
        d = parse_direction(
            "Keep the wide framing and silence, but make the recognition "
            "less obvious. Avoid melodrama."
        )
        yaml_text = format_direction_yaml(d)
        self.assertIn("mode: command", yaml_text)
        self.assertIn("protect: [wide framing, silence]", yaml_text)

    def test_single_line_serialization_stays_one_physical_line(self):
        """Regression guard for Incident 2026-08-23-005: evidence rows must
        not leak multi-line text outside the markdown table."""
        d = parse_direction(
            "Keep the wide framing and silence, but make the recognition "
            "less obvious. Avoid melodrama."
        )
        single = format_direction_single_line(d)
        self.assertNotIn("\n", single)
        self.assertIn("<br>", single)
        self.assertIn("Protect: wide framing, silence", single)


class TestSceneBoardProjection(unittest.TestCase):
    """V0 Scene Board HTML projection: Scene WOs -> scene-board.html."""

    def test_generate_renders_layers_and_beat_table(self):
        """A Scene Work Object renders with all four layer tabs + beat table."""
        with tempfile.TemporaryDirectory() as tmp:
            ws_root = Path(tmp)
            _write_scene_wo(ws_root)

            summary = generate_scene_board(ws_root)

            self.assertEqual(summary["scenes"], 1)
            self.assertTrue(summary["out_path"].exists())
            html = summary["out_path"].read_text(encoding="utf-8")

            # Scene identity
            self.assertIn("2099-01-01-001", html)
            self.assertIn("Test Scene — alpha and beta exchange", html)
            # Four screenplay layer tabs
            for layer in (
                "Layer A — Story",
                "Layer B — Drama",
                "Layer C — Direction",
                "Layer D — Realization",
            ):
                self.assertIn(layer, html)
            # Director Layer beat table headers + a beat cell
            for header in ("Beat", "Screenplay", "Director Intent",
                           "Performance", "Production"):
                self.assertIn(header, html)
            self.assertIn("Alpha pours tea.", html)
            # Scene Thesis is surfaced
            self.assertIn("alpha hides recognition", html)

    def test_non_scene_objects_are_excluded(self):
        """Work Objects without a ## Screenplay section are not rendered."""
        with tempfile.TemporaryDirectory() as tmp:
            ws_root = Path(tmp)
            _write_scene_wo(ws_root)
            _write_non_scene_wo(ws_root)

            summary = generate_scene_board(ws_root)
            html = summary["out_path"].read_text(encoding="utf-8")

            self.assertEqual(summary["scenes"], 1)
            self.assertNotIn("Not a Scene Object", html)
            self.assertNotIn("2099-01-01-002", html)

    def test_empty_workspace_renders_empty_message(self):
        """No Scene Work Objects -> the board shows its empty state."""
        with tempfile.TemporaryDirectory() as tmp:
            ws_root = Path(tmp)
            (ws_root / ".work-studio" / "objects").mkdir(parents=True)

            summary = generate_scene_board(ws_root)
            html = summary["out_path"].read_text(encoding="utf-8")

            self.assertEqual(summary["scenes"], 0)
            self.assertIn("No scenes found", html)


if __name__ == "__main__":
    unittest.main()
