#!/usr/bin/env python3
"""Phase 6 handoff graph tests (WO 2026-08-17-008, slice 1).

Proves the accepted slice-1 design (Decision 2):
  1. fan-out to two read-only specialist branches + a deterministic join;
  2. a crash before the join resumes from the SQLite checkpoint without
     re-running the completed branches, and the join fires exactly once;
  3. explicit max_concurrency = 2;
and that no run touches canonical state (ADR 0025 / build plan 239).

Run under the uv-managed Python 3.11 environment:

    uv run python -m unittest discover -s runtime/tests -v
"""

import contextlib
import hashlib
import io
import json
import os
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from runtime.graph import (
    PHASE6_MAX_CONCURRENCY,
    Phase6Crash,
    backup_checkpoint_db,
    fork_phase6_thread,
    inspect_phase6,
    restore_checkpoint_db,
    run_phase6,
)
from runtime.graph import main as graph_main

ROOT = Path(__file__).resolve().parents[2]
TARGET_WO = "2026-08-22-011"


def _digest_work_studio() -> str:
    """Hash every canonical file so any change is observable."""
    h = hashlib.sha256()
    for p in sorted(ROOT.glob(".work-studio/**/*")):
        if p.is_file():
            h.update(str(p.relative_to(ROOT)).encode())
            h.update(p.read_bytes())
    return h.hexdigest()


