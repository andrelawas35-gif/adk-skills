"""Tests for the Phase 5 first-slice edge projection (WO 2026-08-17-007).

Covers deterministic extraction (leading WO-id from prose-carrying values,
canonical-only -- no `.bak-*` phantoms), the NetworkX DiGraph build, invariant
checks #1 (dangling endpoints), #3 (reciprocal agreement), and #4 (acyclic
supersession with direction normalization), #8 (stale locators via target
content identity), #9 (sensitive-body exclusion), the completion invariants
#2/#5/#6/#10, plus byte-stable rebuild (#7) and the Phase 5 queries
(explanation-path and loop-state). Uses a fixture corpus so the checks' failure
paths are proven (the live corpus is expected to be clean).
"""

import tempfile
import unittest
from pathlib import Path

from runtime.projection import (
    CONFORMANCE_DISCLAIMER,
    Edge,
    build_projection,
    check_advisory_cycles,
    check_dangling_endpoints,
    check_edge_kind_pairs,
    check_forbidden_cycles,
    check_reciprocal_agreement,
    check_stale_locators,
    coverage_report,
    explanation_paths,
    extract_edges,
    loop_state,
    render_projection,
    supersession_edges,
)


def _write_object(
    objects_dir: Path,
    wid: str,
    edges: dict,
    sensitivity: str | None = None,
    body: str = "## Intent\n\n",
) -> Path:
    """Write a minimal canonical object file with optional edge fields.

    ``sensitivity`` is written into the frontmatter; ``body`` defaults to an
    Intent section but can carry arbitrary text (e.g. sensitive markers for
    the invariant #9 body-exclusion tests).
    """
    yyyy, mm = wid[:4], wid[5:7]
    d = objects_dir / yyyy / mm
    d.mkdir(parents=True, exist_ok=True)
    lines = [f"id: {wid}"]
    if sensitivity:
        lines.append(f"sensitivity: {sensitivity}")
    lines += [f"{k}: {v}" for k, v in edges.items()]
    frontmatter = "---\n" + "\n".join(lines) + "\n---\n"
    path = d / f"{wid}-fixture.md"
    path.write_text(frontmatter + body)
    return path


class ProjectionTestBase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.objects = Path(self._tmp.name) / "objects"
        self.objects.mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()


class TestDeterministicExtraction(ProjectionTestBase):
    def test_extracts_leading_id_from_prose_value(self):
        _write_object(self.objects, "2026-07-22-003", {})
        _write_object(
            self.objects,
            "2026-07-22-004",
            {
                "responds_to": (
                    "2026-07-22-003 (diagnosis session — "
                    "backtick-wrapped tag fix)"
                )
            },
        )
        edges = extract_edges(self.objects)
        self.assertIn(
            Edge(
                "2026-07-22-004",
                "2026-07-22-003",
                "responds_to",
                None,
                "frontmatter.responds_to",
            ),
            edges,
        )

    def test_excludes_bak_snapshot_phantoms(self):
        src = _write_object(
            self.objects, "2026-07-23-003", {"superseded_by": "2026-07-23-004"}
        )
        _write_object(self.objects, "2026-07-23-004", {"supersedes": "2026-07-23-003"})
        # A stale snapshot carrying an edge to a phantom id must not produce an edge.
        snapshot = src.with_name(src.name + ".bak-20260810T143745Z")
        snapshot.write_text(
            "---\nid: 2026-07-23-003\nsupersedes: 2026-08-99-001\n---\n"
        )
        edges = extract_edges(self.objects)
        self.assertNotIn(Edge("2026-07-23-003", "2026-08-99-001", "supersedes"), edges)

    def test_deterministic_sorted_order(self):
        # Write edges in reverse insertion order; extraction must sort them.
        _write_object(self.objects, "2026-07-22-001", {})
        _write_object(self.objects, "2026-07-22-002", {"unblocks": "2026-07-22-001"})
        _write_object(
            self.objects, "2026-07-23-004", {"supersedes": "2026-07-23-003"}
        )
        _write_object(
            self.objects, "2026-07-23-003", {"superseded_by": "2026-07-23-004"}
        )
        edges = extract_edges(self.objects)
        keys = [(e.source, e.kind, e.target) for e in edges]
        self.assertEqual(keys, sorted(keys))


