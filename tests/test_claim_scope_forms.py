"""Focused checks for dual-format claim scope parsing (tracer, 2026-08-09-004).

Covers the accepted tracer bullet's exit criteria:
  1. A structured claim round-trips through register -> parse -> inspect
     (paths held separately, plus git_commit/repository and revisit.on).
  2. The four real legacy scalar claims still parse as scalar strings
     (read-only regression, no mutation).
  3. Ambiguity probe: a scalar scope value containing special characters
     still parses as a scalar, not a structured mapping.
"""

import os
import tempfile
import unittest
from argparse import Namespace
from contextlib import contextmanager
from pathlib import Path

from tools.ws.claim import cmd_claim_register, parse_claims

REPO_ROOT = Path(__file__).resolve().parents[1]


def _wo_content(claims: str, consequence: str = "meaningful") -> str:
    return (
        "---\n"
        "id: 2026-08-09-999\n"
        "title: Scope-form fixture\n"
        "type: change\n"
        "status: active\n"
        "state: build\n"
        f"consequence: {consequence}\n"
        "sensitivity: ordinary\n"
        "created_at: 2026-08-09T00:00:00Z\n"
        "updated_at: 2026-08-09T00:00:00Z\n"
        "---\n"
        f"## Claims\n\n{claims}\n"
    )


@contextmanager
def workspace_with_wo(content: str, obj_id: str = "2026-08-09-999"):
    """Tempdir workspace with a fixture Work Object (mirrors dashboard tests)."""
    previous = Path.cwd()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        objects = root / ".work-studio" / "objects" / "2026" / "08"
        objects.mkdir(parents=True)
        (objects / f"{obj_id}-fixture.md").write_text(content)
        os.chdir(root)
        try:
            yield root
        finally:
            os.chdir(previous)


class TestStructuredRegisterRoundTrip(unittest.TestCase):
    def test_register_structured_claim_round_trips(self):
        """The 019-001 four-path case registers and parses back losslessly."""
        four_paths = [
            "skills/core/thinking-pressure-test-decision/SKILL.md",
            "fixtures/conflict-epistemic-tag-contract.md",
            "tools/ws/validate.py",
            "~/.claude/skills/alawas-thinking-pressure-test-decision/SKILL.md",
        ]
        content = _wo_content("", consequence="meaningful")
        with workspace_with_wo(content) as root:
            args = Namespace(
                id="2026-08-09-999",
                text="The six-tag taxonomy was reconciled, but live install drift persists",
                kind="observation",
                scope=None,
                paths=four_paths,
                git_commit="aefd8623",
                dirty_fingerprint=None,
                revisit_on=["validator-changed", "evidence-taxonomy-changed"],
                expect_updated="2026-08-09T00:00:00Z",
                force=False,
            )
            rc = cmd_claim_register(args)
            self.assertEqual(rc, 0)

            obj_file = (
                root / ".work-studio" / "objects" / "2026" / "08"
                / "2026-08-09-999-fixture.md"
            )
            body = obj_file.read_text()
            claims = parse_claims(body)
            self.assertEqual(len(claims), 1)
            claim = claims[0]
            self.assertIsInstance(claim["scope"], dict)
            self.assertEqual(claim["scope"]["paths"], four_paths)
            self.assertEqual(claim["scope"]["git_commit"], "aefd8623")
            self.assertEqual(claim["scope"]["repository"], "andrelawas-work-studio")
            self.assertNotIn("dirty_tree_fingerprint", claim["scope"])
            self.assertEqual(
                claim["revisit"]["on"],
                ["validator-changed", "evidence-taxonomy-changed"],
            )
            self.assertEqual(claim["state"], "captured")

    def test_register_scalar_claim_unchanged(self):
        """The legacy scalar path still emits and parses a flat scope string."""
        content = _wo_content("", consequence="meaningful")
        with workspace_with_wo(content) as root:
            args = Namespace(
                id="2026-08-09-999",
                text="Legacy scalar scope claim",
                kind="decision",
                scope="2026-07-27-016",
                paths=None,
                git_commit=None,
                dirty_fingerprint=None,
                revisit_on=None,
                expect_updated="2026-08-09T00:00:00Z",
                force=False,
            )
            rc = cmd_claim_register(args)
            self.assertEqual(rc, 0)

            obj_file = (
                root / ".work-studio" / "objects" / "2026" / "08"
                / "2026-08-09-999-fixture.md"
            )
            body = obj_file.read_text()
            claims = parse_claims(body)
            self.assertEqual(len(claims), 1)
            self.assertEqual(claims[0]["scope"], "2026-07-27-016")
            self.assertIsInstance(claims[0]["scope"], str)
            self.assertNotIn("revisit", claims[0])

    def test_register_rejects_missing_scope(self):
        content = _wo_content("", consequence="meaningful")
        with workspace_with_wo(content) as root:
            args = Namespace(
                id="2026-08-09-999",
                text="no scope",
                kind="observation",
                scope=None,
                paths=None,
                git_commit=None,
                dirty_fingerprint=None,
                revisit_on=None,
                expect_updated="2026-08-09T00:00:00Z",
                force=False,
            )
            rc = cmd_claim_register(args)
            self.assertEqual(rc, 1)


