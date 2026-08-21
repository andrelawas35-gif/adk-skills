#!/usr/bin/env python3
"""Verify Slice 1 conformance — behavioral matrix and adapter structure.

Dependency-free — uses only Python 3 standard library.

Usage:
    python3 tools/verify-conformance.py --matrix <fixture_files...>
        Verify the behavioral matrix is complete: every fixture is referenced
        and every scenario has platform outcomes.

    python3 tools/verify-conformance.py --structure
        Verify generated adapters contain all required structural elements
        (sections, classifications, degradation rules).

    python3 tools/verify-conformance.py --all
        Run both checks.
"""

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE_DIR = ROOT / "skills" / "core"
ADAPTERS_DIR = ROOT / "adapters"
PLATFORMS = ["codex", "claude-code", "github-copilot"]
SKILLS = sorted(path.name for path in CORE_DIR.iterdir() if path.is_dir())
SKILL_NAMESPACE = "alawas"


def _load_generate_adapters_module():
    """Load generate-adapters.py helpers without a package import.

    Adapter generation is the source of truth for generated SKILL.md bodies and
    reference payloads. The structure verifier keeps its independent structural
    checks, but delegates expected generated text/reference identity to the
    generator so the two tools cannot drift in parallel.
    """
    spec = importlib.util.spec_from_file_location(
        "generate_adapters", ROOT / "tools" / "generate-adapters.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GENERATE_ADAPTERS = _load_generate_adapters_module()


def adapter_skill_name(skill):
    return f"{SKILL_NAMESPACE}-{skill}"


def _load_overlay(platform):
    overlay_path = ADAPTERS_DIR / platform / "overlay.yaml"
    return GENERATE_ADAPTERS.parse_yaml(overlay_path.read_text(encoding="utf-8"))


def _expected_adapter_output(skill, overlay):
    return GENERATE_ADAPTERS.build_skill_output(CORE_DIR / skill, overlay)


def _expected_reference_paths(skill, adapter_skill_dir):
    entries = GENERATE_ADAPTERS.build_reference_entries(
        adapter_skill_name(skill),
        adapter_skill_dir,
        core_skill_dir=CORE_DIR / skill,
    )
    return {
        (ROOT / entry["path"]).relative_to(adapter_skill_dir).as_posix()
        for entry in entries
        if "/references/" in entry["path"]
    }


def _shipped_reference_paths(adapter_skill_dir):
    refs_dir = adapter_skill_dir / "references"
    if not refs_dir.is_dir():
        return set()
    return {
        path.relative_to(adapter_skill_dir).as_posix()
        for path in refs_dir.rglob("*")
        if path.is_file()
    }


# ── Required structural elements ─────────────────────────────────────────────

REQUIRED_SECTIONS = [
    "## Governing principle",
    "## Required capabilities",
    "## Platform Adapter",
]

REQUIRED_ADAPTER_SUBSECTIONS = [
    "### Required capability mappings",
]

REQUIRED_CAPABILITY_CLASSIFICATIONS = {"native", "manual-fallback", "unsupported"}

FORBIDDEN_COLD_PATH_SECTIONS = [
    "### Installation and precedence",
    "### Discovery",
    "### Declared Limitations",
    "### Integrity",
]


def required_capabilities(skill):
    content = (CORE_DIR / skill / "SKILL.md").read_text(encoding="utf-8")
    section = content.split("## Required capabilities", 1)[1].split("\n## ", 1)[0]
    declared = []
    for line in section.splitlines():
        if not line.startswith("- "):
            continue
        declaration = line.split("—", 1)[0]
        for capability in re.findall(r"`([^`]+)`", declaration):
            if capability not in declared:
                declared.append(capability)
    return declared


# ── Matrix verification ──────────────────────────────────────────────────────

def verify_matrix(fixture_files):
    """Verify the behavioral matrix references all fixtures and is complete."""
    errors = []

    # Check that all known fixtures are referenced
    known_fixtures = {
        "fixtures/slice-1-initialize-and-resume.md",
        "fixtures/slice-1-pressure-test-and-record.md",
        "fixtures/slice-1-capability-degradation.md",
        "fixtures/slice-1-behavioral-matrix.md",
        "fixtures/slice-2-turn-signal-into-work.md",
        "fixtures/slice-2-design-tracer-bullet.md",
        "fixtures/slice-2-implement-bounded-change.md",
        "fixtures/slice-2-verify-release-evidence.md",
        "fixtures/slice-3-investigate-live-question.md",
        "fixtures/slice-3-deploy-with-recovery.md",
        "fixtures/slice-3-diagnose-production-incident.md",
        "fixtures/personal-institution-work-studio-contract.md",
    }

    for f in fixture_files:
        path = Path(f)
        if not path.exists():
            errors.append(f"Fixture file not found: {f}")
            continue
        content = path.read_text(encoding="utf-8")

        # Verify required patterns per fixture type
        name = path.name
        if "initialize-and-resume" in name:
            _check_patterns(errors, name, content, [
                "Scenario 1", "Scenario 2", "Scenario 3",
                "Workspace Discovery", "Create a Work Object", "Resume by ID",
            ])
        elif "pressure-test-and-record" in name:
            _check_patterns(errors, name, content, [
                "Scenario 1", "Scenario 2", "Scenario 3",
                "Provenance Lanes", "one question", "do recommended",
                "concurrency conflict", "unauthorized",
            ])
        elif "capability-degradation" in name:
            _check_patterns(errors, name, content, [
                "Scenario 1", "Scenario 2", "Scenario 3",
                "native", "manual-fallback", "unsupported",
                "no false verification",
            ])
        elif "behavioral-matrix" in name:
            _check_patterns(errors, name, content, [
                "Discovery and Workspace",
                "Work Object Creation",
                "Work Object Resumption",
                "Pressure-Testing and Decision",
                "Decision Persistence",
                "Concurrency and Authority",
                "Authority Gates",
                "Capability Degradation",
                "Generated-Artifact Integrity",
            ])
            # Verify each platform column exists (check for platform labels)
            platform_labels = {
                "codex": "Codex",
                "claude-code": "Claude Code",
                "github-copilot": "GitHub Copilot",
            }
            for platform, label in platform_labels.items():
                count = content.count(label)
                if count < 5:
                    errors.append(
                        f"Behavioral matrix may be missing {platform} column "
                        f"(found {count} occurrences of '{label}')")
        elif "turn-signal-into-work" in name:
            _check_patterns(errors, name, content, [
                "Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4",
                "user's language", "explicit activation", "user-approved",
                "manual-fallback", "unsupported",
            ])
        elif "design-tracer-bullet" in name:
            _check_patterns(errors, name, content, [
                "Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4",
                "recommendation", "one question", "accepted design",
                "riskiest assumption", "rollback", "observability",
                "Adjacent Possibility Pass", "option space", "does not implement",
            ])
        elif "implement-bounded-change" in name:
            _check_patterns(errors, name, content, [
                "Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4",
                "repository inspection", "unrelated working-tree changes",
                "continuous verification", "deviation", "manual-fallback",
                "unsupported", "does not deploy",
            ])
        elif "verify-release-evidence" in name:
            _check_patterns(errors, name, content, [
                "Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4",
                "successful verification", "missing evidence", "degraded dependency",
                "retry", "duplicate", "privacy", "security", "does not deploy or release",
            ])
        elif "investigate-live-question" in name:
            _check_patterns(errors, name, content, [
                "Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4", "Scenario 5",
                "primary-source", "reality contact", "contradiction", "unresolved",
                "user-approved summary", "personal archive",
            ])
        elif "deploy-with-recovery" in name:
            _check_patterns(errors, name, content, [
                "Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4",
                "successful incremental deployment", "missing readiness",
                "failed verification", "rollback", "sanitized evidence",
                "manual-fallback", "unsupported", "observe", "does not claim closure",
            ])
        elif "diagnose-production-incident" in name:
            _check_patterns(errors, name, content, [
                "Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4", "Scenario 5",
                "sanitized evidence", "containment", "restoration", "ranked hypothesis",
                "one at a time", "affected path", "external dependency", "waiting",
                "Change Work Object", "linked follow-up",
            ])

    # Verify behavioral matrix exists
    matrix_path = ROOT / "fixtures" / "slice-1-behavioral-matrix.md"
    if not matrix_path.exists():
        errors.append("Behavioral matrix missing: fixtures/slice-1-behavioral-matrix.md")

    return errors


def _check_patterns(errors, filename, content, patterns):
    for pattern in patterns:
        if pattern.lower() not in content.lower():
            errors.append(f"{filename}: missing expected pattern '{pattern}'")


# ── Structure verification ───────────────────────────────────────────────────

def verify_structure():
    """Verify all generated adapters contain required structural elements."""
    errors = []

    for platform in PLATFORMS:
        overlay_path = ADAPTERS_DIR / platform / "overlay.yaml"
        if not overlay_path.exists():
            errors.append(f"MISSING: overlay for {platform}")
            continue
        overlay = _load_overlay(platform)

        for skill in SKILLS:
            adapter_skill_dir = ADAPTERS_DIR / platform / "skills" / adapter_skill_name(skill)
            adapter_path = adapter_skill_dir / "SKILL.md"
            if not adapter_path.exists():
                errors.append(f"MISSING: {adapter_path.relative_to(ROOT)}")
                continue

            content = adapter_path.read_text(encoding="utf-8")

            # Check required sections
            for section in REQUIRED_SECTIONS:
                if section not in content:
                    errors.append(
                        f"{platform}/{skill}: missing section '{section}'")

            # Check adapter subsections
            for subsection in REQUIRED_ADAPTER_SUBSECTIONS:
                if subsection not in content:
                    errors.append(
                        f"{platform}/{skill}: missing adapter subsection '{subsection}'")

            if "\n---\n\n## Platform Adapter" not in content:
                errors.append(
                    f"{platform}/{skill}: missing Platform Adapter separator")
                appendix = ""
            else:
                appendix = content.split("\n---\n\n## Platform Adapter", 1)[1]
            for subsection in FORBIDDEN_COLD_PATH_SECTIONS:
                if subsection in appendix:
                    errors.append(
                        f"{platform}/{skill}: cold-path subsection retained '{subsection}'")

            if platform == "codex":
                if "### Runtime pin resolution" not in appendix:
                    errors.append(f"{platform}/{skill}: missing runtime pin resolution")
            elif "### Runtime pin resolution" in appendix:
                errors.append(f"{platform}/{skill}: irrelevant runtime pin resolution")

            # Check frontmatter has platform
            frontmatter = content.split("---", 2)[1]
            if f"platform: {platform}" not in frontmatter:
                errors.append(
                    f"{platform}/{skill}: frontmatter missing platform declaration")

            # Check exact required capability mappings and classifications.
            if "### Required capability mappings" not in appendix:
                errors.append(
                    f"{platform}/{skill}: missing adapter subsection '### Required capability mappings'")
                rows = []
            elif "| Abstract capability |" not in appendix:
                errors.append(
                    f"{platform}/{skill}: missing capability mappings table")
                rows = []
            else:
                table = appendix.split("### Required capability mappings", 1)[1]
                table = table.split("\n### ", 1)[0]
                rows = re.findall(
                    r"^\| `([^`]+)` \| `([^`]*)` \| (native|manual-fallback|unsupported) \|$",
                    table,
                    re.MULTILINE,
                )
            row_caps = [capability for capability, _, _ in rows]
            if row_caps != required_capabilities(skill):
                errors.append(
                    f"{platform}/{skill}: capability rows do not match declarations")
            classifications = {classification for _, _, classification in rows}
            if not classifications.issubset(REQUIRED_CAPABILITY_CLASSIFICATIONS):
                errors.append(f"{platform}/{skill}: invalid capability classification")

            non_native = [
                (capability, classification)
                for capability, _, classification in rows
                if classification != "native"
            ]
            if non_native and "### Capability Degradation" not in appendix:
                errors.append(f"{platform}/{skill}: missing relevant degradation section")
            if not non_native and "### Capability Degradation" in appendix:
                errors.append(f"{platform}/{skill}: irrelevant degradation section")
            for capability, classification in non_native:
                if f"#### `{capability}` ({classification})" not in appendix:
                    errors.append(
                        f"{platform}/{skill}: missing degradation for '{capability}'")

            # Check generated body against the generator's source of truth.
            expected_content = _expected_adapter_output(skill, overlay)
            if content != expected_content:
                errors.append(
                    f"{platform}/{skill}: generated SKILL.md differs from generator output")

            # Check shipped references against generator source of truth,
            # including nested epistemic references and generated excerpts.
            expected_refs = _expected_reference_paths(skill, adapter_skill_dir)
            shipped_refs = _shipped_reference_paths(adapter_skill_dir)
            for missing in expected_refs - shipped_refs:
                errors.append(
                    f"{platform}/{skill}: missing generated reference '{missing}'")
            for extra in shipped_refs - expected_refs:
                errors.append(
                    f"{platform}/{skill}: ships unexpected reference '{extra}'")

    # Verify core skills have Required capabilities
    for skill in SKILLS:
        core_path = CORE_DIR / skill / "SKILL.md"
        content = core_path.read_text(encoding="utf-8")
        if "## Required capabilities" not in content:
            errors.append(
                f"core/{skill}: missing Required capabilities section")

    # Verify manifests exist and match
    for platform in PLATFORMS:
        manifest_path = ADAPTERS_DIR / platform / "manifest.json"
        if not manifest_path.exists():
            errors.append(f"MISSING: manifest for {platform}")
            continue

        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if manifest.get("platform") != platform:
                errors.append(f"{platform}: manifest platform mismatch")
            if not manifest.get("files"):
                errors.append(f"{platform}: manifest has no file entries")

            for entry in manifest["files"]:
                file_path = ROOT / entry["path"]
                if not file_path.exists():
                    errors.append(f"{platform}: manifest references missing file: {entry['path']}")
                    continue
                actual_sha = hashlib.sha256(file_path.read_bytes()).hexdigest()
                if entry.get("sha256") != actual_sha:
                    errors.append(
                        f"{platform}: manifest checksum mismatch for {entry['path']}")
        except (json.JSONDecodeError, KeyError) as e:
            errors.append(f"{platform}: invalid manifest: {e}")

    # Verify SHA256SUMS
    for platform in PLATFORMS:
        sums_path = ADAPTERS_DIR / platform / "SHA256SUMS"
        if not sums_path.exists():
            errors.append(f"MISSING: SHA256SUMS for {platform}")
            continue

        for line in sums_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                sha, rel = line.split("  ", 1)
                file_path = ADAPTERS_DIR / platform / rel
                if not file_path.exists():
                    errors.append(
                        f"{platform}: SHA256SUMS references missing file: {rel}")
                    continue
                actual = hashlib.sha256(file_path.read_bytes()).hexdigest()
                if sha != actual:
                    errors.append(
                        f"{platform}: SHA256SUMS mismatch for {rel}")
            except ValueError:
                errors.append(f"{platform}: malformed SHA256SUMS line: {line}")

    # Verify shared references exist
    for ref in ["WORK-OBJECT", "AGREEMENT-LOOP", "EVIDENCE-MODEL",
                "CONSEQUENCE-AUTHORITY", "CAPABILITY-DEGRADATION"]:
        ref_path = ROOT / "references" / f"{ref}.md"
        if not ref_path.exists():
            errors.append(f"MISSING: shared reference {ref}.md")

    # Verify .work-studio/config.md exists
    config_path = ROOT / ".work-studio" / "config.md"
    if not config_path.exists():
        errors.append("MISSING: .work-studio/config.md")

    return errors


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        sys.exit(0)

    run_matrix = "--matrix" in sys.argv or "--all" in sys.argv
    run_structure = "--structure" in sys.argv or "--all" in sys.argv

    if not run_matrix and not run_structure:
        print("Usage: verify-conformance.py [--matrix <files...>] [--structure] [--all]")
        sys.exit(1)

    all_errors = []

    if run_matrix:
        fixture_files = [a for a in sys.argv[1:] if a.endswith(".md")]
        if not fixture_files:
            # Default to all known fixture files
            fixtures_dir = ROOT / "fixtures"
            fixture_files = [str(p) for p in fixtures_dir.glob("slice-*.md")]
            fixture_files.append(
                str(fixtures_dir / "personal-institution-work-studio-contract.md"))

        print("=== Behavioral Matrix Verification ===")
        errors = verify_matrix(fixture_files)
        if errors:
            for e in errors:
                print(f"  FAIL: {e}")
            all_errors.extend(errors)
        else:
            print("  PASS: Matrix is complete and all fixtures are valid")
        print()

    if run_structure:
        print("=== Structural Adapter Verification ===")
        errors = verify_structure()
        if errors:
            for e in errors:
                print(f"  FAIL: {e}")
            all_errors.extend(errors)
        else:
            print("  PASS: All adapters contain required structural elements")
        print()

    if all_errors:
        print(f"\n{len(all_errors)} conformance error(s) found.")
        sys.exit(1)
    else:
        print("All conformance checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
