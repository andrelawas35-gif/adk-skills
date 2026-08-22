"""Engineering operating-pipeline graph tracer tests (WO 2026-08-22-023)."""

import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pydantic import ValidationError

from runtime.engineering import (
    EngineeringHandoffEnvelope,
    build_engineering_skill_graph,
    engineering_path,
    load_engineering_pipeline_spec,
    normalize_skill_name,
    propose_engineering_handoff,
    route_engineering_frontier,
)
from runtime.graph import inspect_phase6, phase6_branch_a, phase6_dispatch, run_phase6


class EngineeringGraphProjectionTests(unittest.TestCase):
    def test_pipeline_reference_builds_valid_engineering_graph(self):
        spec = load_engineering_pipeline_spec()
        graph = build_engineering_skill_graph(spec)

        self.assertIn("design-tracer-bullet", graph)
        self.assertIn("engineering-verify-release-evidence", graph)
        self.assertIn("operations-deploy-with-recovery", graph)
        self.assertEqual(
            graph.nodes["engineering-verify-release-evidence"]["governance_domain"],
            "engineering",
        )
        self.assertEqual(
            graph.nodes["operations-deploy-with-recovery"]["governance_domain"],
            "operations",
        )
        self.assertTrue(
            graph.has_edge(
                "engineering-verify-release-evidence",
                "operations-deploy-with-recovery",
            )
        )

    def test_adapter_names_normalize_to_core_runtime_names(self):
        self.assertEqual(
            normalize_skill_name("alawas-engineering-verify-release-evidence"),
            "engineering-verify-release-evidence",
        )
        self.assertEqual(
            normalize_skill_name("engineering-verify-release-evidence"),
            "engineering-verify-release-evidence",
        )

    def test_frontier_router_uses_canonical_ownership_map(self):
        self.assertEqual(
            route_engineering_frontier("CI failure and verification gap").owning_skill,
            "engineering-verify-release-evidence",
        )
        self.assertEqual(
            route_engineering_frontier("deployment rollback recovery plan").owning_skill,
            "operations-deploy-with-recovery",
        )
        low = route_engineering_frontier("strange undefined frontier")
        self.assertEqual(low.owning_skill, "engineering-implement-bounded-change")
        self.assertEqual(low.confidence, "low")

    def test_engineering_path_follows_pipeline_order(self):
        path = engineering_path(
            "alawas-engineering-implement-bounded-change",
            "operations-diagnose-production-incident",
        )
        self.assertEqual(path[0], "engineering-implement-bounded-change")
        self.assertEqual(path[-1], "operations-diagnose-production-incident")
        self.assertIn("engineering-verify-release-evidence", path)
        self.assertIn("operations-deploy-with-recovery", path)


