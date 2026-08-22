"""Business operating-pipeline graph tracer tests (WO 2026-08-22-016/018)."""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pydantic import ValidationError

from runtime.graph import inspect_phase6, phase6_branch_a, phase6_dispatch, run_phase6
from runtime.business import (
    BusinessHandoffEnvelope,
    build_business_skill_graph,
    business_path,
    inspect_business_router,
    load_business_pipeline_spec,
    normalize_skill_name,
    propose_business_handoff,
    route_business_frontier,
    run_business_router,
)


class BusinessGraphProjectionTests(unittest.TestCase):
    def test_pipeline_reference_builds_valid_business_graph(self):
        spec = load_business_pipeline_spec()
        graph = build_business_skill_graph(spec)

        self.assertIn("business-formulate-strategy", graph)
        self.assertIn("business-balance-demand-supply-capacity", graph)
        self.assertIn("governance-govern-scorecards", graph)
        self.assertEqual(
            graph.nodes["business-design-pricing-and-packaging"]["governance_domain"],
            "business",
        )
        self.assertEqual(
            graph.nodes["governance-govern-scorecards"]["governance_domain"],
            "governance",
        )
        self.assertTrue(
            graph.has_edge(
                "business-design-pricing-and-packaging",
                "business-manage-commercial-pipeline",
            )
        )

    def test_adapter_names_normalize_to_core_runtime_names(self):
        self.assertEqual(
            normalize_skill_name("alawas-business-formulate-strategy"),
            "business-formulate-strategy",
        )
        self.assertEqual(
            normalize_skill_name("business-formulate-strategy"),
            "business-formulate-strategy",
        )

    def test_frontier_router_uses_canonical_ownership_map(self):
        self.assertEqual(
            route_business_frontier("cash runway gap and payment timing").owning_skill,
            "business-manage-liquidity-and-cash-runway",
        )
        self.assertEqual(
            route_business_frontier("discount fence and package boundary").owning_skill,
            "business-design-pricing-and-packaging",
        )
        low = route_business_frontier("strange undefined frontier")
        self.assertEqual(low.owning_skill, "business-formulate-strategy")
        self.assertEqual(low.confidence, "low")

    def test_business_path_follows_pipeline_order(self):
        path = business_path(
            "alawas-business-design-pricing-and-packaging",
            "business-manage-liquidity-and-cash-runway",
        )
        self.assertEqual(path[0], "business-design-pricing-and-packaging")
        self.assertEqual(path[-1], "business-manage-liquidity-and-cash-runway")
        self.assertIn("business-manage-commercial-pipeline", path)
        self.assertIn("business-assess-financial-decision", path)


class BusinessHandoffEnvelopeTests(unittest.TestCase):
    def test_handoff_envelope_validates_business_domain(self):
        envelope = BusinessHandoffEnvelope(
            handoff_id="HANDOFF-business-test",
            work_object_id="2026-08-22-016",
            lifecycle_state="build",
            current_frontier="pricing question resolved",
            from_skill="alawas-business-design-pricing-and-packaging",
            to_skill="alawas-business-manage-commercial-pipeline",
            governance_domain="business",
            evidence_resolved=["price package boundary named"],
            next_gap="named deal qualification",
            same_work_object=True,
            authority_boundary="read-only-propose",
            graph_path=[
                "alawas-business-design-pricing-and-packaging",
                "alawas-business-manage-commercial-pipeline",
            ],
        )

        self.assertEqual(envelope.from_skill, "business-design-pricing-and-packaging")
        self.assertEqual(envelope.to_skill, "business-manage-commercial-pipeline")
        self.assertEqual(
            envelope.graph_path,
            [
                "business-design-pricing-and-packaging",
                "business-manage-commercial-pipeline",
            ],
        )

    def test_handoff_envelope_rejects_domain_mismatch(self):
        with self.assertRaises(ValidationError):
            BusinessHandoffEnvelope(
                handoff_id="HANDOFF-business-bad",
                work_object_id="2026-08-22-016",
                lifecycle_state="build",
                current_frontier="pricing question resolved",
                from_skill="business-design-pricing-and-packaging",
                to_skill="business-manage-commercial-pipeline",
                governance_domain="engineering",
                evidence_resolved=[],
                next_gap="named deal qualification",
                same_work_object=True,
                authority_boundary="read-only-propose",
                graph_path=[
                    "business-design-pricing-and-packaging",
                    "business-manage-commercial-pipeline",
                ],
            )

    def test_propose_business_handoff_routes_next_gap(self):
        envelope = propose_business_handoff(
            handoff_id="HANDOFF-business-auto",
            work_object_id="2026-08-22-016",
            lifecycle_state="build",
            current_frontier="market boundary resolved",
            from_skill="business-manage-market-intelligence",
            evidence_resolved=["target segment named"],
            next_gap="value metric and package boundary",
            same_work_object=True,
            authority_boundary="read-only-propose",
        )

        self.assertEqual(envelope.to_skill, "business-design-pricing-and-packaging")
        self.assertEqual(envelope.governance_domain, "business")
        self.assertEqual(envelope.graph_path[-1], "business-design-pricing-and-packaging")