class Phase6HandoffTests(unittest.TestCase):

    def test_fanout_join_runs_both_branches_and_join_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            checkpoint_db = tmp / "tracer.sqlite"
            before = _digest_work_studio()

            result = run_phase6(TARGET_WO, "fanout-join", checkpoint_db)

            self.assertIs(result["branch_a_completed"], True)
            self.assertIs(result["branch_b_completed"], True)
            self.assertIs(result["join_fired"], True)
            # WO 2026-08-17-001 Decision 6: derive_proposal returns the real
            # skill name from the conductor's routing table, keyed by state
            # only (role no longer differentiates) -- TARGET_WO is state
            # "build", so both branches independently propose the same real
            # skill: "implement-bounded-change".
            self.assertEqual("implement-bounded-change", result["join_proposal"])
            self.assertTrue(result.get("handoff_envelope"))
            self.assertTrue(result.get("branch_a_receipt"))
            self.assertTrue(result.get("branch_b_receipt"))
            # authority_scope is derived from TARGET_WO's consequence ("low").
            self.assertEqual(
                "read-only",
                result["handoff_envelope"]["authority_scope"],
                "authority_scope should be derived from TARGET_WO consequence",
            )
            # Both branches propose the same real skill for TARGET_WO's state.
            self.assertEqual(
                "implement-bounded-change", result["branch_a_receipt"]["proposed_next_skill"]
            )
            self.assertEqual(
                "implement-bounded-change", result["branch_b_receipt"]["proposed_next_skill"]
            )
            # Implement branch records no verification gaps; the verify branch
            # derives real gaps from TARGET_WO (evidence present, unchecked).
            self.assertEqual(
                [], result["branch_a_receipt"]["verification_gaps"],
                "implement branch records no verification gaps",
            )
            self.assertEqual(
                ["no checked success evidence"],
                result["branch_b_receipt"]["verification_gaps"],
                "verify branch gaps derived from TARGET_WO",
            )
            self.assertEqual(
                _digest_work_studio(), before,
                "canonical state changed across a run",
            )

    def test_crash_before_join_resumes_without_duplicated_join(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            checkpoint_db = tmp / "tracer.sqlite"
            branch_marker = tmp / "branches.txt"
            crash_marker = tmp / "crash.txt"
            before = _digest_work_studio()

            thread_id = "crash-before-join"
            env = {
                "PHASE6_BRANCH_MARKER": str(branch_marker),
                "PHASE6_CRASH_NODE": "join",
                "PHASE6_CRASH_MARKER": str(crash_marker),
            }

            # Run 1: both branches complete, then join raises the sentinel.
            with patch.dict(os.environ, env):
                with self.assertRaises(Phase6Crash):
                    run_phase6(TARGET_WO, thread_id, checkpoint_db)

            state = inspect_phase6(thread_id, checkpoint_db)
            self.assertIs(state["branch_a_completed"], True)
            self.assertIs(state["branch_b_completed"], True)
            self.assertIs(state["join_fired"], False)
            # Each branch recorded exactly one side effect.
            self.assertEqual(
                2, len(branch_marker.read_text(encoding="utf-8").splitlines())
            )

            # Run 2: resume the same thread; join fires, branches do not re-run.
            with patch.dict(os.environ, env):
                result = run_phase6(
                    TARGET_WO, thread_id, checkpoint_db, resume=True
                )
            self.assertIs(result["join_fired"], True)
            self.assertEqual("implement-bounded-change", result["join_proposal"])
            self.assertEqual(
                2, len(branch_marker.read_text(encoding="utf-8").splitlines()),
                "a branch re-ran after resume",
            )
            # The join fired exactly once across crash + resume.
            self.assertEqual(
                "join-attempt-1\n",
                crash_marker.read_text(encoding="utf-8"),
            )
            self.assertEqual(
                _digest_work_studio(), before,
                "canonical state changed across crash/resume",
            )

    def test_derive_proposal_is_pure_and_deterministic(self):
        """WO 2026-08-17-001 Decision 6: the WO-state -> proposal mapping
        returns the real skill name from the conductor's routing table
        (governance-conduct-work-object/SKILL.md's state->skill table),
        keyed by state only -- role no longer affects the result."""
        from runtime.handoff import derive_proposal

        cases = [
            # (state, role, expected proposal) -- mirrors the conductor's
            # 8-row routing table exactly; role is accepted but ignored.
            ("notice", "implement", "turn-signal-into-work"),
            ("explore", "implement", "develop-idea"),
            ("design", "implement", "design-tracer-bullet"),
            ("build", "implement", "implement-bounded-change"),
            ("verify", "implement", "verify-release-evidence"),
            ("release", "implement", "deploy-with-recovery"),
            ("observe", "implement", "review-outcome-and-adapt"),
            ("close", "implement", "review-outcome-and-adapt"),
            # role has no effect on the outcome -- same states, different role.
            ("design", "verify", "design-tracer-bullet"),
            ("build", "verify", "implement-bounded-change"),
            ("build", "other-role", "implement-bounded-change"),
            # Unrecognized/empty state still defers to the director.
            ("unknown", "implement", "await-director"),
            ("", "verify", "await-director"),
        ]
        for state, role, expected in cases:
            with self.subTest(state=state, role=role):
                self.assertEqual(expected, derive_proposal(state, role))
        # Deterministic: repeated calls return identical results.
        self.assertEqual(
            derive_proposal("build", "verify"),
            derive_proposal("build", "verify"),
        )

    def test_derive_authority_scope_is_pure_and_deterministic(self):
        """The consequence -> authority-scope mapping is deterministic and grounded."""
        from runtime.handoff import derive_authority_scope

        cases = [
            # (consequence, expected authority_scope)
            ("low", "read-only"),
            ("meaningful", "read-only-propose"),
            ("high", "governed"),
            ("", "unknown"),
            ("unknown", "unknown"),
            ("private", "unknown"),
            ("restricted", "unknown"),
        ]
        for consequence, expected in cases:
            with self.subTest(consequence=consequence):
                self.assertEqual(expected, derive_authority_scope(consequence))
        # Deterministic: repeated calls return identical results.
        self.assertEqual(
            derive_authority_scope("low"), derive_authority_scope("low")
        )

    def test_derive_verification_gaps_is_pure_and_deterministic(self):
        """The verification-signal -> gaps mapping is deterministic and read-only."""
        from runtime.handoff import derive_verification_gaps

        cases = [
            # (has_checked_success_evidence, has_evidence_ledger_entries, gaps)
            (True, True, []),
            (True, False, ["no evidence ledger entries"]),
            (False, True, ["no checked success evidence"]),
            (
                False,
                False,
                ["no checked success evidence", "no evidence ledger entries"],
            ),
        ]
        for has_checked, has_ledger, expected in cases:
            with self.subTest(has_checked=has_checked, has_ledger=has_ledger):
                self.assertEqual(
                    expected, derive_verification_gaps(has_checked, has_ledger)
                )
        # Deterministic: repeated calls return identical results.
        self.assertEqual(
            derive_verification_gaps(False, True),
            derive_verification_gaps(False, True),
        )

    def test_fork_phase6_resumes_crashed_before_join(self):
        """A crash-before-join thread can be forked to a sibling and completed."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            checkpoint_db = tmp / "tracer.sqlite"
            crash_marker = tmp / "crash.txt"
            before = _digest_work_studio()

            thread_id = "fork-source"
            sibling = "fork-sibling"
            env = {
                "PHASE6_CRASH_NODE": "join",
                "PHASE6_CRASH_MARKER": str(crash_marker),
            }

            with patch.dict(os.environ, env):
                with self.assertRaises(Phase6Crash):
                    run_phase6(TARGET_WO, thread_id, checkpoint_db)

            # Fork the crashed (branches-done, join-pending) thread to a sibling.
            forked = fork_phase6_thread(thread_id, sibling, checkpoint_db)
            self.assertEqual(thread_id, forked["source_thread_id"])
            self.assertEqual(sibling, forked["thread_id"])

            state = inspect_phase6(sibling, checkpoint_db)
            self.assertTrue(state["has_envelope"])
            self.assertTrue(state["branch_a_completed"])
            self.assertTrue(state["branch_b_completed"])
            self.assertFalse(state["join_fired"])

            # Resume the sibling: join fires exactly once, deterministic proposal.
            result = run_phase6(TARGET_WO, sibling, checkpoint_db, resume=True)
            self.assertTrue(result["join_fired"])
            # WO 2026-08-17-001 Decision 6: derive_proposal is state-keyed (real
            # skill names), so both branches propose the same skill for TARGET_WO
            # (state "build") -- the fork/resume must preserve that determinism.
            self.assertEqual(
                "implement-bounded-change",
                result["join_proposal"],
            )
            self.assertEqual(
                _digest_work_studio(), before,
                "canonical state changed across fork/resume",
            )

    def test_fork_phase6_error_paths(self):
        """Fork refuses an empty source and an occupied target."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            checkpoint_db = tmp / "tracer.sqlite"

            # Populate the DB so it is usable.
            run_phase6(TARGET_WO, "source", checkpoint_db)

            # Empty source: a thread that has never run.
            with self.assertRaises(ValueError):
                fork_phase6_thread("missing", "sibling", checkpoint_db)

            # Occupied target: a thread that already has checkpoint state.
            fork_phase6_thread("source", "taken", checkpoint_db)
            with self.assertRaises(ValueError):
                fork_phase6_thread("source", "taken", checkpoint_db)

    def test_backup_restore_roundtrip_resumes_crashed_before_join(self):
        """A crash-before-join thread survives backup -> delete -> restore -> resume."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            checkpoint_db = tmp / "tracer.sqlite"
            backup_dir = tmp / "backups"
            crash_marker = tmp / "crash.txt"
            before = _digest_work_studio()

            thread_id = "br-source"
            env = {
                "PHASE6_CRASH_NODE": "join",
                "PHASE6_CRASH_MARKER": str(crash_marker),
            }

            with patch.dict(os.environ, env):
                with self.assertRaises(Phase6Crash):
                    run_phase6(TARGET_WO, thread_id, checkpoint_db)

            # Backup the Phase 6 checkpoint DB.
            backup = backup_checkpoint_db(checkpoint_db, backup_dir)
            self.assertTrue(backup.backup_path.exists())

            # Delete the live DB, then restore from the backup.
            checkpoint_db.unlink()
            restored = restore_checkpoint_db(backup.backup_path, checkpoint_db)
            self.assertEqual(checkpoint_db, restored.restored_checkpoint_db)

            # Inspect the restored thread: same state as before the crash.
            state = inspect_phase6(thread_id, checkpoint_db)
            self.assertTrue(state["has_envelope"])
            self.assertTrue(state["branch_a_completed"])
            self.assertTrue(state["branch_b_completed"])
            self.assertFalse(state["join_fired"])

            # Resume the restored thread: join fires exactly once.
            result = run_phase6(TARGET_WO, thread_id, checkpoint_db, resume=True)
            self.assertTrue(result["join_fired"])
            self.assertEqual(
                "implement-bounded-change",
                result["join_proposal"],
            )
            self.assertEqual(
                _digest_work_studio(), before,
                "canonical state changed across backup/restore/resume",
            )

    def test_backup_restore_error_paths(self):
        """Backup of a missing DB and restore to an existing target both fail."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            checkpoint_db = tmp / "tracer.sqlite"
            backup_dir = tmp / "backups"

            # Backup of a missing DB.
            with self.assertRaises(FileNotFoundError):
                backup_checkpoint_db(checkpoint_db, backup_dir)

            # Populate a DB, back it up, then restore into an existing target.
            run_phase6(TARGET_WO, "br-source", checkpoint_db)
            backup = backup_checkpoint_db(checkpoint_db, backup_dir)
            with self.assertRaises(FileExistsError):
                restore_checkpoint_db(backup.backup_path, checkpoint_db)

    def test_backup_restore_cli_roundtrip_for_phase6(self):
        """The backup/restore/inspect-phase6/run-phase6 CLI subcommands work on a
        Phase 6 checkpoint DB (exercised through the real main() dispatch)."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            checkpoint_db = tmp / "tracer.sqlite"
            backup_dir = tmp / "backups"
            crash_marker = tmp / "crash.txt"
            before = _digest_work_studio()

            thread_id = "cli-br"
            env = {
                "PHASE6_CRASH_NODE": "join",
                "PHASE6_CRASH_MARKER": str(crash_marker),
            }
            with patch.dict(os.environ, env):
                with self.assertRaises(Phase6Crash):
                    run_phase6(TARGET_WO, thread_id, checkpoint_db)

            def cli_json(args):
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rc = graph_main(args)
                self.assertEqual(0, rc)
                return json.loads(buf.getvalue())

            backup = cli_json([
                "backup", "--checkpoint-db", str(checkpoint_db),
                "--backup-dir", str(backup_dir),
            ])
            self.assertTrue(Path(backup["backup_path"]).exists())

            checkpoint_db.unlink()
            restored = cli_json([
                "restore", "--backup", backup["backup_path"],
                "--checkpoint-db", str(checkpoint_db),
            ])
            self.assertEqual(str(checkpoint_db), restored["restored_checkpoint_db"])

            state = cli_json([
                "inspect-phase6", thread_id,
                "--checkpoint-db", str(checkpoint_db),
            ])
            self.assertTrue(state["has_envelope"])
            self.assertTrue(state["branch_a_completed"])
            self.assertTrue(state["branch_b_completed"])
            self.assertFalse(state["join_fired"])

            result = cli_json([
                "run-phase6", TARGET_WO, thread_id,
                "--checkpoint-db", str(checkpoint_db), "--resume",
            ])
            self.assertTrue(result["join_fired"])
            self.assertEqual(
                "implement-bounded-change",
                result["join_proposal"],
            )
            self.assertEqual(
                _digest_work_studio(), before,
                "canonical state changed across CLI backup/restore",
            )

    def test_merge_proposals_is_pure_and_deterministic(self):
        """The join's proposal merge is deterministic and deduplicates."""
        from runtime.handoff import merge_proposals

        cases = [
            ([], ""),
            ([{"proposed_next_skill": "implement-bounded-change"}],
             "implement-bounded-change"),
            ([{"proposed_next_skill": "implement-bounded-change"},
              {"proposed_next_skill": "implement-bounded-change"}],
             "implement-bounded-change"),
            ([{"proposed_next_skill": "verify-release-evidence"},
              {"proposed_next_skill": "implement-bounded-change"}],
             "implement-bounded-change; verify-release-evidence"),
            ([{"proposed_next_skill": ""},
              {"proposed_next_skill": "implement-bounded-change"}],
             "implement-bounded-change"),
        ]
        for receipts, expected in cases:
            with self.subTest(receipts=receipts):
                self.assertEqual(expected, merge_proposals(receipts))
        # Order-independent: sorted output regardless of receipt order.
        self.assertEqual(
            merge_proposals([{"proposed_next_skill": "x"},
                             {"proposed_next_skill": "y"}]),
            merge_proposals([{"proposed_next_skill": "y"},
                             {"proposed_next_skill": "x"}]),
        )

    def test_multi_state_determinism_across_lifecycle(self):
        """The Phase 6 graph derives correct, deterministic signals for real WOs
        across lifecycle states (self-discovering; no whole-tree digest)."""
        from runtime.graph import _phase6_wo_verification_signals, _read_frontmatter
        from runtime.handoff import (
            _STATE_ROUTING_TABLE,
            derive_authority_scope,
            derive_verification_gaps,
        )

        # Self-discover one real WO per routing-table state.
        by_state: dict = {}
        for p in sorted((ROOT / ".work-studio" / "objects").rglob("*.md")):
            if ".bak-" in p.name:
                continue
            try:
                fm = _read_frontmatter(p)
            except ValueError:
                continue  # not a Work Object (e.g. README.md)
            st = fm.get("state", "")
            if st in _STATE_ROUTING_TABLE and st not in by_state:
                by_state[st] = (p, fm)

        self.assertGreaterEqual(
            len(by_state), 3,
            "expected real WOs across several lifecycle states",
        )

        for state, (wo_path, fm) in sorted(by_state.items()):
            with self.subTest(state=state, wo=wo_path.stem):
                wo_id = fm["id"]
                expected_proposal = _STATE_ROUTING_TABLE[state]
                expected_authority = derive_authority_scope(
                    fm.get("consequence", "")
                )
                expected_gaps = derive_verification_gaps(
                    *_phase6_wo_verification_signals(wo_path)
                )

                with tempfile.TemporaryDirectory() as tmp:
                    tmp = Path(tmp)
                    result = run_phase6(wo_id, f"state-{state}", tmp / "t.sqlite")
                    if result.get("business_handoff_envelope"):
                        expected_proposal = (
                            result["business_handoff_envelope"]["to_skill"]
                        )
                    self.assertEqual(expected_proposal, result["join_proposal"], state)
                    self.assertEqual(
                        expected_authority,
                        result["handoff_envelope"]["authority_scope"],
                        state,
                    )
                    self.assertEqual(
                        expected_gaps,
                        result["branch_b_receipt"]["verification_gaps"],
                        state,
                    )
                    # Determinism: a fresh run yields the same proposal.
                    result2 = run_phase6(
                        wo_id, f"state-{state}-2", tmp / "t2.sqlite"
                    )
                    self.assertEqual(
                        result["join_proposal"], result2["join_proposal"], state
                    )

    def test_state_routing_table_stays_in_sync_with_conductor(self):
        """The runtime routing table must not silently drift from the conductor's."""
        from runtime.handoff import _STATE_ROUTING_TABLE

        skill_path = (
            ROOT / "skills" / "core"
            / "governance-conduct-work-object" / "SKILL.md"
        )
        self.assertTrue(skill_path.exists(), f"conductor skill missing: {skill_path}")
        text = skill_path.read_text(encoding="utf-8")

        # Parse the conductor's state -> skill routing rows: "| state | skill ... |"
        states = (
            "notice", "explore", "design", "build", "verify",
            "release", "observe", "close",
        )
        conductor = {}
        for line in text.splitlines():
            m = re.match(
                r"^\|\s*(%s)\s*\|\s*([a-z0-9-]+)" % "|".join(states),
                line,
            )
            if m:
                conductor[m.group(1)] = m.group(2)

        self.assertEqual(
            set(_STATE_ROUTING_TABLE), set(conductor),
            "runtime routing states diverged from the conductor",
        )
        for state, skill in _STATE_ROUTING_TABLE.items():
            self.assertEqual(
                skill, conductor[state],
                f"runtime routes {state} -> {skill} but conductor routes it elsewhere",
            )

    def test_max_concurrency_is_explicit(self):
        self.assertEqual(2, PHASE6_MAX_CONCURRENCY)

    def test_four_crash_point_matrix(self):
        """A crash at any of the four superstep boundaries resumes cleanly.

        Observed intermediate states (verified by experiment, 2026-08-17): a
        crash at a node's start persists the completed parallel sibling's
        superstep (branch_b stays completed when branch_a crashes, and vice
        versa), so each branch runs exactly once across crash + resume.
        """
        # (has_envelope, branch_a_completed, branch_b_completed) after the crash.
        expected_intermediate = {
            "dispatch": (False, False, False),
            "branch_a": (True, False, True),
            "branch_b": (True, True, False),
            "join": (True, True, True),
        }
        for node, (has_env, a_done, b_done) in expected_intermediate.items():
            with self.subTest(node=node):
                with tempfile.TemporaryDirectory() as tmp:
                    tmp = Path(tmp)
                    checkpoint_db = tmp / "tracer.sqlite"
                    branch_marker = tmp / "branches.txt"
                    crash_marker = tmp / "crash.txt"
                    before = _digest_work_studio()
                    thread_id = f"matrix-{node}"
                    env = {
                        "PHASE6_BRANCH_MARKER": str(branch_marker),
                        "PHASE6_CRASH_NODE": node,
                        "PHASE6_CRASH_MARKER": str(crash_marker),
                    }

                    # Run 1: crash once at the named node's first attempt.
                    with patch.dict(os.environ, env):
                        with self.assertRaises(Phase6Crash):
                            run_phase6(TARGET_WO, thread_id, checkpoint_db)

                    state = inspect_phase6(thread_id, checkpoint_db)
                    self.assertEqual(has_env, state["has_envelope"], node)
                    self.assertEqual(a_done, state["branch_a_completed"], node)
                    self.assertEqual(b_done, state["branch_b_completed"], node)
                    self.assertFalse(state["join_fired"], node)
                    self.assertEqual(
                        f"{node}-attempt-1\n",
                        crash_marker.read_text(encoding="utf-8"),
                        node,
                    )

                    # Run 2: resume; join fires once, branches do not re-run.
                    with patch.dict(os.environ, env):
                        result = run_phase6(
                            TARGET_WO, thread_id, checkpoint_db, resume=True
                        )
                    self.assertTrue(result["join_fired"], node)
                    self.assertEqual(
                        "implement-bounded-change", result["join_proposal"], node
                    )
                    self.assertEqual(
                        2,
                        len(
                            branch_marker.read_text(
                                encoding="utf-8"
                            ).splitlines()
                        ),
                        f"a branch re-ran at crash point {node}",
                    )
                    self.assertEqual(
                        _digest_work_studio(), before,
                        f"canonical state changed at crash point {node}",
                    )


class Phase6DirectionGateTests(unittest.TestCase):
    """direction_gate: the join transition pauses for explicit director
    approval (WO 2026-08-17-016 Decision 11), and its resume mechanism
    (Command(resume=...) via approve_direction) never conflicts with the
    pre-existing crash-checkpoint resume mechanism (resume=True)."""

    def test_run_pauses_after_join_before_direction_is_answered(self):
        with tempfile.TemporaryDirectory() as tmp:
            checkpoint_db = Path(tmp) / "tracer.sqlite"
            thread_id = "direction-pause"

            result = run_phase6(TARGET_WO, thread_id, checkpoint_db)

            self.assertIn("__interrupt__", result)
            self.assertTrue(result.get("join_fired"))
            self.assertNotIn("direction_approved", result)

            state = inspect_phase6(thread_id, checkpoint_db)
            self.assertTrue(state["join_fired"])

    def test_approve_direction_true_and_false_complete_with_matching_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            checkpoint_db = Path(tmp) / "tracer.sqlite"

            run_phase6(TARGET_WO, "direction-approve", checkpoint_db)
            approved = run_phase6(
                TARGET_WO, "direction-approve", checkpoint_db, approve_direction=True
            )
            self.assertIs(approved.get("direction_approved"), True)
            self.assertNotIn("__interrupt__", approved)

            run_phase6(TARGET_WO, "direction-reject", checkpoint_db)
            rejected = run_phase6(
                TARGET_WO, "direction-reject", checkpoint_db, approve_direction=False
            )
            self.assertIs(rejected.get("direction_approved"), False)
            self.assertNotIn("__interrupt__", rejected)

    def test_crash_checkpoint_resume_and_direction_approval_compose_on_one_thread(self):
        """The riskiest assumption behind Decision 11: a thread can recover
        from an in-process crash (resume=True) and then, separately, have
        its direction interrupt answered (approve_direction=True) -- the two
        resume mechanisms never need to apply in the same invoke() call."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            checkpoint_db = tmp / "tracer.sqlite"
            branch_marker = tmp / "branches.txt"
            crash_marker = tmp / "crash.txt"
            thread_id = "crash-then-approve"
            env = {
                "PHASE6_BRANCH_MARKER": str(branch_marker),
                "PHASE6_CRASH_NODE": "branch_a",
                "PHASE6_CRASH_MARKER": str(crash_marker),
            }

            # Run 1: crashes at branch_a's first attempt.
            with patch.dict(os.environ, env):
                with self.assertRaises(Phase6Crash):
                    run_phase6(TARGET_WO, thread_id, checkpoint_db)

            # Run 2: crash-checkpoint resume gets past the crash, through
            # join, and up to (but not past) the new direction_gate pause.
            with patch.dict(os.environ, env):
                paused = run_phase6(TARGET_WO, thread_id, checkpoint_db, resume=True)
            self.assertIn("__interrupt__", paused)
            self.assertTrue(paused.get("join_fired"))
            self.assertNotIn("direction_approved", paused)

            # Run 3: a separate, later call answers the interrupt.
            final = run_phase6(
                TARGET_WO, thread_id, checkpoint_db, approve_direction=True
            )
            self.assertIs(final.get("direction_approved"), True)
            self.assertNotIn("__interrupt__", final)
            self.assertEqual(
                2, len(branch_marker.read_text(encoding="utf-8").splitlines()),
                "a branch re-ran across the crash/resume/approve sequence",
            )


if __name__ == "__main__":
    unittest.main()