class EngineeringHandoffEnvelopeTests(unittest.TestCase):
    def test_handoff_envelope_validates_target_domain(self):
        envelope = EngineeringHandoffEnvelope(
            handoff_id="HANDOFF-engineering-test",
            work_object_id="2026-08-22-023",
            lifecycle_state="build",
            current_frontier="implementation completed",
            from_skill="alawas-engineering-implement-bounded-change",
            to_skill="alawas-engineering-verify-release-evidence",
            governance_domain="engineering",
            evidence_resolved=["bounded implementation completed locally"],
            next_gap="CI failure and verification gap",
            same_work_object=True,
            authority_boundary="read-only-propose",
            graph_path=[
                "alawas-engineering-implement-bounded-change",
                "alawas-engineering-verify-release-evidence",
            ],
        )

        self.assertEqual(envelope.from_skill, "engineering-implement-bounded-change")
        self.assertEqual(envelope.to_skill, "engineering-verify-release-evidence")
        self.assertEqual(
            envelope.graph_path,
            [
                "engineering-implement-bounded-change",
                "engineering-verify-release-evidence",
            ],
        )

    def test_handoff_envelope_rejects_domain_mismatch(self):
        with self.assertRaises(ValidationError):
            EngineeringHandoffEnvelope(
                handoff_id="HANDOFF-engineering-bad",
                work_object_id="2026-08-22-023",
                lifecycle_state="build",
                current_frontier="implementation completed",
                from_skill="engineering-implement-bounded-change",
                to_skill="engineering-verify-release-evidence",
                governance_domain="operations",
                evidence_resolved=[],
                next_gap="CI failure and verification gap",
                same_work_object=True,
                authority_boundary="read-only-propose",
                graph_path=[
                    "engineering-implement-bounded-change",
                    "engineering-verify-release-evidence",
                ],
            )

    def test_propose_engineering_handoff_routes_next_gap(self):
        envelope = propose_engineering_handoff(
            handoff_id="HANDOFF-engineering-auto",
            work_object_id="2026-08-22-023",
            lifecycle_state="build",
            current_frontier="implementation completed",
            from_skill="engineering-implement-bounded-change",
            evidence_resolved=["local edit completed"],
            next_gap="CI failure and verification gap",
            same_work_object=True,
            authority_boundary="read-only-propose",
        )

        self.assertEqual(envelope.to_skill, "engineering-verify-release-evidence")
        self.assertEqual(envelope.governance_domain, "engineering")
        self.assertEqual(envelope.graph_path[-1], "engineering-verify-release-evidence")

    def test_propose_engineering_handoff_routes_operations_gap(self):
        envelope = propose_engineering_handoff(
            handoff_id="HANDOFF-engineering-ops",
            work_object_id="2026-08-22-023",
            lifecycle_state="release",
            current_frontier="release evidence completed",
            from_skill="engineering-verify-release-evidence",
            evidence_resolved=["verification evidence sufficient"],
            next_gap="deployment rollback recovery plan",
            same_work_object=True,
            authority_boundary="governed",
        )

        self.assertEqual(envelope.to_skill, "operations-deploy-with-recovery")
        self.assertEqual(envelope.governance_domain, "operations")


