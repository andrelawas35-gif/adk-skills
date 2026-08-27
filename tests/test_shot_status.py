"""Focused regression tests for the V1 shot state machine and hierarchy (WO 2026-08-24-006).

Covers the shot-status transition mechanism (``ws shot-status``): a Shot Work
Object moves through blocking → animation → render → review → approved by
updating the ``shot_status`` frontmatter field + History, without touching the
fixed ``ws transition`` lifecycle enum (per the V1 tracer, Decision 2). Also
locks the hierarchy edge parsing that the tracer validated (``ws relation`` /
``ws graph``).
"""

import sys
import tempfile
import unittest
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS_DIR))

from ws.shot_status import transition, SHOT_STATES  # noqa: E402
from ws.graph import _collect_all_edges  # noqa: E402


SHOT_FRONTMATTER = """---
schema_version: 1
id: 2099-03-03-001
title: Test Shot
type: project
status: active
state: notice
consequence: low
sensitivity: ordinary
domain: [architecture]
shot_status: blocking
created_at: 2099-03-03T00:00:00Z
updated_at: 2099-03-03T00:00:00Z
next_action: none
---"""

SHOT_BODY = """
## Intent

Fixture shot for the V1 shot state machine test.

## History
"""


def _write_shot(ws_root: Path, filename: str = "2099-03-03-001-test-shot.md") -> Path:
    objects_dir = ws_root / ".work-studio" / "objects" / "2099" / "03"
    objects_dir.mkdir(parents=True, exist_ok=True)
    path = objects_dir / filename
    path.write_text(SHOT_FRONTMATTER + "\n" + SHOT_BODY, encoding="utf-8")
    return path


class TestShotStatus(unittest.TestCase):
    def test_transition_updates_status_and_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_shot(Path(tmp))
            result = transition(path, "animation")
            self.assertTrue(result["ok"])
            self.assertEqual(result["old_status"], "blocking")
            self.assertEqual(result["new_status"], "animation")
            text = path.read_text(encoding="utf-8")
            self.assertIn("shot_status: animation", text)
            self.assertIn("Shot status: blocking → animation", text)

    def test_full_sequence_to_approved(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_shot(Path(tmp))
            for status in ("animation", "render", "review", "approved"):
                result = transition(path, status)
                self.assertTrue(result["ok"], f"transition to {status} failed")
            text = path.read_text(encoding="utf-8")
            self.assertIn("shot_status: approved", text)
            for old, new in (("blocking", "animation"), ("animation", "render"),
                             ("render", "review"), ("review", "approved")):
                self.assertIn(f"Shot status: {old} → {new}", text)

    def test_invalid_status_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_shot(Path(tmp))
            result = transition(path, "bogus")
            self.assertFalse(result["ok"])
            self.assertIn("Invalid shot status", result["error"])
            # file unchanged
            self.assertIn("shot_status: blocking", path.read_text(encoding="utf-8"))

    def test_valid_states_are_exactly_the_production_set(self):
        self.assertEqual(
            SHOT_STATES, ["blocking", "animation", "render", "review", "approved"]
        )


class TestHierarchyEdgeParsing(unittest.TestCase):
    def test_depends_on_edge_parsed_and_direction_semantics(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws_root = Path(tmp)
            objects_dir = ws_root / ".work-studio" / "objects" / "2099" / "03"
            objects_dir.mkdir(parents=True, exist_ok=True)
            # Shot depends_on Scene (child -> parent), the V1 hierarchy shape.
            body = SHOT_BODY + "\n## Relationships\n\n" + (
                "  REL-2099_03_03_001-001:\n"
                "    type: depends_on\n"
                "    from: wo:2099-03-03-001\n"
                "    to: wo:2099-03-03-002\n"
                "    created_at: 2099-03-03T00:00:00Z\n"
            )
            (objects_dir / "2099-03-03-001-test-shot.md").write_text(
                SHOT_FRONTMATTER + "\n" + body, encoding="utf-8"
            )

            edges = _collect_all_edges(ws_root / ".work-studio" / "objects")
            self.assertEqual(len(edges), 1)
            self.assertEqual(edges[0]["type"], "depends_on")
            self.assertEqual(edges[0]["from"], "wo:2099-03-03-001")
            self.assertEqual(edges[0]["to"], "wo:2099-03-03-002")


if __name__ == "__main__":
    unittest.main()
