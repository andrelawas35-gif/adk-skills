import tempfile
import unittest
from pathlib import Path

from tools.ws.design_assets import (
    VALID_ASSET_KINDS,
    VALID_ASSET_STATUSES,
    validate_asset_record,
    validate_asset_registry,
)


ROOT = Path(__file__).resolve().parents[1]


class DesignAssetRegistryTests(unittest.TestCase):
    def test_registry_taxonomy_is_explicit(self):
        self.assertEqual(
            {"tracer", "draft", "active", "deprecated", "retired"},
            VALID_ASSET_STATUSES,
        )
        self.assertEqual(
            {
                "foundation",
                "token-set",
                "theme",
                "component-family",
                "ux-pattern",
                "flow",
                "projection",
                "motion",
            },
            VALID_ASSET_KINDS,
        )

    def test_reviewbadge_asset_record_passes(self):
        path = ROOT / ".work-studio" / "design-assets" / "reviewbadge.asset.md"
        self.assertEqual([], validate_asset_record(path))

    def test_incomplete_asset_fails_with_useful_messages(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.asset.md"
            path.write_text(
                "# Broken\n\n"
                "**Status:** invented\n"
                "**Asset ID:** `asset.bad`\n\n"
                "## Asset Summary\n\nNo lifecycle.\n",
                encoding="utf-8",
            )

            errors = validate_asset_record(path)

        joined = "\n".join(errors)
        self.assertIn("missing required field 'Work Object'", joined)
        self.assertIn("missing required section '## Lifecycle'", joined)
        self.assertIn("Asset ID must be backtick-wrapped", joined)
        self.assertIn("Status 'invented'", joined)

    def test_registry_validates_workspace_records(self):
        errors = validate_asset_registry(ROOT)
        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