class Phase6EngineeringDispatchIntegrationTests(unittest.TestCase):
    def setUp(self):
        self._tmp = Path(tempfile.mkdtemp())
        self.wo_path = self._tmp / (
            "2026-08-22-024-integrate-engineering-operating-pipeline-routing.md"
        )
        self.wo_path.write_text(
            """---
schema_version: 1
id: 2026-08-22-024
title: Engineering verification handoff
type: change
status: active
state: build
consequence: meaningful
sensitivity: ordinary
engineering_scope: true
created_at: 2026-08-22T00:00:00Z
updated_at: 2026-08-22T00:00:00Z
next_action: CI failure and verification gap
---
## Intent

Engineering operating pipeline dispatch fixture.

## Open questions

- CI failure and verification gap
""",
            encoding="utf-8",
        )

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_phase6_dispatch_uses_engineering_router_for_engineering_work_object(self):
        with patch("runtime.graph._find_work_object", return_value=self.wo_path):
            result = phase6_dispatch(
                {"work_object_id": "2026-08-22-024", "thread_id": "phase6-engineering"}
            )

        self.assertEqual(
            "engineering-verify-release-evidence",
            result["handoff_envelope"]["to_skill"],
        )
        self.assertEqual(
            "engineering", result["handoff_envelope"]["governance_domain"]
        )
        self.assertEqual(
            "engineering-verify-release-evidence",
            result["engineering_handoff_envelope"]["to_skill"],
        )
        self.assertEqual(
            "engineering-verify-release-evidence",
            result["engineering_route_result"]["owning_skill"],
        )

    def test_phase6_branches_honor_engineering_dispatch_route(self):
        with patch("runtime.graph._find_work_object", return_value=self.wo_path):
            dispatch = phase6_dispatch(
                {"work_object_id": "2026-08-22-024", "thread_id": "phase6-engineering"}
            )
            branch = phase6_branch_a(
                {
                    "work_object_id": "2026-08-22-024",
                    "thread_id": "phase6-engineering",
                    **dispatch,
                }
            )

        self.assertEqual(
            "engineering-verify-release-evidence",
            branch["branch_a_receipt"]["proposed_next_skill"],
        )

    def test_phase6_checkpoint_inspection_exposes_engineering_handoff(self):
        checkpoint_db = self._tmp / "phase6-engineering.sqlite"
        with patch("runtime.graph._find_work_object", return_value=self.wo_path):
            result = run_phase6(
                "2026-08-22-024", "phase6-engineering-e2e", checkpoint_db
            )

        self.assertEqual("engineering-verify-release-evidence", result["join_proposal"])
        state = inspect_phase6("phase6-engineering-e2e", checkpoint_db)
        self.assertTrue(state["has_engineering_handoff_envelope"])
        self.assertEqual(
            "engineering-verify-release-evidence",
            state["engineering_route_result"]["owning_skill"],
        )

    def test_phase6_dispatch_prefers_explicit_engineering_scope_true(self):
        explicit_path = self._tmp / "explicit-engineering-scope.md"
        explicit_path.write_text(
            """---
schema_version: 1
id: 2026-08-22-024
title: Scope metadata fixture
type: change
status: active
state: build
consequence: meaningful
sensitivity: ordinary
engineering_scope: true
created_at: 2026-08-22T00:00:00Z
updated_at: 2026-08-22T00:00:00Z
next_action: deployment rollback recovery plan
---
## Intent

No domain words needed here.
""",
            encoding="utf-8",
        )

        with patch("runtime.graph._find_work_object", return_value=explicit_path):
            result = phase6_dispatch(
                {"work_object_id": "2026-08-22-024", "thread_id": "explicit-true"}
            )

        self.assertEqual(
            "operations-deploy-with-recovery",
            result["engineering_handoff_envelope"]["to_skill"],
        )
        self.assertEqual("operations", result["handoff_envelope"]["governance_domain"])

    def test_phase6_dispatch_prefers_explicit_engineering_scope_false(self):
        explicit_path = self._tmp / "explicit-not-engineering-scope.md"
        explicit_path.write_text(
            """---
schema_version: 1
id: 2026-08-22-024
title: Engineering verification fixture explicitly disabled
type: change
status: active
state: build
consequence: meaningful
sensitivity: ordinary
engineering_scope: false
created_at: 2026-08-22T00:00:00Z
updated_at: 2026-08-22T00:00:00Z
next_action: CI failure and verification gap
---
## Intent

This fixture contains engineering words but explicitly opts out.
""",
            encoding="utf-8",
        )

        with patch("runtime.graph._find_work_object", return_value=explicit_path):
            result = phase6_dispatch(
                {"work_object_id": "2026-08-22-024", "thread_id": "explicit-false"}
            )

        self.assertNotIn("engineering_handoff_envelope", result)
        self.assertEqual(
            "implement-bounded-change", result["handoff_envelope"]["to_skill"]
        )

    def test_phase6_dispatch_preserves_business_precedence(self):
        both_path = self._tmp / "business-and-engineering-scope.md"
        both_path.write_text(
            """---
schema_version: 1
id: 2026-08-22-024
title: Business and engineering scope fixture
type: change
status: active
state: build
consequence: meaningful
sensitivity: ordinary
business_scope: true
engineering_scope: true
created_at: 2026-08-22T00:00:00Z
updated_at: 2026-08-22T00:00:00Z
next_action: value metric and package boundary
---
## Intent

Business scope should keep its existing precedence.
""",
            encoding="utf-8",
        )

        with patch("runtime.graph._find_work_object", return_value=both_path):
            result = phase6_dispatch(
                {"work_object_id": "2026-08-22-024", "thread_id": "business-first"}
            )

        self.assertIn("business_handoff_envelope", result)
        self.assertNotIn("engineering_handoff_envelope", result)
        self.assertEqual(
            "business-design-pricing-and-packaging",
            result["handoff_envelope"]["to_skill"],
        )


if __name__ == "__main__":
    unittest.main()
