import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.ws.asset_workbench import generate


ROOT = Path(__file__).resolve().parents[1]


class AssetWorkbenchTests(unittest.TestCase):
    def test_generate_real_workspace_projection(self):
        summary = generate(ROOT)
        out = ROOT / ".work-studio" / "asset-workbench.html"
        self.assertEqual(out, summary["out_path"])
        self.assertGreaterEqual(summary["assets"], 1)
        self.assertEqual(0, summary["gaps"])
        text = out.read_text(encoding="utf-8")
        self.assertIn("Design Asset Workbench", text)
        self.assertIn("asset.design.reviewbadge", text)
        self.assertIn("Read-only projection", text)
        self.assertIn("design-project-asset-workbench", text)

    def test_cli_command_generates_projection(self):
        result = subprocess.run(
            [sys.executable, "-m", "tools.ws", "asset-workbench"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("asset-workbench.html", result.stdout)
        self.assertIn("Assets:", result.stdout)

    def test_projection_reports_validation_gaps_without_mutating_asset(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            asset_dir = root / ".work-studio" / "design-assets"
            asset_dir.mkdir(parents=True)
            asset = asset_dir / "broken.asset.md"
            asset.write_text(
                "# Broken\n\n"
                "**Work Object:** `2026-08-22-017`\n"
                "**Pipeline:** `references/DESIGN-ASSET-PIPELINE.md`\n"
                "**Status:** tracer\n"
                "**Asset ID:** `asset.design.broken`\n"
                "**Asset kind:** component-family\n"
                "**Source of truth:** this asset record\n\n"
                "## Asset Summary\n\nBroken.\n"
                "## Lifecycle\n\n| Step | Owning skill | Evidence |\n"
                "|------|--------------|----------|\n"
                "| Intake | `design-manage-assets` | test |\n"
                "## Verification Notes\n\nNone.\n"
                "## Rollback\n\nDelete.\n",
                encoding="utf-8",
            )

            before = asset.read_text(encoding="utf-8")
            summary = generate(root)
            after = asset.read_text(encoding="utf-8")

        self.assertEqual(before, after)
        self.assertEqual(1, summary["assets"])
        self.assertGreater(summary["gaps"], 0)


if __name__ == "__main__":
    unittest.main()
