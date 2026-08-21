"""Focused checks for the support-adequacy dashboard reader (Direction 5).

Cases:
  1. Counts claims with zero or one distinct ledger source (below adequacy);
     a claim's scope (scalar or structured paths) never counts as a source.
  2. Does NOT count claims with two or more distinct ledger sources.
  3. Fails closed on a malformed CLM- block (visible ValueError).
  4. Decision 3 exclusion: a ledger row naming only the claim ID
     (registration/tracking) does NOT add a source.
  5. A ledger row sharing a substantive content token with the claim's text
     DOES add a source (content-level provenance).
  6. Structured (dict) scope does not crash the reader and is not a source.
"""

import os
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

from tools.ws.dashboard_signals import count_claims_below_support_adequacy


def _wo_body(claims: str, ledger: str = "") -> str:
    ledger_section = (
        "## Evidence ledger\n\n"
        "| Tag | Source | Entry |\n"
        "|-----|--------|-------|\n"
        f"{ledger}\n"
        if ledger
        else ""
    )
    return (
        "## Intent\n\nFixture for the support-adequacy tracer.\n\n"
        f"{ledger_section}"
        f"## Claims\n\n{claims}\n"
    )


@contextmanager
def workspace_with_wo(body: str):
    previous = Path.cwd()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        objects = root / ".work-studio" / "objects" / "2026" / "08"
        objects.mkdir(parents=True)
        (objects / "2026-08-08-999-fixture.md").write_text(
            "---\nid: 2026-08-08-999\n---\n" + body
        , encoding="utf-8")
        os.chdir(root)
        try:
            yield
        finally:
            os.chdir(previous)


class SupportAdequacyTest(unittest.TestCase):
    def test_counts_claims_with_zero_or_one_source(self):
        body = _wo_body(
            claims=(
                "  CLM-2026_08_08_999-001:\n"
                '    text: "single-sourced claim"\n'
                "    kind: inference\n"
                "    state: captured\n"
                '    scope: "refs/one"\n'
                "    created_at: 2026-08-08T00:00:00Z\n"
                "  CLM-2026_08_08_999-002:\n"
                '    text: "multi-sourced claim"\n'
                "    kind: inference\n"
                "    state: captured\n"
                '    scope: "refs/one"\n'
                "    created_at: 2026-08-08T00:00:00Z\n"
                "  CLM-2026_08_08_999-003:\n"
                '    text: "unsourced claim"\n'
                "    kind: inference\n"
                "    state: captured\n"
                "    created_at: 2026-08-08T00:00:00Z\n"
            ),
            ledger=(
                "| [system] | refs/two | Verification entry for "
                "CLM-2026_08_08_999-002 confirming the multi-sourced claim "
                "draws on a second ref. |\n"
            ),
        )
        with workspace_with_wo(body):
            # Scope is not a source. 001 has zero ledger sources; 003 has
            # zero; 002 has one (a substantive ledger row naming the ID and
            # sharing 'multi-sourced'). All three are below adequacy.
            self.assertEqual(count_claims_below_support_adequacy(), 3)

    def test_registration_row_does_not_add_source(self):
        body = _wo_body(
            claims=(
                "  CLM-2026_08_08_999-001:\n"
                '    text: "install drift persists in live skills"\n'
                "    kind: observation\n"
                "    state: captured\n"
                '    scope: "refs/taxonomy"\n'
                "    created_at: 2026-08-08T00:00:00Z\n"
            ),
            ledger=(
                "| [system] | implement-bounded-change, 2026-08-08 | "
                "Tracer executed: claim CLM-2026_08_08_999-001 registered. |\n"
            ),
        )
        with workspace_with_wo(body):
            # The row names the claim ID but shares no substantive content
            # token with the claim text, so it is a registration row (Decision
            # 3): it does NOT add a source. The claim's scope is not a source
            # either -> zero ledger sources -> below adequacy.
            self.assertEqual(count_claims_below_support_adequacy(), 1)

    def test_two_substantive_ledger_rows_reach_adequacy(self):
        body = _wo_body(
            claims=(
                "  CLM-2026_08_08_999-001:\n"
                '    text: "install drift persists in live skills"\n'
                "    kind: observation\n"
                "    state: captured\n"
                '    scope: "refs/taxonomy"\n'
                "    created_at: 2026-08-08T00:00:00Z\n"
            ),
            ledger=(
                "| [system] | refs/live-scan, 2026-08-08 | "
                "Live scan for CLM-2026_08_08_999-001 confirms install "
                "drift persists in the installed copy. |\n"
                "| [system] | refs/manual, 2026-08-08 | "
                "Manual check for CLM-2026_08_08_999-001 confirms install "
                "drift persists on a second host. |\n"
            ),
        )
        with workspace_with_wo(body):
            # Each row names the claim ID and shares content tokens (install,
            # drift, persists, ...) with the claim text, so both provide
            # content-level provenance. Scope is not a source: 2 distinct
            # ledger sources -> not below adequacy.
            self.assertEqual(count_claims_below_support_adequacy(), 0)

    def test_structured_scope_is_not_a_source_and_does_not_crash(self):
        body = _wo_body(
            claims=(
                "  CLM-2026_08_08_999-001:\n"
                '    text: "structured scope claim"\n'
                "    kind: inference\n"
                "    state: captured\n"
                "    scope:\n"
                "      paths: [refs/one]\n"
                "    created_at: 2026-08-08T00:00:00Z\n"
            ),
        )
        with workspace_with_wo(body):
            # Structured (dict) scope with paths is a defeater surface, not a
            # source, and must not crash the reader. No ledger provenance ->
            # below adequacy.
            self.assertEqual(count_claims_below_support_adequacy(), 1)

    def test_malformed_claim_fails_visibly(self):
        body = _wo_body(
            claims=(
                "  CLM-BROKEN:\n"
                '    text: "bad claim"\n'
            ),
        )
        with workspace_with_wo(body):
            with self.assertRaisesRegex(
                ValueError,
                r"2026-08-08-999-fixture\.md: malformed claim heading: CLM-BROKEN",
            ):
                count_claims_below_support_adequacy()

    def test_empty_workspace_returns_zero(self):
        with workspace_with_wo("## Intent\n\nNo claims.\n"):
            self.assertEqual(count_claims_below_support_adequacy(), 0)


if __name__ == "__main__":
    unittest.main()
