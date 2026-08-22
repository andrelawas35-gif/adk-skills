import unittest
from pathlib import Path

from tools.ws.design_assets import asset_record_paths, parse_asset_fields, validate_asset_record
from tools.ws.design_asset_routing import route_asset_record


ROOT = Path(__file__).resolve().parents[1]

REVIEWBADGE = ROOT / ".work-studio" / "design-assets" / "reviewbadge.asset.md"
COMPOSITION = (
    ROOT
    / ".work-studio"
    / "deliverables"
    / "2026-08-22-017-reviewbadge-editorial-contrast-composition.md"
)
STEWARDSHIP = (
    ROOT
    / ".work-studio"
    / "deliverables"
    / "2026-08-22-017-reviewbadge-experience-stewardship.md"
)


class CreativeUseCompositionTests(unittest.TestCase):
    def test_reviewbadge_asset_is_accepted_active(self):
        fields = parse_asset_fields(REVIEWBADGE.read_text(encoding="utf-8"))
        self.assertEqual("active", fields.get("Status", ""))
        self.assertEqual("component-family", fields.get("Asset kind", ""))
        self.assertEqual([], validate_asset_record(REVIEWBADGE))

    def test_reviewbadge_still_routes_to_single_owner_after_acceptance(self):
        for frontier in ("theme", "component-family"):
            route = route_asset_record(REVIEWBADGE, frontier=frontier)
            self.assertEqual("design-compose-design-system", route.owner)
            self.assertEqual((), route.gaps)
        steward = route_asset_record(REVIEWBADGE, frontier="ux-pattern")
        self.assertEqual("design-steward-experience-patterns", steward.owner)
        self.assertEqual((), steward.gaps)

    def test_editorial_contrast_composition_record_is_well_formed(self):
        text = COMPOSITION.read_text(encoding="utf-8")
        normalized = " ".join(text.lower().split())
        self.assertIn("design-compose-design-system", text)
        self.assertIn("editorial-contrast", text)
        self.assertIn("confirmed creative direction", normalized)
        self.assertIn("inherited", normalized)
        self.assertIn("overridden", normalized)
        self.assertIn("prohibited", normalized)
        self.assertIn("does not authorize implementation", normalized)

    def test_experience_stewardship_record_declares_blocked_noncolor_signal(self):
        text = STEWARDSHIP.read_text(encoding="utf-8")
        normalized = " ".join(text.lower().split())
        self.assertIn("design-steward-experience-patterns", text)
        self.assertIn("create-review-approve", text)
        self.assertIn("blocked", normalized)
        self.assertIn("non-color contrast", normalized)
        self.assertIn("claim accessibility compliance", normalized)

    def test_all_real_assets_still_validate_after_acceptance(self):
        for path in asset_record_paths(ROOT):
            self.assertEqual([], validate_asset_record(path), msg=str(path))


if __name__ == "__main__":
    unittest.main()