class TestInvariantChecks(ProjectionTestBase):
    def test_dangling_target_detected(self):
        _write_object(self.objects, "2026-07-22-001", {})
        _write_object(
            self.objects, "2026-07-22-002", {"unblocks": "2026-08-99-001"}
        )
        _g, edges, known = build_projection(self.objects)
        problems = check_dangling_endpoints(edges, known)
        self.assertEqual(len(problems), 1)
        self.assertIn("2026-08-99-001", problems[0])

    def test_live_reciprocal_pair_passes(self):
        _write_object(
            self.objects, "2026-07-23-003", {"superseded_by": "2026-07-23-004"}
        )
        _write_object(
            self.objects, "2026-07-23-004", {"supersedes": "2026-07-23-003"}
        )
        _g, edges, _known = build_projection(self.objects)
        self.assertEqual(check_reciprocal_agreement(edges), [])

    def test_reciprocal_disagreement_detected(self):
        _write_object(
            self.objects, "2026-07-23-003", {"superseded_by": "2026-07-23-004"}
        )
        _write_object(
            self.objects, "2026-07-23-004", {"supersedes": "2026-07-23-005"}
        )
        _write_object(self.objects, "2026-07-23-005", {})
        _g, edges, _known = build_projection(self.objects)
        problems = check_reciprocal_agreement(edges)
        self.assertGreaterEqual(len(problems), 1)


class TestForbiddenCycles(ProjectionTestBase):
    """Invariant #4: acyclic supersession (slice 2, Decision 3)."""

    def test_seeded_supersession_cycle_detected(self):
        _write_object(
            self.objects, "2026-07-01-001", {"supersedes": "2026-07-01-002"}
        )
        _write_object(
            self.objects, "2026-07-01-002", {"supersedes": "2026-07-01-003"}
        )
        _write_object(
            self.objects, "2026-07-01-003", {"supersedes": "2026-07-01-001"}
        )
        _g, edges, _known = build_projection(self.objects)
        problems = check_forbidden_cycles(edges)
        self.assertGreaterEqual(len(problems), 1)
        self.assertIn("supersession cycle", problems[0])

    def test_live_reciprocal_pair_is_not_a_false_cycle(self):
        # supersedes 004->003 + superseded_by 003->004 describe the same fact;
        # normalization must not turn the agreed pair into a 2-cycle.
        _write_object(
            self.objects, "2026-07-23-003", {"superseded_by": "2026-07-23-004"}
        )
        _write_object(
            self.objects, "2026-07-23-004", {"supersedes": "2026-07-23-003"}
        )
        _g, edges, _known = build_projection(self.objects)
        self.assertEqual(check_forbidden_cycles(edges), [])
        norm = [(e.source, e.target) for e in supersession_edges(edges)]
        # Both fields normalize to the newer->older direction; no edge points
        # the other way (which would be the false-cycle direction).
        self.assertIn(("2026-07-23-004", "2026-07-23-003"), norm)
        self.assertNotIn(("2026-07-23-003", "2026-07-23-004"), norm)

    def test_self_loop_supersession_reported(self):
        _write_object(
            self.objects, "2026-07-01-001", {"supersedes": "2026-07-01-001"}
        )
        _g, edges, _known = build_projection(self.objects)
        problems = check_forbidden_cycles(edges)
        self.assertGreaterEqual(len(problems), 1)
        self.assertIn("self-loop supersession", problems[0])

    def test_responds_to_cycle_is_advisory_only(self):
        _write_object(
            self.objects, "2026-07-01-001", {"responds_to": "2026-07-01-002"}
        )
        _write_object(
            self.objects, "2026-07-01-002", {"responds_to": "2026-07-01-001"}
        )
        _g, edges, _known = build_projection(self.objects)
        # Hard acyclicity check passes; the cycle is advisory only.
        self.assertEqual(check_forbidden_cycles(edges), [])
        advisory = check_advisory_cycles(edges)
        self.assertGreaterEqual(len(advisory), 1)
        self.assertIn("responds_to cycle (advisory)", advisory[0])


class TestStaleLocators(ProjectionTestBase):
    """Invariant #8: stale locators via target content identity (slice 3)."""

    def test_changed_target_is_stale(self):
        target = _write_object(self.objects, "2026-07-22-001", {})
        _write_object(
            self.objects, "2026-07-22-002", {"unblocks": "2026-07-22-001"}
        )
        _g, recorded, _k = build_projection(self.objects)
        # Mutate the target's content between the recorded and current projections.
        target.write_text("---\nid: 2026-07-22-001\n---\n## Changed\n\n")
        _g, current, _k = build_projection(self.objects)
        problems = check_stale_locators(recorded, current)
        self.assertEqual(len(problems), 1)
        self.assertIn("stale locator", problems[0])

    def test_unchanged_target_not_stale(self):
        _write_object(self.objects, "2026-07-22-001", {})
        _write_object(
            self.objects, "2026-07-22-002", {"unblocks": "2026-07-22-001"}
        )
        _g, recorded, _k = build_projection(self.objects)
        _g, current, _k = build_projection(self.objects)
        self.assertEqual(check_stale_locators(recorded, current), [])

    def test_dangling_target_has_no_identity_and_no_stale_claim(self):
        _write_object(
            self.objects, "2026-07-22-002", {"unblocks": "2026-08-99-001"}
        )
        _g, edges, _k = build_projection(self.objects)
        self.assertEqual(len(edges), 1)
        self.assertIsNone(edges[0].target_identity)
        self.assertEqual(check_stale_locators(edges, edges), [])

    def test_byte_stable_holds_with_identity(self):
        _write_object(self.objects, "2026-07-22-001", {})
        _write_object(
            self.objects, "2026-07-22-002", {"unblocks": "2026-07-22-001"}
        )
        g1, e1, _ = build_projection(self.objects)
        g2, e2, _ = build_projection(self.objects)
        self.assertEqual(render_projection(g1, e1), render_projection(g2, e2))


