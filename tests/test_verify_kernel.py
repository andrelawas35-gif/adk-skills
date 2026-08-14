#!/usr/bin/env python3
"""Regression tests proving verify-kernel.py catches a missing path and an
undeclared skill (WO 2026-08-14-004).

The verifier already has both checks (tools/verify-kernel.py:228-251 forward
MISSING check, :253-265 reverse UNDECLARED check), but no committed test
exercises them. These tests prove "it catches" the two failure modes and that
a well-formed manifest+tree passes cleanly (guards against a vacuously-failing
verifier).

Invocation (Decision 1, Branch A): the verifier resolves paths against the
module-global ROOT and has no CLI flag to point at a fixture, so the tests
load the module via importlib (hyphenated filename) and mock.patch ROOT to a
temp fixture tree, then call check_paths(manifest_dict) directly. The CLI
wiring and YAML-parse path are out of scope.

Dependency-free — standard-library unittest + mock only, matching the repo
convention. Run with:

    python3 -m unittest discover -s tests -v
"""

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
VERIFIER_PATH = ROOT / "tools" / "verify-kernel.py"


def load_verifier():
    """Load tools/verify-kernel.py via importlib (hyphenated filename)."""
    spec = importlib.util.spec_from_file_location("verify_kernel", VERIFIER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_manifest(entries):
    """Build a minimal manifest dict in the shape check_paths reads."""
    return {"kernel": {"entries": entries}}


class VerifyKernelChecksTest(unittest.TestCase):
    def setUp(self):
        self.vk = load_verifier()

    def test_missing_declared_path_flagged(self):
        """A declared-but-missing path produces a MISSING finding."""
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            manifest = make_manifest([
                {"path": "does/not/exist", "purpose": "missing on purpose"},
            ])
            with mock.patch.object(self.vk, "ROOT", tmp):
                passed, errors = self.vk.check_paths(manifest)

        self.assertFalse(passed)
        self.assertTrue(
            any("MISSING: does/not/exist" in err for err in errors),
            f"expected MISSING finding, got errors={errors!r}",
        )

    def test_missing_skill_subpath_flagged(self):
        """A declared skill with no SKILL.md on disk produces a MISSING finding."""
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            (tmp / "skills" / "core" / "known-skill").mkdir(parents=True)
            # deliberately no SKILL.md inside known-skill
            manifest = make_manifest([
                {"path": "skills/core/", "skills": ["known-skill"]},
            ])
            with mock.patch.object(self.vk, "ROOT", tmp):
                passed, errors = self.vk.check_paths(manifest)

        self.assertFalse(passed)
        self.assertTrue(
            any("MISSING: skills/core/known-skill/SKILL.md" in err for err in errors),
            f"expected MISSING SKILL.md finding, got errors={errors!r}",
        )

    def test_undeclared_skill_flagged(self):
        """An on-disk skill absent from the manifest produces UNDECLARED."""
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            skills_dir = tmp / "skills" / "core"
            (skills_dir / "ghost-skill").mkdir(parents=True)
            (skills_dir / "ghost-skill" / "SKILL.md").write_text("# Ghost\n")
            manifest = make_manifest([
                {"path": "skills/core/", "skills": []},
            ])
            with mock.patch.object(self.vk, "ROOT", tmp):
                passed, errors = self.vk.check_paths(manifest)

        self.assertFalse(passed)
        self.assertTrue(
            any("UNDECLARED: skills/core/ghost-skill/SKILL.md" in err for err in errors),
            f"expected UNDECLARED finding, got errors={errors!r}",
        )

    def test_well_formed_manifest_passes_clean(self):
        """A valid manifest+tree produces no findings (guards vacuous failure)."""
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            skills_dir = tmp / "skills" / "core"
            (skills_dir / "known-skill").mkdir(parents=True)
            (skills_dir / "known-skill" / "SKILL.md").write_text("# Known\n")
            manifest = make_manifest([
                {"path": "skills/core/", "skills": ["known-skill"]},
            ])
            with mock.patch.object(self.vk, "ROOT", tmp):
                passed, errors = self.vk.check_paths(manifest)

        self.assertTrue(passed)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
