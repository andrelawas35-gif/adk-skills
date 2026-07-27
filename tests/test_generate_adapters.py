#!/usr/bin/env python3
"""Behavioral tests for the adapter generator.

Dependency-free — standard-library unittest only, matching the generator's
"no runtime dependencies" contract. Run with:

    python3 -m unittest discover -s tests -v
"""

import hashlib
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "tools" / "generate-adapters.py"
CORE_DIR = ROOT / "skills" / "core"
ADAPTERS_DIR = ROOT / "adapters"
PLATFORMS = ["codex", "claude-code", "github-copilot"]
SKILL_NAMESPACE = "alawas"


def run_generator(*args):
    return subprocess.run(
        [sys.executable, str(GENERATOR), *args],
        capture_output=True, text=True, cwd=str(ROOT),
    )


def core_body(skill_name):
    """The Markdown body of a core skill (everything after the frontmatter)."""
    text = (CORE_DIR / skill_name / "SKILL.md").read_text()
    body = text.split("---", 2)[2].lstrip("\n").rstrip("\n")
    for name in sorted(core_skill_names(), key=len, reverse=True):
        body = body.replace(f"`{name}`", f"`{adapter_skill_name(name)}`")
    return body


def core_skill_names():
    return sorted(p.name for p in CORE_DIR.iterdir() if p.is_dir())


def adapter_skill_name(skill):
    return f"{SKILL_NAMESPACE}-{skill}"


def adapter_file(platform, skill):
    return ADAPTERS_DIR / platform / "skills" / adapter_skill_name(skill) / "SKILL.md"


