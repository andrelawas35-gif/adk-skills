"""Tests for ws authority check — tracer-bullet verification.

Three test cases:
  1. GRANTED — action within scope, no expiry
  2. DENIED — action outside scope
  3. AMBIGUOUS — unparseable scope (wildcard token)
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Ensure tools.ws is importable
TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
REPO_ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(REPO_ROOT))


# ── Helper: build a synthetic Work Object with an Authority History entry ─────

AUTHORITY_WO_TEMPLATE = """---
schema_version: 1
id: 2026-07-28-TEST
title: Authority Check Test Fixture
type: project
status: active
state: notice
consequence: low
sensitivity: ordinary
created_at: 2026-07-28T00:00:00Z
updated_at: 2026-07-28T00:00:00Z
next_action: Test fixture for ws authority check.
---
## Intent

Test fixture for ws authority check tracer bullet.

## History
### 2026-07-28T00:00:00Z — Authority: deploy grant

- **Scope:** {scope}
- **Evidence reviewed:** tracer test
- **Constraints:** none
- **Authority mode:** independent-authorization
- **Granted by:** test
{extra_fields}
"""


def _build_wo(scope: str = "deploy", expiry: str = "") -> str:
    extra = f"- **Expiry:** {expiry}\n" if expiry else ""
    return AUTHORITY_WO_TEMPLATE.format(scope=scope, extra_fields=extra)


class TestAuthorityCheck(unittest.TestCase):
    """Tests for ws authority check command."""

    def _run_check(self, wo_path: Path, action: str) -> str:
        """Run ws authority check and return stdout."""
        import subprocess

        env = os.environ.copy()
        env["PYTHONPATH"] = str(REPO_ROOT) + (
            f":{env.get('PYTHONPATH', '')}" if env.get("PYTHONPATH") else ""
        )

        result = subprocess.run(
            [sys.executable, "-m", "tools.ws", "authority", "check",
             str(wo_path), "--action", action],
            capture_output=True,
            text=True,
            cwd=str(wo_path.parent),
            env=env,
        )
        if result.returncode != 0:
            raise AssertionError(
                f"Command failed (exit {result.returncode}): "
                f"{result.stderr.strip()}"
            )
        return result.stdout.strip()

    def _build_workspace(self, tmp: Path, scope: str = "deploy") -> Path:
        """Build a workspace root with config.md and a synthetic WO by ID.

        Returns the path to the Work Object file under
        .work-studio/objects/2026/07/.
        """
        ws_root = tmp / "ws"
        config_dir = ws_root / ".work-studio"
        config_dir.mkdir(parents=True)
        (config_dir / "config.md").write_text("# config\n")
        obj_dir = ws_root / ".work-studio" / "objects" / "2026" / "07"
        obj_dir.mkdir(parents=True)
        wo_path = obj_dir / "2026-07-28-TEST-authority-fixture.md"
        wo_path.write_text(_build_wo(scope=scope))
        return wo_path

    def _run_check_by_id(self, ws_root: Path, obj_id: str, action: str) -> str:
        """Run ws authority check by ID against a workspace root."""
        import subprocess

        env = os.environ.copy()
        env["PYTHONPATH"] = str(REPO_ROOT) + (
            f":{env.get('PYTHONPATH', '')}" if env.get("PYTHONPATH") else ""
        )

        result = subprocess.run(
            [sys.executable, "-m", "tools.ws", "authority", "check",
             obj_id, "--action", action],
            capture_output=True,
            text=True,
            cwd=str(ws_root),
            env=env,
        )
        if result.returncode != 0:
            raise AssertionError(
                f"Command failed (exit {result.returncode}): "
                f"{result.stderr.strip()}"
            )
        return result.stdout.strip()

    def test_granted_action_in_scope(self):
        """GRANTED when action is within scope and no expiry."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            wo_path = tmp_path / "test-wo.md"
            wo_path.write_text(_build_wo(scope="deploy"))

            output = self._run_check(wo_path, "deploy")
            self.assertIn("GRANTED", output)
            self.assertNotIn("DENIED", output)
            self.assertNotIn("AMBIGUOUS", output)

    def test_denied_action_outside_scope(self):
        """DENIED when action is not within scope."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            wo_path = tmp_path / "test-wo.md"
            wo_path.write_text(_build_wo(scope="deploy"))

            output = self._run_check(wo_path, "delete")
            self.assertIn("DENIED", output)
            self.assertNotIn("GRANTED", output)

    def test_ambiguous_unparseable_scope(self):
        """AMBIGUOUS when scope contains wildcard/unparseable token."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            wo_path = tmp_path / "test-wo.md"
            wo_path.write_text(_build_wo(scope="deploy *"))

            output = self._run_check(wo_path, "deploy")
            self.assertIn("AMBIGUOUS", output)
            self.assertNotIn("GRANTED", output)

    def test_denied_expired_grant(self):
        """DENIED when grant has expired."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            wo_path = tmp_path / "test-wo.md"
            wo_path.write_text(_build_wo(scope="deploy", expiry="2000-01-01"))

            output = self._run_check(wo_path, "deploy")
            self.assertIn("DENIED", output)
            self.assertIn("expired", output.lower())

    def test_granted_multiple_actions_in_scope(self):
        """GRANTED when action is one of several in scope."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            wo_path = tmp_path / "test-wo.md"
            wo_path.write_text(_build_wo(scope="deploy rollback restart"))

            output = self._run_check(wo_path, "rollback")
            self.assertIn("GRANTED", output)

    def test_ambiguous_no_authority_entries(self):
        """AMBIGUOUS when no Authority History entries exist."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            wo_path = tmp_path / "test-wo.md"
            # WO without History section
            wo_path.write_text("""---
schema_version: 1
id: 2026-07-28-TEST-EMPTY
title: Empty Test
type: project
status: active
state: notice
consequence: low
sensitivity: ordinary
created_at: 2026-07-28T00:00:00Z
updated_at: 2026-07-28T00:00:00Z
next_action: None.
---
## Intent

No History section.
""")

            output = self._run_check(wo_path, "deploy")
            self.assertIn("AMBIGUOUS", output)
            self.assertIn("No Authority History", output)

    def test_id_resolution_grants_in_scope(self):
        """ID form resolves the Work Object and returns GRANTED."""
        with tempfile.TemporaryDirectory() as tmp:
            wo_path = self._build_workspace(Path(tmp), scope="deploy")
            ws_root = wo_path.parent.parent.parent.parent.parent

            output = self._run_check_by_id(ws_root, "2026-07-28-TEST", "deploy")
            self.assertIn("GRANTED", output)
            self.assertNotIn("DENIED", output)
            self.assertNotIn("AMBIGUOUS", output)

    def test_id_resolution_unknown_id_returns_error(self):
        """Unknown ID returns an error rather than guessing a grant."""
        with tempfile.TemporaryDirectory() as tmp:
            wo_path = self._build_workspace(Path(tmp), scope="deploy")
            ws_root = wo_path.parent.parent.parent.parent.parent

            import subprocess

            env = os.environ.copy()
            env["PYTHONPATH"] = str(REPO_ROOT) + (
                f":{env.get('PYTHONPATH', '')}" if env.get("PYTHONPATH") else ""
            )
            result = subprocess.run(
                [sys.executable, "-m", "tools.ws", "authority", "check",
                 "2026-07-28-DOES-NOT-EXIST", "--action", "deploy"],
                capture_output=True,
                text=True,
                cwd=str(ws_root),
                env=env,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not found", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