class BusinessRouterGraphTests(unittest.TestCase):
    def setUp(self):
        self._tmp = Path(tempfile.mkdtemp())
        self.checkpoint_db = self._tmp / "business-router.sqlite"

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _run(self, thread_id="business-router", approve=None, **overrides):
        params = {
            "work_object_id": "2026-08-22-018",
            "thread_id": thread_id,
            "lifecycle_state": "build",
            "current_frontier": "market boundary resolved",
            "from_skill": "business-manage-market-intelligence",
            "evidence_resolved": ["target segment named"],
            "next_gap": "value metric and package boundary",
            "same_work_object": True,
            "authority_boundary": "read-only-propose",
            "checkpoint_db": self.checkpoint_db,
            "approve": approve,
        }
        params.update(overrides)
        return run_business_router(**params)

    def test_router_pauses_with_checkpointed_handoff_proposal(self):
        result = self._run()

        self.assertIn("__interrupt__", result)
        self.assertEqual(
            result["handoff_envelope"]["to_skill"],
            "business-design-pricing-and-packaging",
        )
        self.assertNotIn("director_approved", result)

        state = inspect_business_router("business-router", self.checkpoint_db)
        self.assertTrue(state["awaiting_approval"])
        self.assertTrue(state["has_handoff_envelope"])
        self.assertEqual(
            state["values"]["route_result"]["owning_skill"],
            "business-design-pricing-and-packaging",
        )

    def test_router_resume_records_director_approval(self):
        self._run(thread_id="approve")
        approved = self._run(thread_id="approve", approve=True)

        self.assertNotIn("__interrupt__", approved)
        self.assertIs(approved["director_approved"], True)
        self.assertEqual(
            approved["handoff_envelope"]["to_skill"],
            "business-design-pricing-and-packaging",
        )

        self._run(thread_id="reject")
        rejected = self._run(thread_id="reject", approve=False)
        self.assertIs(rejected["director_approved"], False)

    def test_router_rejects_live_mutation_authority_boundary(self):
        with self.assertRaisesRegex(ValueError, "unsupported business router authority"):
            self._run(authority_boundary="live-system-mutation")


