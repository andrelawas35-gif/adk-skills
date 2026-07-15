#!/usr/bin/env python3
"""Behavioral tests for the adapter generator.

Dependency-free — standard-library unittest only, matching the generator's
"no runtime dependencies" contract. Run with:

    python3 -m unittest discover -s tests -v
"""

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "tools" / "generate-adapters.py"
CORE_DIR = ROOT / "skills" / "core"
ADAPTERS_DIR = ROOT / "adapters"
PLATFORMS = ["codex", "claude-code", "github-copilot"]


def run_generator(*args):
    return subprocess.run(
        [sys.executable, str(GENERATOR), *args],
        capture_output=True, text=True, cwd=str(ROOT),
    )


def core_body(skill_name):
    """The Markdown body of a core skill (everything after the frontmatter)."""
    text = (CORE_DIR / skill_name / "SKILL.md").read_text()
    return text.split("---", 2)[2].lstrip("\n").rstrip("\n")


def core_skill_names():
    return sorted(p.name for p in CORE_DIR.iterdir() if p.is_dir())


class GeneratorContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Always start from a freshly generated tree.
        result = run_generator()
        assert result.returncode == 0, result.stderr

    def test_check_passes_after_generate(self):
        result = run_generator("--check")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_regeneration_is_byte_for_byte_identical(self):
        """Regenerating without source changes must not alter any artifact."""
        before = {p: p.read_bytes() for p in ADAPTERS_DIR.rglob("*")
                  if p.is_file()}
        result = run_generator()
        self.assertEqual(result.returncode, 0, result.stderr)
        after = {p: p.read_bytes() for p in ADAPTERS_DIR.rglob("*")
                 if p.is_file()}
        self.assertEqual(before.keys(), after.keys(), "file set changed")
        for path, content in before.items():
            self.assertEqual(content, after[path],
                             f"{path.relative_to(ROOT)} changed on regen")

    def test_core_body_is_preserved_verbatim(self):
        """The adapter must reproduce the core body unchanged before its
        appended Platform Adapter section — no edits to decision logic,
        authority rules, or schema semantics."""
        for platform in PLATFORMS:
            for skill in core_skill_names():
                adapter = (ADAPTERS_DIR / platform / "skills" / skill
                           / "SKILL.md").read_text()
                body_before_adapter = adapter.split(
                    "\n---\n\n## Platform Adapter", 1)[0]
                # Strip the generated frontmatter to isolate the body.
                after_fm = body_before_adapter.split("---", 2)[2].lstrip("\n")
                self.assertIn(
                    core_body(skill), after_fm,
                    f"{platform}/{skill}: core body not preserved verbatim")

    def test_adapter_only_appends_platform_section(self):
        """Beyond frontmatter, the adapter differs from core only by an
        appended section — it never inserts into or rewrites the body."""
        for platform in PLATFORMS:
            for skill in core_skill_names():
                adapter = (ADAPTERS_DIR / platform / "skills" / skill
                           / "SKILL.md").read_text()
                after_fm = adapter.split("---", 2)[2].lstrip("\n")
                self.assertTrue(
                    after_fm.startswith(core_body(skill)),
                    f"{platform}/{skill}: body is not core + suffix")
                suffix = after_fm[len(core_body(skill)):]
                self.assertIn("## Platform Adapter", suffix)

    def test_frontmatter_declares_platform(self):
        for platform in PLATFORMS:
            for skill in core_skill_names():
                adapter = (ADAPTERS_DIR / platform / "skills" / skill
                           / "SKILL.md").read_text()
                frontmatter = adapter.split("---", 2)[1]
                self.assertIn(f"platform: {platform}", frontmatter)
                self.assertIn(f"name: {skill}", frontmatter)

    def test_manifest_checksums_match_files(self):
        for platform in PLATFORMS:
            manifest = json.loads(
                (ADAPTERS_DIR / platform / "manifest.json").read_text())
            self.assertEqual(manifest["platform"], platform)
            self.assertTrue(manifest["version"])
            self.assertTrue(manifest["files"])
            for entry in manifest["files"]:
                actual = hashlib.sha256(
                    (ROOT / entry["path"]).read_bytes()).hexdigest()
                self.assertEqual(
                    entry["sha256"], actual,
                    f"{platform}: manifest checksum mismatch for {entry['path']}")

    def test_sha256sums_match_files(self):
        for platform in PLATFORMS:
            sums_file = ADAPTERS_DIR / platform / "SHA256SUMS"
            self.assertTrue(sums_file.exists(), f"{platform}: no SHA256SUMS")
            for line in sums_file.read_text().splitlines():
                sha, rel = line.split("  ", 1)
                actual = hashlib.sha256(
                    (ADAPTERS_DIR / platform / rel).read_bytes()).hexdigest()
                self.assertEqual(
                    sha, actual,
                    f"{platform}: SHA256SUMS mismatch for {rel}")

    def test_all_platforms_share_identical_behavior(self):
        """Every platform's adapter embeds the exact same core body, so the
        shared behavioral scenario runs identically across platforms — the
        only differences are metadata and the platform wiring appendix."""
        for skill in core_skill_names():
            bodies = {}
            for platform in PLATFORMS:
                adapter = (ADAPTERS_DIR / platform / "skills" / skill
                           / "SKILL.md").read_text()
                after_fm = adapter.split("---", 2)[2].lstrip("\n")
                bodies[platform] = after_fm.split(
                    "\n---\n\n## Platform Adapter", 1)[0]
            distinct = set(bodies.values())
            self.assertEqual(
                len(distinct), 1,
                f"{skill}: core behavior diverges across platforms")

    def test_platform_constraints_are_disclosed(self):
        """A manual-fallback capability must be surfaced in the adapter, not
        silently changed — the adapter discloses the constraint."""
        adapter = (ADAPTERS_DIR / "claude-code" / "skills"
                   / "conduct-work-object" / "SKILL.md").read_text()
        self.assertIn("manual-fallback", adapter)
        self.assertIn("Declared Limitations", adapter)
        self.assertIn("### Installation and precedence", adapter)
        self.assertIn("takes precedence", adapter)

    def test_drift_is_detected(self):
        """--check must fail (and then recover) when an artifact is edited."""
        target = (ADAPTERS_DIR / "claude-code" / "skills"
                  / "conduct-work-object" / "SKILL.md")
        original = target.read_bytes()
        try:
            target.write_text(target.read_text() + "\ndrifted\n")
            result = run_generator("--check")
            self.assertEqual(result.returncode, 1,
                             "drift should make --check fail")
            self.assertIn("DRIFT", result.stdout)
        finally:
            target.write_bytes(original)
        # Confirm clean state is restored.
        self.assertEqual(run_generator("--check").returncode, 0)


if __name__ == "__main__":
    unittest.main()
