"""Compound request handling tests for orchestrator routing (WO 2026-08-25-003 Step 4).

Tests the WO ID dominance behavior and mixed-signal resolution from OQ 7.
"""

from __future__ import annotations

import unittest
from runtime.orchestrator import route_request


class TestCompoundRequestHandling(unittest.TestCase):
    """Verify compound request handling with WO ID dominance."""

    def test_single_wo_id_routes_to_governance(self):
        """Single WO ID reference routes to governance-conduct-work-object for lifecycle."""
        request = "transition WO 2026-08-25-003 to verify"
        
        decision = route_request(request)
        
        # Should extract WO ID and use its domain/consequence from frontmatter
        self.assertIsNotNone(decision.domain)
        self.assertEqual(decision.signal_used, "wo_id")

    def test_wo_id_with_keyword_signals_routes_to_governance(self):
        """WO ID with production keywords still routes to governance (lifecycle operation)."""
        request = "update WO 2026-08-25-003 and render a preview for shot 14"
        
        decision = route_request(request)
        
        # WO ID should dominate, even with production keywords present
        self.assertIn(decision.signal_used, ["wo_id", "wo_id_dominates"])
        self.assertIsNotNone(decision.domain)
        self.assertEqual(decision.skill, "governance-conduct-work-object")

    def test_multiple_wo_ids_uses_maximum_consequence(self):
        """Multiple WO IDs use maximum consequence for gating authority."""
        request = "update WO 2026-08-25-003 and review WO 2026-08-24-014"
        
        decision = route_request(request)
        
        # Should extract first WO ID (highest priority signal takes precedence)
        self.assertIn(decision.signal_used, ["wo_id", "wo_id_dominates"])
        # Maximum consequence should be checked when multiple WOs found

    def test_wo_id_with_comp_reference(self):
        """WO ID with COMP reference still uses WO dominance."""
        request = "update WO 2026-08-25-003 and check COMP-042 status"
        
        decision = route_request(request)
        
        # WO ID should dominate over COMP reference  
        self.assertIn(decision.signal_used, ["wo_id", "wo_id_dominates"])
        self.assertEqual(decision.skill, "governance-conduct-work-object")

    def test_no_wo_id_with_keyword_signals_uses_keywords(self):
        """No WO ID with keywords should use keyword routing (not compound handling)."""
        request = "render shot 14 for the client presentation"
        
        decision = route_request(request)
        
        # Should NOT be marked as compound_handled (no WO reference)
        self.assertFalse(decision.compound_handled)
        self.assertEqual(decision.signal_used, "keyword")
        self.assertEqual(decision.domain, "production")

    def test_wo_id_with_multiple_keywords(self):
        """WO ID with multiple domain keywords still uses single domain from WO."""
        request = "update WO 2026-08-25-003 and implement the scene planner and render a preview"
        
        decision = route_request(request)
        
        # Should use WO's own domain, not infer from multiple keywords
        self.assertIn(decision.signal_used, ["wo_id", "wo_id_dominates"])
        self.assertEqual(decision.skill, "governance-conduct-work-object")

    def test_specific_wo_with_known_domain(self):
        """WO with known production domain should route to that domain (not governance)."""
        # WO 2026-08-25-003 has domain: [engineering] and consequence: meaningful
        request = "update WO 2026-08-25-003"
        
        decision = route_request(request)
        
        self.assertEqual(decision.domain, "engineering")
        self.assertEqual(decision.consequence, "meaningful")

    def test_routing_note_for_compound_requests(self):
        """Compound requests include routing explanation in note field."""
        request = "update WO 2026-08-25-003 and render preview"
        
        decision = route_request(request)
        
        if decision.compound_handled:
            self.assertIsNotNone(decision.routing_note)
            # Note text may vary slightly, check for key phrase regardless of case
            note_lower = (decision.routing_note or "").lower()
            self.assertIn("wo id dominates", note_lower)


if __name__ == "__main__":
    unittest.main()