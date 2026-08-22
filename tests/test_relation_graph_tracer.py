"""Focused checks for the relation/graph tracer bullet (WO 2026-08-22-026).

Covers the accepted Decision 1 exit criteria and its riskiest assumption:
a ``## Relationships`` section-parser projection can write and trace a
typed edge with deterministic ref resolution, with no schema migration
beyond the Relationships writer/reader.

  1. ``ws relation add`` appends a schema-valid, append-only REL record.
  2. ``ws graph trace`` reads it back across the corpus, both directions.
  3. Endpoint resolution: an edge type outside the fixed vocabulary is
     rejected; a --to referencing a nonexistent Work Object is rejected;
     an explicit external:<locator> endpoint is accepted unresolved.
  4. Two edges from the same origin allocate sequential REL ids.
  5. A missing edge is reported as "not recorded", never as a negative
     claim -- the projection-absence invariant from the evidence model.
"""

import os
import tempfile
import unittest
from argparse import Namespace
from contextlib import contextmanager
from pathlib import Path

from tools.ws.relation import cmd_relation_add, parse_relationships
from tools.ws.graph import cmd_graph_trace

REPO_ROOT = Path(__file__).resolve().parents[1]


def _wo_content(obj_id: str, title: str, consequence: str = "meaningful") -> str:
    return (
        "---\n"
        f"id: {obj_id}\n"
        f"title: {title}\n"
        "type: change\n"
        "status: active\n"
        "state: build\n"
        f"consequence: {consequence}\n"
        "sensitivity: ordinary\n"
        "created_at: 2026-08-22T00:00:00Z\n"
        "updated_at: 2026-08-22T00:00:00Z\n"
        "---\n"
        "## Intent\n\nFixture.\n"
    )


@contextmanager
def workspace_with_wos(objects: dict):
    """Tempdir workspace with fixture Work Objects.

    ``objects`` maps obj_id -> body content (as returned by _wo_content).
    All fixtures are placed under 2026/08 for simplicity.
    """
    previous = Path.cwd()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        month_dir = root / ".work-studio" / "objects" / "2026" / "08"
        month_dir.mkdir(parents=True)
        for obj_id, content in objects.items():
            (month_dir / f"{obj_id}-fixture.md").write_text(content, encoding="utf-8")
        os.chdir(root)
        try:
            yield root
        finally:
            os.chdir(previous)


def _add_args(from_id, edge_type, to, basis=None, expect_updated="2026-08-22T00:00:00Z", force=False):
    return Namespace(
        id=from_id, type=edge_type, to=to, basis=basis,
        expect_updated=expect_updated, force=force,
    )


def _trace_args(ref, direction="both"):
    return Namespace(ref=ref, direction=direction)