def required_capabilities(skill):
    text = (CORE_DIR / skill / "SKILL.md").read_text()
    section = text.split("## Required capabilities", 1)[1].split("\n## ", 1)[0]
    declared = []
    for line in section.splitlines():
        if line.startswith("- "):
            declaration = line.split("—", 1)[0]
            for capability in re.findall(r"`([^`]+)`", declaration):
                if capability not in declared:
                    declared.append(capability)
    return declared


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
                adapter = adapter_file(platform, skill).read_text()
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
                adapter = adapter_file(platform, skill).read_text()
                after_fm = adapter.split("---", 2)[2].lstrip("\n")
                self.assertTrue(
                    after_fm.startswith(core_body(skill)),
                    f"{platform}/{skill}: body is not core + suffix")
                suffix = after_fm[len(core_body(skill)):]
                self.assertIn("## Platform Adapter", suffix)

    def test_frontmatter_declares_platform(self):
        for platform in PLATFORMS:
            for skill in core_skill_names():
                adapter = adapter_file(platform, skill).read_text()
                frontmatter = adapter.split("---", 2)[1]
                self.assertIn(f"platform: {platform}", frontmatter)
                self.assertIn(f"name: {adapter_skill_name(skill)}", frontmatter)

    def test_generated_description_is_a_single_line_quoted_scalar(self):
        """Keep the generated description in a directly parseable YAML scalar."""
        for platform in PLATFORMS:
            for skill in core_skill_names():
                adapter = adapter_file(platform, skill).read_text()
                frontmatter = adapter.split("---", 2)[1].splitlines()
                description_line = next(
                    line for line in frontmatter if line.startswith("description: "))
                encoded = description_line[len("description: "):]
                description = json.loads(encoded)
                self.assertIsInstance(description, str)
                self.assertTrue(description.strip(), f"{platform}/{skill}: empty description")
                self.assertNotIn("\n", description)

    def test_generated_descriptions_are_compact_trigger_action_boundary_metadata(self):
        boundary_terms = ("does not", "never", "stops for")
        descriptions = set()
        for platform in PLATFORMS:
            for skill in core_skill_names():
                frontmatter = adapter_file(platform, skill).read_text().split("---", 2)[1]
                encoded = next(
                    line[len("description: "):]
                    for line in frontmatter.splitlines()
                    if line.startswith("description: ")
                )
                description = json.loads(encoded)
                self.assertTrue(description.startswith("Use when "), skill)
                self.assertIn(";", description, skill)
                self.assertTrue(
                    any(term in description.lower() for term in boundary_terms), skill)
                self.assertLessEqual(len(description.split()), 40, skill)
                descriptions.add((skill, description))
        self.assertEqual(len(descriptions), len(core_skill_names()))

    def test_installed_conductor_contains_the_minimum_work_object_schema(self):
        """Conductor delegates creation to ws CLI; schema lives in WORK-OBJECT.md and schema.py.

        The conductor adapter must reference the CLI create command, and the
        schema fields must be discoverable from WORK-OBJECT.md or the CLI.
        """
        # Verify the conductor references ws create (the new write path)
        for platform in PLATFORMS:
            adapter = adapter_file(platform, "conduct-work-object").read_text()
            self.assertTrue(
                "ws create" in adapter or "tools.ws" in adapter,
                f"{platform}: conductor should reference ws CLI for creation"
            )

        # Verify WORK-OBJECT.md contains the minimum schema
        wo_md = (ROOT / "references" / "WORK-OBJECT.md").read_text()
        schema_fields = [
            "schema_version",
            "id:",
            "title:",
            "type:",
            "status:",
            "state:",
            "consequence:",
            "sensitivity:",
            "created_at:",
            "updated_at:",
            "next_action:",
        ]
        for field in schema_fields:
            self.assertIn(field, wo_md, f"WORK-OBJECT.md missing field: {field}")

    def test_high_consequence_objects_cannot_be_staged_without_confirmation(self):
        required = (
            "Do not stage, annotate, change status, append History, or make any "
            "other mutation"
        )
        for platform in PLATFORMS:
            for skill in core_skill_names():
                adapter = adapter_file(platform, skill).read_text()
                self.assertIn(
                    required, " ".join(adapter.split()),
                    f"{platform}/{skill}: weak authority gate")
        local_flow = (
            "For a low- or meaningful-consequence Work Object, `yes` or "
            "`do recommended` accepts"
        )
        for platform in PLATFORMS:
            adapter = adapter_file(platform, "pressure-test-decision").read_text()
            self.assertIn(local_flow, " ".join(adapter.split()))

    def test_gated_skills_have_inline_authority_blocks(self):
        """Every skill that describes gated actions must have an inline
        authority gate block referencing CONSEQUENCE-AUTHORITY.md (Decision 57).

        The test checks both the core source and all generated adapters.
        """
        gated_skills = {
            "conduct-work-object",
            "deploy-with-recovery",
            "implement-bounded-change",
            "verify-release-evidence",
            "review-outcome-and-adapt",
            "diagnose-production-incident",
            "maintain-working-method",
            "govern-scorecards",
        }
        authority_marker = "**Authority gate:**"
        reference_marker = "CONSEQUENCE-AUTHORITY.md"

        # Core skills must have inline authority blocks
        for skill in gated_skills:
            core_text = (CORE_DIR / skill / "SKILL.md").read_text()
            self.assertIn(
                authority_marker, core_text,
                f"core/{skill}: missing inline authority gate block"
            )
            self.assertIn(
                reference_marker, core_text,
                f"core/{skill}: authority gate does not reference CONSEQUENCE-AUTHORITY.md"
            )

        # Generated adapters must propagate authority blocks
        for platform in PLATFORMS:
            for skill in gated_skills:
                adapter = adapter_file(platform, skill).read_text()
                self.assertIn(
                    authority_marker, adapter,
                    f"{platform}/{skill}: authority gate missing in adapter"
                )
                self.assertIn(
                    reference_marker, adapter,
                    f"{platform}/{skill}: authority gate missing CONSEQUENCE-AUTHORITY.md ref"
                )

        # Non-gated skills should NOT have authority blocks (prevent scope creep)
        all_skills = set(core_skill_names())
        non_gated = all_skills - gated_skills
        for skill in non_gated:
            core_text = (CORE_DIR / skill / "SKILL.md").read_text()
            self.assertNotIn(
                authority_marker, core_text,
                f"core/{skill}: has authority gate but is not in gated-skills list"
            )

    def test_installed_skills_include_their_declared_references(self):
        """Each generated skill receives only the reference files its core body
        mentions (Decision 88). Skills that mention none get no references dir."""
        references = [
            "MISSING-ARTIFACT-GAP.md",
            "AGREEMENT-LOOP.md",
            "SKILL-AWARE-GRILLING.md",
            "CAPABILITY-DEGRADATION.md",
            "CONSEQUENCE-AUTHORITY.md",
            "EVIDENCE-MODEL.md",
        ]
        for platform in PLATFORMS:
            for skill in core_skill_names():
                core_text = (CORE_DIR / skill / "SKILL.md").read_text()
                body = core_text.split("---", 2)[2]
                mentioned = [r for r in references if r in body]
                refs_dir = (ADAPTERS_DIR / platform / "skills"
                            / adapter_skill_name(skill) / "references")
                if mentioned:
                    self.assertTrue(refs_dir.is_dir(),
                                    f"{platform}/{skill}: expected references dir")
                    for reference in mentioned:
                        path = refs_dir / reference
                        self.assertTrue(path.is_file(),
                                        f"missing installed reference: {path}")
                else:
                    self.assertFalse(refs_dir.exists(),
                                     f"{platform}/{skill}: unexpected references dir")

    def test_generated_adapters_include_local_grilling_profile_summary(self):
        for platform in PLATFORMS:
            for skill in core_skill_names():
                adapter = adapter_file(platform, skill).read_text()
                normalized = " ".join(adapter.split())
                if skill == "grilling-session":
                    self.assertIn("## Entry and delegation", adapter)
                    self.assertIn("Run ephemerally", normalized)
                else:
                    self.assertIn("## Skill Grilling Profile", adapter)
                    self.assertIn(f"`{adapter_skill_name(skill)}` profile", normalized)

    def test_every_required_core_capability_is_mapped_and_classified(self):
        """A core requirement cannot silently disappear at an adapter boundary."""
        for skill in core_skill_names():
            core_text = (CORE_DIR / skill / "SKILL.md").read_text()
            capabilities_section = core_text.split("## Required capabilities", 1)[1]
            capabilities_section = capabilities_section.split("\n## ", 1)[0]
            required = re.findall(r"^- `([^`]+)`", capabilities_section, re.MULTILINE)

            for platform in PLATFORMS:
                adapter = adapter_file(platform, skill).read_text()
                for capability in required:
                    with self.subTest(skill=skill, platform=platform, capability=capability):
                        self.assertRegex(
                            adapter,
                            rf"\| `{re.escape(capability)}` \| .+ \| (native|manual-fallback|unsupported) \|",
                        )

    def test_platform_appendix_contains_only_required_capability_rows(self):
        for platform in PLATFORMS:
            for skill in core_skill_names():
                adapter = adapter_file(platform, skill).read_text()
                appendix = adapter.split("\n---\n\n## Platform Adapter", 1)[1]
                table = appendix.split("### Required capability mappings", 1)[1]
                table = table.split("\n### ", 1)[0]
                rows = re.findall(r"^\| `([^`]+)` \|", table, re.MULTILINE)
                self.assertEqual(rows, required_capabilities(skill),
                                 f"{platform}/{skill}: irrelevant or missing mapping")

    def test_platform_appendix_excludes_cold_path_maintainer_guidance(self):
        forbidden = (
            "### Installation and precedence",
            "### Discovery",
            "### Declared Limitations",
            "### Integrity",
            "tools/install.sh",
            "python3 tools/generate-adapters.py",
        )
        for platform in PLATFORMS:
            for skill in core_skill_names():
                appendix = adapter_file(platform, skill).read_text().split(
                    "\n---\n\n## Platform Adapter", 1)[1]
                for text in forbidden:
                    self.assertNotIn(text, appendix, f"{platform}/{skill}: {text}")

    def test_degradation_details_are_emitted_only_when_required(self):
        codex_inquiry = adapter_file("codex", "investigate-live-question").read_text()
        codex_build = adapter_file("codex", "implement-bounded-change").read_text()
        self.assertIn("#### `web_search` (manual-fallback)", codex_inquiry)
        self.assertNotIn("`browser_automation`", codex_inquiry)
        self.assertNotIn("### Capability Degradation", codex_build)

        # deployment: manual-fallback on all platforms — degradation present in deploy-with-recovery
        for platform in PLATFORMS:
            with self.subTest(platform=platform):
                adapter = adapter_file(platform, "deploy-with-recovery").read_text()
                self.assertIn("#### `deployment` (manual-fallback)", adapter)
                self.assertIn("#### `secret_access` (manual-fallback)", adapter)
                self.assertIn("#### `file_uploads` (manual-fallback)", adapter)

        # artifact_rendering: native on Claude Code — no degradation section there
        cc_gov = adapter_file("claude-code", "govern-scorecards").read_text()
        self.assertNotIn("#### `artifact_rendering`", cc_gov)
        # artifact_rendering: manual-fallback on Codex and Copilot — degradation present
        codex_gov = adapter_file("codex", "govern-scorecards").read_text()
        self.assertIn("#### `artifact_rendering` (manual-fallback)", codex_gov)
        copilot_gov = adapter_file("github-copilot", "govern-scorecards").read_text()
        self.assertIn("#### `artifact_rendering` (manual-fallback)", copilot_gov)

    def test_new_capabilities_classified_across_platforms(self):
        """All six new capabilities from Decision 75 appear in every overlay
        with valid classifications."""
        new_caps = {"deployment", "secret_access", "background_processes",
                     "persistent_session_state", "file_uploads", "artifact_rendering"}
        valid_classifications = {"native", "manual-fallback", "unsupported"}

        for platform in PLATFORMS:
            overlay_text = (ADAPTERS_DIR / platform / "overlay.yaml").read_text()
            # Extract capabilities section: from "capabilities:" to next top-level key
            caps_section = overlay_text.split("capabilities:", 1)[1]
            caps_section = caps_section.split("\n#", 1)[0]
            for cap in new_caps:
                with self.subTest(platform=platform, capability=cap):
                    self.assertIn(cap, caps_section,
                                  f"{platform}: {cap} missing from capabilities")
                    # Extract classification value
                    m = re.search(rf"  {re.escape(cap)}: (\S+)", caps_section)
                    self.assertIsNotNone(m,
                        f"{platform}: {cap} has no classification")
                    self.assertIn(m.group(1), valid_classifications,
                        f"{platform}: {cap} has invalid classification: {m.group(1)}")

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

    def test_all_platforms_share_identical_core_text(self):
        """The core body text is byte-identical across platforms — this
        guarantees no platform-specific rewriting but does not assert
        behavioral equivalence under different platform runtimes."""
        for skill in core_skill_names():
            bodies = {}
            for platform in PLATFORMS:
                adapter = adapter_file(platform, skill).read_text()
                after_fm = adapter.split("---", 2)[2].lstrip("\n")
                bodies[platform] = after_fm.split(
                    "\n---\n\n## Platform Adapter", 1)[0]
            distinct = set(bodies.values())
            self.assertEqual(
                len(distinct), 1,
                f"{skill}: core behavior diverges across platforms")

    def test_platform_constraints_are_disclosed(self):
        """A required manual-fallback capability remains explicit."""
        adapter = adapter_file("claude-code", "investigate-live-question").read_text()
        self.assertIn("manual-fallback", adapter)
        self.assertIn("#### `web_search` (manual-fallback)", adapter)

    def test_codex_runtime_defers_to_the_project_pin(self):
        """Codex may discover duplicate same-name skills, so either copy must
        explicitly defer to the project-pinned artifact recorded by installer."""
        for skill in core_skill_names():
            adapter = adapter_file("codex", skill).read_text()
            self.assertIn("### Runtime pin resolution", adapter)
            self.assertIn(".work-studio/adapter.codex.lock", adapter)
            self.assertIn("load and follow the pinned copy", adapter)

    def test_pin_resolution_is_codex_only(self):
        """Pin-resolution paragraph is Codex-only. Decision 85: this is an
        unverified assumption about other platforms' native precedence."""
        for skill in core_skill_names():
            for platform in ["claude-code", "github-copilot"]:
                adapter = adapter_file(platform, skill).read_text()
                self.assertNotIn("### Runtime pin resolution", adapter)

    def test_drift_is_detected(self):
        """--check must fail (and then recover) when an artifact is edited."""
        target = adapter_file("claude-code", "conduct-work-object")
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