class TestQueries(ProjectionTestBase):
    """Slice 4: explanation-path and loop-state queries (Decision 5)."""

    def test_explanation_path_traces_chain_with_kinds(self):
        _write_object(
            self.objects, "2026-07-01-001", {"unblocks": "2026-07-01-002"}
        )
        _write_object(
            self.objects, "2026-07-01-002", {"responds_to": "2026-07-01-003"}
        )
        _write_object(self.objects, "2026-07-01-003", {})
        g, edges, _ = build_projection(self.objects)
        report = explanation_paths(g, edges, "2026-07-01-001", "2026-07-01-003")
        self.assertEqual(len(report), 1)
        self.assertIn("2026-07-01-001 -> 2026-07-01-002", report[0])
        self.assertIn("unblocks", report[0])
        self.assertIn("2026-07-01-002 -> 2026-07-01-003", report[0])
        self.assertIn("responds_to", report[0])

    def test_explanation_path_direct_and_no_path(self):
        _write_object(self.objects, "2026-07-22-001", {})
        _write_object(
            self.objects, "2026-07-22-002", {"unblocks": "2026-07-22-001"}
        )
        _write_object(self.objects, "2026-07-22-005", {})
        g, edges, _ = build_projection(self.objects)
        direct = explanation_paths(g, edges, "2026-07-22-002", "2026-07-22-001")
        self.assertEqual(len(direct), 1)
        self.assertIn("unblocks", direct[0])
        no_path = explanation_paths(g, edges, "2026-07-22-002", "2026-07-22-005")
        self.assertEqual(len(no_path), 1)
        self.assertIn("no path", no_path[0])

    def test_loop_state_reports_reciprocal_pair_2cycle(self):
        _write_object(
            self.objects, "2026-07-23-003", {"superseded_by": "2026-07-23-004"}
        )
        _write_object(
            self.objects, "2026-07-23-004", {"supersedes": "2026-07-23-003"}
        )
        g, edges, _ = build_projection(self.objects)
        report = loop_state(g, edges)
        self.assertEqual(len(report), 1)
        self.assertIn("superseded_by", report[0])
        self.assertIn("supersedes", report[0])

    def test_loop_state_reports_seeded_3cycle_deterministically(self):
        _write_object(
            self.objects, "2026-07-01-001", {"supersedes": "2026-07-01-002"}
        )
        _write_object(
            self.objects, "2026-07-01-002", {"supersedes": "2026-07-01-003"}
        )
        _write_object(
            self.objects, "2026-07-01-003", {"supersedes": "2026-07-01-001"}
        )
        g, edges, _ = build_projection(self.objects)
        r1 = loop_state(g, edges)
        r2 = loop_state(g, edges)
        self.assertEqual(len(r1), 1)
        self.assertEqual(r1, r2)  # deterministic
        self.assertIn("2026-07-01-001 -> 2026-07-01-002", r1[0])

    def test_loop_state_empty_for_acyclic(self):
        _write_object(self.objects, "2026-07-22-001", {})
        _write_object(
            self.objects, "2026-07-22-002", {"unblocks": "2026-07-22-001"}
        )
        g, edges, _ = build_projection(self.objects)
        self.assertEqual(loop_state(g, edges), [])


