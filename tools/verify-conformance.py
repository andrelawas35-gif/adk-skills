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


def adapter_skill_name(skill):
    return f"{SKILL_NAMESPACE}-{skill}"


def namespaced_core_body(skill):
    body = (CORE_DIR / skill / "SKILL.md").read_text().split("---", 2)[2].lstrip("\n").rstrip("\n")
    for name in sorted(SKILLS, key=len, reverse=True):
        body = body.replace(f"`{name}`", f"`{adapter_skill_name(name)}`")
    return body


# ── Required structural elements ─────────────────────────────────────────────

REQUIRED_SECTIONS = [
    "## Governing principle",
    "## Boundaries and non-goals",
    "## Inputs and preconditions",
    "## Required capabilities",
    "## Consequence and authority rules",
    "## Agreement Loop behavior",
    "## Stage workflow",
    "## Evidence rules",
    "## Work Object updates",
    "## Routing and termination",
    "## Anti-patterns",
    "## Final self-check",
    "## Platform Adapter",
]

REQUIRED_ADAPTER_SUBSECTIONS = [
    "### Installation and precedence",
    "### Discovery",
    "### Capability Mappings",
    "### Declared Limitations",
    "### Integrity",
]

REQUIRED_CAPABILITY_CLASSIFICATIONS = {"native", "manual-fallback", "unsupported"}

REQUIRED_DEGRADATION_PATTERNS = [
    "Never mark verification, export, or deployment",
    "manual-fallback",
    "unsupported",
    "Stricter safety wins",
]


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
        content = path.read_text()

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
        elif name == "personal-institution-work-studio-contract.md":
            _check_patterns(errors, name, content, [
                "Scenario 1", "Scenario 2", "Scenario 3", "Scenario 4",
                "Scenario 5", "Scenario 6", "Private record does not enter",
                "Approved Evidence Bridge", "Chat does not silently",
                "stale Active-lens", "missing evidence as a gap",
                "Incompatible protocol versions", "manual, user-approved summary",
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
                "user's language", "explicit activation", "Evidence Bridge",
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
                "Approved Evidence Bridge", "Personal Institution archive",
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
        for skill in SKILLS:
            adapter_path = ADAPTERS_DIR / platform / "skills" / adapter_skill_name(skill) / "SKILL.md"
            if not adapter_path.exists():
                errors.append(f"MISSING: {adapter_path.relative_to(ROOT)}")
                continue

            content = adapter_path.read_text()

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

            # Check frontmatter has platform
            frontmatter = content.split("---", 2)[1]
            if f"platform: {platform}" not in frontmatter:
                errors.append(
                    f"{platform}/{skill}: frontmatter missing platform declaration")

            # Check capability mappings table
            if "| Abstract capability |" not in content:
                errors.append(
                    f"{platform}/{skill}: missing capability mappings table")

            # Check degradation section present
            if "### Capability Degradation" not in content:
                errors.append(
                    f"{platform}/{skill}: missing Capability Degradation section")

            # Check degradation patterns
            for pattern in REQUIRED_DEGRADATION_PATTERNS:
                if pattern.lower() not in content.lower():
                    errors.append(
                        f"{platform}/{skill}: missing degradation pattern '{pattern}'")

            # Check core body is preserved
            core_body = namespaced_core_body(skill)
            if core_body not in content:
                errors.append(
                    f"{platform}/{skill}: core body not preserved verbatim")

            # Check Generated-Artifact integrity markers
            if "This file is generated" not in content:
                errors.append(
                    f"{platform}/{skill}: missing generation warning")

    # Verify core skills have Required capabilities
    for skill in SKILLS:
        core_path = CORE_DIR / skill / "SKILL.md"
        content = core_path.read_text()
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
            manifest = json.loads(manifest_path.read_text())
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

        for line in sums_path.read_text().splitlines():
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

    # Verify overlays exist
    for platform in PLATFORMS:
        overlay_path = ADAPTERS_DIR / platform / "overlay.yaml"
        if not overlay_path.exists():
            errors.append(f"MISSING: overlay for {platform}")
            continue

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