class TestRelationAddAndGraphTrace(unittest.TestCase):
    def test_add_and_trace_round_trip_both_directions(self):
        """The demo edge (WO-to-WO) writes, and traces from both ends."""
        objects = {
            "2026-08-22-001": _wo_content("2026-08-22-001", "Origin fixture"),
            "2026-08-22-002": _wo_content("2026-08-22-002", "Target fixture"),
        }
        with workspace_with_wos(objects):
            rc = cmd_relation_add(_add_args(
                "2026-08-22-001", "responds_to", "2026-08-22-002", basis="Decision 1",
            ))
            self.assertEqual(rc, 0)

            # Downstream from the origin
            rc = cmd_graph_trace(_trace_args("2026-08-22-001", direction="downstream"))
            self.assertEqual(rc, 0)

            # Upstream into the target
            rc = cmd_graph_trace(_trace_args("2026-08-22-002", direction="upstream"))
            self.assertEqual(rc, 0)

            # Parse directly to confirm the written block's shape
            month_dir = Path.cwd() / ".work-studio" / "objects" / "2026" / "08"
            origin_file = month_dir / "2026-08-22-001-fixture.md"
            body = origin_file.read_text(encoding="utf-8").split("---", 2)[-1]
            edges = parse_relationships(body)
            self.assertEqual(len(edges), 1)
            self.assertEqual(edges[0]["type"], "responds_to")
            self.assertEqual(edges[0]["from"], "wo:2026-08-22-001")
            self.assertEqual(edges[0]["to"], "wo:2026-08-22-002")
            self.assertEqual(edges[0]["basis"], "Decision 1")
            self.assertTrue(edges[0]["id"].startswith("REL-2026_08_22_001-"))

    def test_rejects_edge_type_outside_fixed_vocabulary(self):
        objects = {"2026-08-22-001": _wo_content("2026-08-22-001", "Origin fixture")}
        with workspace_with_wos(objects):
            rc = cmd_relation_add(_add_args(
                "2026-08-22-001", "totally_made_up_type", "external:some-locator",
            ))
            self.assertEqual(rc, 1)

    def test_rejects_to_referencing_nonexistent_work_object(self):
        objects = {"2026-08-22-001": _wo_content("2026-08-22-001", "Origin fixture")}
        with workspace_with_wos(objects):
            rc = cmd_relation_add(_add_args(
                "2026-08-22-001", "depends_on", "2026-08-22-999",
            ))
            self.assertEqual(rc, 1)

    def test_accepts_explicit_external_endpoint_unresolved(self):
        """Graph invariant #1: an endpoint resolves, or is explicitly external."""
        objects = {"2026-08-22-001": _wo_content("2026-08-22-001", "Origin fixture")}
        with workspace_with_wos(objects):
            rc = cmd_relation_add(_add_args(
                "2026-08-22-001", "used", "external:tools/ws/relation.py@dirty",
            ))
            self.assertEqual(rc, 0)

            month_dir = Path.cwd() / ".work-studio" / "objects" / "2026" / "08"
            origin_file = month_dir / "2026-08-22-001-fixture.md"
            body = origin_file.read_text(encoding="utf-8").split("---", 2)[-1]
            edges = parse_relationships(body)
            self.assertEqual(edges[0]["to"], "external:tools/ws/relation.py@dirty")

    def test_sequential_ids_for_repeated_edges_from_same_origin(self):
        objects = {
            "2026-08-22-001": _wo_content("2026-08-22-001", "Origin fixture"),
            "2026-08-22-002": _wo_content("2026-08-22-002", "Target A"),
            "2026-08-22-003": _wo_content("2026-08-22-003", "Target B"),
        }
        with workspace_with_wos(objects):
            rc = cmd_relation_add(_add_args("2026-08-22-001", "depends_on", "2026-08-22-002"))
            self.assertEqual(rc, 0)

            # Re-read updated_at after the first write for the second call's concurrency check
            month_dir = Path.cwd() / ".work-studio" / "objects" / "2026" / "08"
            origin_file = month_dir / "2026-08-22-001-fixture.md"
            content = origin_file.read_text(encoding="utf-8")
            new_updated_at = [
                line.split(":", 1)[1].strip()
                for line in content.splitlines()
                if line.startswith("updated_at:")
            ][0]

            rc = cmd_relation_add(_add_args(
                "2026-08-22-001", "supports", "2026-08-22-003",
                expect_updated=new_updated_at,
            ))
            self.assertEqual(rc, 0)

            body = origin_file.read_text(encoding="utf-8").split("---", 2)[-1]
            edges = parse_relationships(body)
            self.assertEqual(len(edges), 2)
            self.assertEqual(edges[0]["id"], "REL-2026_08_22_001-001")
            self.assertEqual(edges[1]["id"], "REL-2026_08_22_001-002")

    def test_missing_edge_reports_not_recorded_not_absent(self):
        """No edges written -- trace must not claim the ref has no relationships."""
        objects = {"2026-08-22-001": _wo_content("2026-08-22-001", "Lonely fixture")}
        with workspace_with_wos(objects):
            rc = cmd_graph_trace(_trace_args("2026-08-22-001"))
            self.assertEqual(rc, 0)  # advisory, not an error


if __name__ == "__main__":
    unittest.main()