class TestSensitiveBodyExclusion(ProjectionTestBase):
    """Slice 5: invariant #9 -- sensitive source bodies never leak (Decision 6)."""

    MARKER = "RESTRICTED-BODY-MARKER-9f3a"
    PROMPT = "hidden chain-of-thought"

    def test_restricted_body_marker_absent_from_output(self):
        _write_object(
            self.objects,
            "2026-07-22-001",
            {"responds_to": "2026-07-22-003"},
            sensitivity="restricted",
            body=f"## Hidden reasoning\n{self.MARKER}\n{self.PROMPT}\n",
        )
        _write_object(self.objects, "2026-07-22-003", {})
        g, edges, _ = build_projection(self.objects)
        render = render_projection(g, edges)
        self.assertNotIn(self.MARKER, render)
        self.assertNotIn(self.PROMPT, render)
        # Edges and the graph carry only ids/kinds/identities -- no body text.
        for e in edges:
            self.assertNotIn(self.MARKER, e.target_identity or "")
        self.assertNotIn(self.MARKER, " ".join(g.nodes()))

    def test_render_is_strictly_node_and_edge_lines(self):
        _write_object(self.objects, "2026-07-22-001", {})
        _write_object(
            self.objects, "2026-07-22-002", {"unblocks": "2026-07-22-001"}
        )
        g, edges, _ = build_projection(self.objects)
        for line in render_projection(g, edges).splitlines():
            self.assertTrue(
                line.startswith("#")
                or line.startswith("node ")
                or line.startswith("edge "),
                f"unexpected render line: {line!r}",
            )

    def test_prompt_and_hidden_reasoning_body_text_absent(self):
        _write_object(
            self.objects,
            "2026-07-22-004",
            {"responds_to": "2026-07-22-003"},
            body="## Hidden reasoning\nPROMPT-LEAK-MARKER hidden chain-of-thought\n",
        )
        _write_object(self.objects, "2026-07-22-003", {})
        g, edges, _ = build_projection(self.objects)
        render = render_projection(g, edges)
        self.assertNotIn("PROMPT-LEAK-MARKER", render)
        self.assertNotIn(self.PROMPT, render)


class TestCompletionInvariants(ProjectionTestBase):
    """Slice 6: completion invariants #2/#5/#6/#10 (Decision 7)."""

    def test_undeclared_edge_kind_flagged(self):
        _write_object(self.objects, "2026-07-22-001", {})
        _write_object(
            self.objects, "2026-07-22-002", {"unblocks": "2026-07-22-001"}
        )
        _g, edges, _k = build_projection(self.objects)
        # Live edges all use declared kinds -> clean (WO-only, satisfied by
        # construction per open question 2).
        self.assertEqual(check_edge_kind_pairs(edges), [])
        # A directly-constructed undeclared kind is flagged.
        bogus = [Edge("2026-07-22-001", "2026-07-22-002", "depends_on")]
        problems = check_edge_kind_pairs(bogus)
        self.assertEqual(len(problems), 1)
        self.assertIn("undeclared edge kind", problems[0])

    def test_edges_carry_extraction_rule(self):
        _write_object(self.objects, "2026-07-22-001", {})
        _write_object(
            self.objects, "2026-07-22-002", {"unblocks": "2026-07-22-001"}
        )
        _g, edges, _k = build_projection(self.objects)
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0].extraction_rule, "frontmatter.unblocks")

    def test_missing_edge_reported_as_missing_coverage(self):
        _write_object(self.objects, "2026-07-22-001", {})
        _write_object(
            self.objects, "2026-07-22-002", {"unblocks": "2026-07-22-001"}
        )
        _g, edges, known = build_projection(self.objects)
        report = coverage_report(
            edges,
            known,
            [
                ("2026-07-22-002", "2026-07-22-001"),  # present
                ("2026-07-22-001", "2026-07-22-002"),  # missing
            ],
        )
        self.assertEqual(len(report), 1)
        self.assertIn("missing coverage", report[0])
        self.assertNotIn("not related", report[0])

    def test_render_carries_conformance_disclaimer(self):
        _write_object(self.objects, "2026-07-22-001", {})
        _write_object(
            self.objects, "2026-07-22-002", {"unblocks": "2026-07-22-001"}
        )
        g, edges, _ = build_projection(self.objects)
        render = render_projection(g, edges)
        self.assertIn("does not assert evidence adequacy", render)
        self.assertTrue(render.startswith(CONFORMANCE_DISCLAIMER))


class TestByteStableRebuild(ProjectionTestBase):
    def test_two_runs_render_identical_bytes(self):
        _write_object(self.objects, "2026-07-22-001", {})
        _write_object(self.objects, "2026-07-22-002", {"unblocks": "2026-07-22-001"})
        _write_object(
            self.objects, "2026-07-23-003", {"superseded_by": "2026-07-23-004"}
        )
        _write_object(
            self.objects, "2026-07-23-004", {"supersedes": "2026-07-23-003"}
        )
        g1, edges1, _ = build_projection(self.objects)
        g2, edges2, _ = build_projection(self.objects)
        self.assertEqual(render_projection(g1, edges1), render_projection(g2, edges2))


if __name__ == "__main__":
    unittest.main()