class BusinessRouterCliTests(unittest.TestCase):
    def setUp(self):
        self._tmp = Path(tempfile.mkdtemp())
        self.checkpoint_db = self._tmp / "business-router-cli.sqlite"

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _cli(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "runtime.business", *args],
            capture_output=True,
            text=True,
        )

    def test_cli_run_inspect_and_approve_router(self):
        run = self._cli(
            "run-router",
            "--work-object-id", "2026-08-22-019",
            "--thread-id", "cli-business",
            "--checkpoint-db", str(self.checkpoint_db),
            "--lifecycle-state", "build",
            "--current-frontier", "market boundary resolved",
            "--from-skill", "business-manage-market-intelligence",
            "--evidence-resolved", "target segment named",
            "--next-gap", "value metric and package boundary",
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn('"__interrupt__"', run.stdout)
        self.assertIn('"business-design-pricing-and-packaging"', run.stdout)

        inspect = self._cli(
            "inspect-router",
            "--thread-id", "cli-business",
            "--checkpoint-db", str(self.checkpoint_db),
        )
        self.assertEqual(inspect.returncode, 0, inspect.stderr)
        self.assertIn('"awaiting_approval": true', inspect.stdout)
        self.assertIn('"has_handoff_envelope": true', inspect.stdout)

        approve = self._cli(
            "run-router",
            "--work-object-id", "2026-08-22-019",
            "--thread-id", "cli-business",
            "--checkpoint-db", str(self.checkpoint_db),
            "--approve",
        )
        self.assertEqual(approve.returncode, 0, approve.stderr)
        self.assertIn('"director_approved": true', approve.stdout)
        self.assertNotIn('"__interrupt__"', approve.stdout)

    def test_cli_requires_next_gap_for_fresh_run(self):
        result = self._cli(
            "run-router",
            "--work-object-id", "2026-08-22-019",
            "--thread-id", "missing-gap",
            "--checkpoint-db", str(self.checkpoint_db),
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("--next-gap is required", result.stderr)


class RuntimeGraphBusinessRouterCliTests(unittest.TestCase):
    def setUp(self):
        self._tmp = Path(tempfile.mkdtemp())
        self.checkpoint_db = self._tmp / "runtime-graph-business-router.sqlite"

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _cli(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "runtime.graph", *args],
            capture_output=True,
            text=True,
        )

    def test_runtime_graph_run_inspect_and_approve_business_router(self):
        run = self._cli(
            "run-business-router",
            "--work-object-id", "2026-08-22-020",
            "--thread-id", "runtime-graph-business",
            "--checkpoint-db", str(self.checkpoint_db),
            "--lifecycle-state", "build",
            "--current-frontier", "market boundary resolved",
            "--from-skill", "business-manage-market-intelligence",
            "--evidence-resolved", "target segment named",
            "--next-gap", "value metric and package boundary",
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn('"__interrupt__"', run.stdout)
        self.assertIn('"business-design-pricing-and-packaging"', run.stdout)

        inspect = self._cli(
            "inspect-business-router",
            "--thread-id", "runtime-graph-business",
            "--checkpoint-db", str(self.checkpoint_db),
        )
        self.assertEqual(inspect.returncode, 0, inspect.stderr)
        self.assertIn('"awaiting_approval": true', inspect.stdout)
        self.assertIn('"has_handoff_envelope": true', inspect.stdout)

        approve = self._cli(
            "run-business-router",
            "--work-object-id", "2026-08-22-020",
            "--thread-id", "runtime-graph-business",
            "--checkpoint-db", str(self.checkpoint_db),
            "--approve",
        )
        self.assertEqual(approve.returncode, 0, approve.stderr)
        self.assertIn('"director_approved": true', approve.stdout)
        self.assertNotIn('"__interrupt__"', approve.stdout)

    def test_runtime_graph_requires_next_gap_for_fresh_business_router_run(self):
        result = self._cli(
            "run-business-router",
            "--work-object-id", "2026-08-22-020",
            "--thread-id", "runtime-graph-missing-gap",
            "--checkpoint-db", str(self.checkpoint_db),
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("--next-gap is required", result.stderr)


class Phase6BusinessDispatchIntegrationTests(unittest.TestCase):
    def setUp(self):
        self._tmp = Path(tempfile.mkdtemp())
        self.wo_path = self._tmp / (
            "2026-08-22-021-integrate-business-router-into-phase-6-dispatch.md"
        )
        self.wo_path.write_text(
            """---
schema_version: 1
id: 2026-08-22-021
title: Business pricing and packaging handoff
type: change
status: active
state: build
consequence: meaningful
sensitivity: ordinary
business_scope: true
created_at: 2026-08-22T00:00:00Z
updated_at: 2026-08-22T00:00:00Z
next_action: value metric and package boundary
---
## Intent

Business operating pipeline tracer fixture.

## Open questions

- value metric and package boundary
""",
            encoding="utf-8",
        )

    def tearDown(self):
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_phase6_dispatch_uses_business_router_for_business_work_object(self):
        with patch("runtime.graph._find_work_object", return_value=self.wo_path):
            result = phase6_dispatch(
                {"work_object_id": "2026-08-22-021", "thread_id": "phase6-business"}
            )

        self.assertEqual(
            "business-design-pricing-and-packaging",
            result["handoff_envelope"]["to_skill"],
        )
        self.assertEqual("business", result["handoff_envelope"]["governance_domain"])
        self.assertEqual(
            "business-design-pricing-and-packaging",
            result["business_handoff_envelope"]["to_skill"],
        )
        self.assertEqual(
            "business-design-pricing-and-packaging",
            result["business_route_result"]["owning_skill"],
        )

    def test_phase6_branches_honor_business_dispatch_route(self):
        with patch("runtime.graph._find_work_object", return_value=self.wo_path):
            dispatch = phase6_dispatch(
                {"work_object_id": "2026-08-22-021", "thread_id": "phase6-business"}
            )
            branch = phase6_branch_a(
                {
                    "work_object_id": "2026-08-22-021",
                    "thread_id": "phase6-business",
                    **dispatch,
                }
            )

        self.assertEqual(
            "business-design-pricing-and-packaging",
            branch["branch_a_receipt"]["proposed_next_skill"],
        )

    def test_phase6_checkpoint_inspection_exposes_business_handoff(self):
        checkpoint_db = self._tmp / "phase6-business.sqlite"
        with patch("runtime.graph._find_work_object", return_value=self.wo_path):
            result = run_phase6(
                "2026-08-22-021", "phase6-business-e2e", checkpoint_db
            )

        self.assertEqual(
            "business-design-pricing-and-packaging",
            result["join_proposal"],
        )
        state = inspect_phase6("phase6-business-e2e", checkpoint_db)
        self.assertTrue(state["has_business_handoff_envelope"])
        self.assertEqual(
            "business-design-pricing-and-packaging",
            state["business_route_result"]["owning_skill"],
        )

    def test_phase6_dispatch_prefers_explicit_business_scope_true(self):
        explicit_path = self._tmp / "explicit-business-scope.md"
        explicit_path.write_text(
            """---
schema_version: 1
id: 2026-08-22-022
title: Scope metadata fixture
type: change
status: active
state: build
consequence: meaningful
sensitivity: ordinary
business_scope: true
created_at: 2026-08-22T00:00:00Z
updated_at: 2026-08-22T00:00:00Z
next_action: value metric and package boundary
---
## Intent

No domain words needed here.
""",
            encoding="utf-8",
        )

        with patch("runtime.graph._find_work_object", return_value=explicit_path):
            result = phase6_dispatch(
                {"work_object_id": "2026-08-22-022", "thread_id": "explicit-true"}
            )

        self.assertEqual(
            "business-design-pricing-and-packaging",
            result["business_handoff_envelope"]["to_skill"],
        )

    def test_phase6_dispatch_prefers_explicit_business_scope_false(self):
        explicit_path = self._tmp / "explicit-not-business-scope.md"
        explicit_path.write_text(
            """---
schema_version: 1
id: 2026-08-22-022
title: Business pricing fixture explicitly disabled
type: change
status: active
state: build
consequence: meaningful
sensitivity: ordinary
business_scope: false
created_at: 2026-08-22T00:00:00Z
updated_at: 2026-08-22T00:00:00Z
next_action: business pricing package boundary
---
## Intent

This fixture contains business words but explicitly opts out.
""",
            encoding="utf-8",
        )

        with patch("runtime.graph._find_work_object", return_value=explicit_path):
            result = phase6_dispatch(
                {"work_object_id": "2026-08-22-022", "thread_id": "explicit-false"}
            )

        self.assertNotIn("business_handoff_envelope", result)
        self.assertEqual("implement-bounded-change", result["handoff_envelope"]["to_skill"])


if __name__ == "__main__":
    unittest.main()
