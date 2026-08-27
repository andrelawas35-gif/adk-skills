#!/usr/bin/env python3
"""Orchestrator deterministic routing tracer tests (WO 2026-08-25-003 Decision 5).

Proves the 6 test cases accepted in the tracer design: five signal types
(Work Object ID, keyword x3, COMP reference) route deterministically, and a
request with no recognizable signal correctly flags needs_llm_fallback
rather than guessing.

Run under the uv-managed Python 3.11 environment:

    uv run python -m unittest discover -s runtime/tests -v
"""

import unittest

from runtime.orchestrator import route_request


class OrchestratorRoutingTests(unittest.TestCase):

    def test_wo_id_signal_reads_domain_and_consequence_from_frontmatter(self):
        decision = route_request("transition WO 2026-08-24-014 to verify")
        self.assertEqual(decision.signal_used, "wo_id")
        self.assertEqual(decision.domain, "production")
        self.assertEqual(decision.consequence, "meaningful")
        self.assertEqual(decision.confidence, "high")
        self.assertFalse(decision.needs_llm_fallback)

    def test_render_keyword_routes_to_production_blender(self):
        decision = route_request("render a preview for shot 14")
        self.assertEqual(decision.signal_used, "keyword")
        self.assertEqual(decision.domain, "production")
        self.assertEqual(decision.skill, "production-operate-blender")
        self.assertFalse(decision.needs_llm_fallback)

    def test_implement_keyword_routes_to_engineering(self):
        decision = route_request("implement the scene planner tracer")
        self.assertEqual(decision.signal_used, "keyword")
        self.assertEqual(decision.domain, "engineering")
        self.assertEqual(decision.skill, "engineering-implement-bounded-change")
        self.assertFalse(decision.needs_llm_fallback)

    def test_comp_reference_maps_to_production_with_no_specific_skill(self):
        decision = route_request("what's the status of COMP-042?")
        self.assertEqual(decision.signal_used, "comp_ref")
        self.assertEqual(decision.domain, "production")
        self.assertIsNone(decision.skill)
        self.assertFalse(decision.needs_llm_fallback)

    def test_pricing_keyword_routes_to_business(self):
        decision = route_request("help me with pricing strategy")
        self.assertEqual(decision.signal_used, "keyword")
        self.assertEqual(decision.domain, "business")
        self.assertEqual(decision.skill, "business-design-pricing-and-packaging")
        self.assertFalse(decision.needs_llm_fallback)

    def test_no_recognizable_signal_flags_llm_fallback(self):
        decision = route_request("make the lighting more dramatic")
        self.assertEqual(decision.signal_used, "none")
        self.assertIsNone(decision.domain)
        self.assertIsNone(decision.skill)
        self.assertTrue(decision.needs_llm_fallback)


if __name__ == "__main__":
    unittest.main()