class TestParseStructuredBlock(unittest.TestCase):
    def test_parse_structured_block_direct(self):
        """Hand-authored structured block (doc form) parses into a dict scope."""
        claims_text = (
            "  CLM-2026_08_09_999-001:\n"
            '    text: "structured claim"\n'
            "    kind: observation\n"
            "    state: supported\n"
            "    scope:\n"
            '      repository: "andrelawas-work-studio"\n'
            '      git_commit: "abc123"\n'
            '      dirty_tree_fingerprint: "d3adbeef"\n'
            '      paths: ["a.py", "b/c.py"]\n'
            "    created_at: 2026-08-09T00:00:00Z\n"
            "    revisit:\n"
            '      on: ["validator-changed"]\n'
        )
        claims = parse_claims(_wo_content(claims_text))
        self.assertEqual(len(claims), 1)
        scope = claims[0]["scope"]
        self.assertEqual(scope["paths"], ["a.py", "b/c.py"])
        self.assertEqual(scope["repository"], "andrelawas-work-studio")
        self.assertEqual(scope["git_commit"], "abc123")
        self.assertEqual(scope["dirty_tree_fingerprint"], "d3adbeef")
        self.assertEqual(claims[0]["revisit"]["on"], ["validator-changed"])
        self.assertEqual(claims[0]["state"], "supported")


class TestAmbiguityProbe(unittest.TestCase):
    def test_scalar_scope_with_special_chars_stays_scalar(self):
        """A quoted scalar containing brackets/colons must not become a mapping."""
        claims_text = (
            "  CLM-2026_08_09_999-001:\n"
            '    text: "legacy"\n'
            "    kind: decision\n"
            "    state: captured\n"
            '    scope: "{a: b} references/epistemic/taxonomy.yaml"\n'
            "    created_at: 2026-08-09T00:00:00Z\n"
        )
        claims = parse_claims(_wo_content(claims_text))
        self.assertEqual(len(claims), 1)
        self.assertEqual(
            claims[0]["scope"], "{a: b} references/epistemic/taxonomy.yaml"
        )
        self.assertIsInstance(claims[0]["scope"], str)
        self.assertNotIn("revisit", claims[0])


class TestRealLegacyRegression(unittest.TestCase):
    def test_real_legacy_claims_parse_unchanged(self):
        """Read-only regression over the four frozen scalar claims."""
        obj_016 = (
            REPO_ROOT / ".work-studio/objects/2026/07"
            / "2026-07-27-016-build-claim-sidecar-register-and-inspect-for-"
              "meaningful-consequence-work-objects.md"
        )
        obj_019 = (
            REPO_ROOT / ".work-studio/objects/2026/07"
            / "2026-07-27-019-complete-tier-1-epistemic-layer-baseline-identity-"
              "evidence-schemas-and-tracer-1.md"
        )
        if not obj_016.exists() or not obj_019.exists():
            self.skipTest("real legacy claim objects not present")

        claims_016 = {c["id"]: c for c in parse_claims(obj_016.read_text())}
        claims_019 = {c["id"]: c for c in parse_claims(obj_019.read_text())}

        expected = {
            "CLM-2026_07_27_016-001": "2026-07-27-014/015",
            "CLM-2026_07_27_016-002": "2026-07-27-016",
            "CLM-2026_07_27_016-003": "2026-07-27-016/decision-3",
            "CLM-2026_07_27_019-001": "references/epistemic/taxonomy.yaml",
        }
        for cid, scope in expected.items():
            claim = claims_016.get(cid) or claims_019.get(cid)
            self.assertIsNotNone(claim, f"{cid} not found")
            self.assertEqual(claim["scope"], scope)
            self.assertIsInstance(claim["scope"], str)
            self.assertNotIn("revisit", claim)


if __name__ == "__main__":
    unittest.main()
