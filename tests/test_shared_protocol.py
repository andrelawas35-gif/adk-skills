#!/usr/bin/env python3
"""Installed-boundary regressions for the Shared Protocol."""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INSTALL = ROOT / "tools" / "install.sh"
FIXTURE = ROOT / "fixtures" / "personal-institution-work-studio-contract.md"


class SharedProtocolContract(unittest.TestCase):
    def test_installed_adapter_exposes_a_checksummed_protocol(self):
        with tempfile.TemporaryDirectory() as work:
            home = Path(work) / "home" / ".claude"
            env = {**os.environ, "CLAUDE_HOME": str(home)}
            result = subprocess.run(
                [str(INSTALL), "--platform", "claude-code", "--global"],
                cwd=ROOT, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            installed = home / "skills" / "alawas-conduct-work-object" / "references" / "SHARED-PROTOCOL.md"
            self.assertTrue(installed.is_file())

        manifest = json.loads((ROOT / "adapters" / "claude-code" / "manifest.json").read_text())
        self.assertEqual(manifest["protocol_version"], "0.1")
        self.assertTrue(any(entry["path"].endswith("references/SHARED-PROTOCOL.md") for entry in manifest["files"]))

    def test_conformance_rejects_a_missing_protocol_scenario(self):
        with tempfile.TemporaryDirectory() as work:
            malformed = Path(work) / FIXTURE.name
            text = FIXTURE.read_text().replace("## Scenario 6 — Incompatible protocol versions degrade safely", "")
            malformed.write_text(text)
            result = subprocess.run(
                ["python3", "tools/verify-conformance.py", "--matrix", str(malformed)],
                cwd=ROOT, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Incompatible protocol versions", result.stdout)


if __name__ == "__main__":
    unittest.main()
