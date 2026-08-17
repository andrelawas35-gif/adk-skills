#!/usr/bin/env python3
"""Kill/resume regression test for the 2-node checkpointed graph (WO 2026-08-15-008).

Proves Decision 2's riskiest assumption: a process killed mid-run (after node 1
completes, before node 2 finishes) resumes from the SQLite checkpoint without
re-executing node 1, and touches no canonical state.

Run under the uv-managed Python 3.11 environment (langgraph + checkpoint-sqlite
installed; `sys.executable` is the venv python):

    uv run --python 3.11 python -m unittest discover -s runtime/tests -v
"""

import hashlib
import json
import os
import signal
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

from runtime.graph import build_checkpoint_serializer, recover_checkpoint_db

ROOT = Path(__file__).resolve().parents[2]
TARGET_WO = "2026-07-27-001"
GRAPH_MODULE = ["-m", "runtime.graph"]


def _digest_work_studio() -> str:
    """Hash every canonical file so any change is observable."""
    h = hashlib.sha256()
    for p in sorted(ROOT.glob(".work-studio/**/*")):
        if p.is_file():
            h.update(str(p.relative_to(ROOT)).encode())
            h.update(p.read_bytes())
    return h.hexdigest()


def _run_graph(args, env, timeout=120):
    return subprocess.Popen(
        [sys.executable, *GRAPH_MODULE, *args],
        cwd=str(ROOT), env=env,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )


class KillResumeTests(unittest.TestCase):

    def test_kill_after_node1_resumes_without_reexecution(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            checkpoint_db = tmp / "tracer.sqlite"
            marker = tmp / "marker.txt"
            signal_file = tmp / "node2_started"

            before = _digest_work_studio()

            # ── Run 1: kill after node 2 starts (node 1's checkpoint committed).
            env1 = dict(os.environ)
            env1["GRAPH_NODE2_SIGNAL_FILE"] = str(signal_file)
            env1["GRAPH_NODE2_SLEEP_SECONDS"] = "60"  # wide window to kill
            proc = _run_graph([TARGET_WO, "kill-resume-test", str(marker),
                               "--checkpoint-db", str(checkpoint_db)], env1)

            # Wait (bounded) for node 2 to start, proving node 1 finished.
            deadline = time.time() + 60
            while time.time() < deadline and not signal_file.exists():
                if proc.poll() is not None:
                    out, err = proc.communicate()
                    self.fail(f"graph exited before node 2 started: {out} {err}")
                time.sleep(0.05)
            self.assertTrue(signal_file.exists(), "node 2 never started")
            proc.send_signal(signal.SIGKILL)
            proc.wait(timeout=10)
            # Close the killed process's pipes to avoid dangling descriptors.
            proc.communicate()

            # Node 1 must have recorded exactly one side effect.
            marker_lines = marker.read_text(encoding="utf-8").splitlines()
            self.assertEqual(1, len(marker_lines),
                             f"node 1 side effect count: {len(marker_lines)}")
            self.assertTrue(marker_lines[0].startswith("load_envelope:"))

            # ── Run 2: resume the same thread_id without the kill window.
            env2 = dict(os.environ)  # no signal/sleep hooks
            result = subprocess.run(
                [sys.executable, *GRAPH_MODULE, TARGET_WO, "kill-resume-test",
                 str(marker), "--checkpoint-db", str(checkpoint_db), "--resume"],
                cwd=str(ROOT), env=env2, capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("'node2_completed': True", result.stdout)

            # Node 1 must NOT have re-executed; node 2 completed.
            marker_lines = marker.read_text(encoding="utf-8").splitlines()
            self.assertEqual(1, len(marker_lines),
                             f"node 1 re-executed: {len(marker_lines)} lines")

            # Canonical state must be byte-identical across kill + resume.
            after = _digest_work_studio()
            self.assertEqual(before, after,
                             "canonical state changed across kill/resume")


class CheckpointRecoveryTests(unittest.TestCase):

    def test_missing_checkpoint_db_recovers_without_canonical_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            checkpoint_db = tmp / "missing" / "tracer.sqlite"
            before = _digest_work_studio()

            recovery = recover_checkpoint_db(checkpoint_db)

            self.assertEqual("created_missing", recovery.status)
            self.assertEqual(checkpoint_db, recovery.checkpoint_db)
            self.assertIsNone(recovery.quarantine_path)
            self.assertFalse(checkpoint_db.exists())
            self.assertEqual(before, _digest_work_studio())

    def test_corrupt_checkpoint_db_is_quarantined_without_canonical_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            checkpoint_db = tmp / "tracer.sqlite"
            checkpoint_db.write_bytes(b"not a sqlite checkpoint db")
            before = _digest_work_studio()

            recovery = recover_checkpoint_db(checkpoint_db)

            self.assertEqual("quarantined_corrupt", recovery.status)
            self.assertEqual(checkpoint_db, recovery.checkpoint_db)
            self.assertIsNotNone(recovery.quarantine_path)
            self.assertFalse(checkpoint_db.exists())
            self.assertTrue(recovery.quarantine_path.exists())
            self.assertEqual(
                b"not a sqlite checkpoint db",
                recovery.quarantine_path.read_bytes(),
            )
            self.assertEqual(before, _digest_work_studio())

    def test_graph_runs_after_corrupt_checkpoint_db_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            checkpoint_db = tmp / "tracer.sqlite"
            marker = tmp / "marker.txt"
            checkpoint_db.write_bytes(b"not a sqlite checkpoint db")
            before = _digest_work_studio()

            result = subprocess.run(
                [sys.executable, *GRAPH_MODULE, TARGET_WO, "corrupt-recovery-test",
                 str(marker), "--checkpoint-db", str(checkpoint_db)],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("'node2_completed': True", result.stdout)
            self.assertEqual(
                [f"load_envelope:{TARGET_WO}"],
                marker.read_text(encoding="utf-8").splitlines(),
            )
            quarantined = list(tmp.glob("tracer.sqlite.corrupt-*"))
            self.assertEqual(1, len(quarantined))
            self.assertTrue(checkpoint_db.exists())
            self.assertEqual(before, _digest_work_studio())


class IdempotencyReceiptTests(unittest.TestCase):

    def test_duplicate_invocation_replays_marker_side_effect_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            checkpoint_db = tmp / "tracer.sqlite"
            idempotency_db = tmp / "idempotency.sqlite"
            marker = tmp / "marker.txt"
            thread_id = "duplicate-receipt-test"
            before = _digest_work_studio()

            command = [
                sys.executable, *GRAPH_MODULE, TARGET_WO, thread_id, str(marker),
                "--checkpoint-db", str(checkpoint_db),
                "--idempotency-db", str(idempotency_db),
            ]
            first = subprocess.run(
                command, cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            second = subprocess.run(
                command, cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )

            self.assertEqual(0, first.returncode, first.stderr)
            self.assertEqual(0, second.returncode, second.stderr)
            self.assertIn("'node2_completed': True", first.stdout)
            self.assertIn("'node2_completed': True", second.stdout)
            self.assertEqual(
                [f"load_envelope:{TARGET_WO}"],
                marker.read_text(encoding="utf-8").splitlines(),
            )
            with sqlite3.connect(str(idempotency_db)) as conn:
                rows = conn.execute(
                    """
                    SELECT thread_id, work_object_id, effect_name
                    FROM idempotency_receipts
                    """
                ).fetchall()
            self.assertEqual(
                [(thread_id, TARGET_WO, "load_envelope_marker")],
                rows,
            )
            self.assertEqual(before, _digest_work_studio())


class OperatorCommandTests(unittest.TestCase):

    def test_inspect_resume_and_fork_commands_are_runtime_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            checkpoint_db = tmp / "tracer.sqlite"
            idempotency_db = tmp / "idempotency.sqlite"
            marker = tmp / "marker.txt"
            source_thread_id = "operator-source"
            forked_thread_id = "operator-forked"
            before = _digest_work_studio()

            run_result = subprocess.run(
                [
                    sys.executable, *GRAPH_MODULE, "run",
                    TARGET_WO, source_thread_id, str(marker),
                    "--checkpoint-db", str(checkpoint_db),
                    "--idempotency-db", str(idempotency_db),
                ],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(0, run_result.returncode, run_result.stderr)
            self.assertEqual(
                [f"load_envelope:{TARGET_WO}"],
                marker.read_text(encoding="utf-8").splitlines(),
            )

            inspect_result = subprocess.run(
                [
                    sys.executable, *GRAPH_MODULE, "inspect", source_thread_id,
                    "--checkpoint-db", str(checkpoint_db),
                ],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(0, inspect_result.returncode, inspect_result.stderr)
            inspected = json.loads(inspect_result.stdout)
            self.assertEqual("usable", inspected["recovery_status"])
            self.assertEqual(source_thread_id, inspected["thread_id"])
            self.assertEqual([], inspected["next"])
            self.assertTrue(inspected["values"]["node1_completed"])
            self.assertTrue(inspected["values"]["node2_completed"])

            resume_result = subprocess.run(
                [
                    sys.executable, *GRAPH_MODULE, "resume",
                    TARGET_WO, source_thread_id, str(marker),
                    "--checkpoint-db", str(checkpoint_db),
                    "--idempotency-db", str(idempotency_db),
                ],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(0, resume_result.returncode, resume_result.stderr)
            resumed = json.loads(resume_result.stdout)
            self.assertTrue(resumed["node2_completed"])
            self.assertEqual(
                [f"load_envelope:{TARGET_WO}"],
                marker.read_text(encoding="utf-8").splitlines(),
            )

            fork_result = subprocess.run(
                [
                    sys.executable, *GRAPH_MODULE, "fork",
                    source_thread_id, forked_thread_id,
                    "--checkpoint-db", str(checkpoint_db),
                ],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(0, fork_result.returncode, fork_result.stderr)
            forked = json.loads(fork_result.stdout)
            self.assertEqual(source_thread_id, forked["source_thread_id"])
            self.assertEqual(forked_thread_id, forked["thread_id"])
            self.assertEqual([], forked["next"])
            self.assertEqual(forked_thread_id, forked["values"]["thread_id"])
            self.assertTrue(forked["values"]["node1_completed"])
            self.assertTrue(forked["values"]["node2_completed"])

            fork_inspect_result = subprocess.run(
                [
                    sys.executable, *GRAPH_MODULE, "inspect", forked_thread_id,
                    "--checkpoint-db", str(checkpoint_db),
                ],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(0, fork_inspect_result.returncode,
                             fork_inspect_result.stderr)
            fork_inspected = json.loads(fork_inspect_result.stdout)
            self.assertEqual(forked_thread_id,
                             fork_inspected["values"]["thread_id"])
            self.assertEqual([], fork_inspected["next"])

            fork_resume_result = subprocess.run(
                [
                    sys.executable, *GRAPH_MODULE, "resume",
                    TARGET_WO, forked_thread_id, str(marker),
                    "--checkpoint-db", str(checkpoint_db),
                    "--idempotency-db", str(idempotency_db),
                ],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(0, fork_resume_result.returncode,
                             fork_resume_result.stderr)
            self.assertEqual(
                [f"load_envelope:{TARGET_WO}"],
                marker.read_text(encoding="utf-8").splitlines(),
            )
            self.assertEqual(before, _digest_work_studio())


class BackupRestoreCommandTests(unittest.TestCase):

    def test_backup_restore_inspect_and_resume_are_runtime_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            checkpoint_db = tmp / "source" / "tracer.sqlite"
            restored_db = tmp / "restored" / "tracer.sqlite"
            idempotency_db = tmp / "idempotency.sqlite"
            restored_idempotency_db = tmp / "restored-idempotency.sqlite"
            marker = tmp / "marker.txt"
            backup_dir = tmp / "backup"
            thread_id = "backup-restore-source"
            before = _digest_work_studio()

            run_result = subprocess.run(
                [
                    sys.executable, *GRAPH_MODULE, "run",
                    TARGET_WO, thread_id, str(marker),
                    "--checkpoint-db", str(checkpoint_db),
                    "--idempotency-db", str(idempotency_db),
                ],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(0, run_result.returncode, run_result.stderr)
            self.assertEqual(
                [f"load_envelope:{TARGET_WO}"],
                marker.read_text(encoding="utf-8").splitlines(),
            )

            backup_result = subprocess.run(
                [
                    sys.executable, *GRAPH_MODULE, "backup",
                    "--checkpoint-db", str(checkpoint_db),
                    "--backup-dir", str(backup_dir),
                ],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(0, backup_result.returncode, backup_result.stderr)
            backup = json.loads(backup_result.stdout)
            backup_path = Path(backup["backup_path"])
            self.assertEqual(str(checkpoint_db), backup["source_checkpoint_db"])
            self.assertEqual(backup_dir, backup_path.parent)
            self.assertNotEqual(checkpoint_db, backup_path)
            self.assertTrue(backup_path.exists())

            restore_result = subprocess.run(
                [
                    sys.executable, *GRAPH_MODULE, "restore",
                    "--backup", str(backup_path),
                    "--checkpoint-db", str(restored_db),
                ],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(0, restore_result.returncode, restore_result.stderr)
            restored = json.loads(restore_result.stdout)
            self.assertEqual(str(backup_path), restored["backup_path"])
            self.assertEqual(str(restored_db), restored["restored_checkpoint_db"])
            self.assertTrue(restored_db.exists())

            inspect_result = subprocess.run(
                [
                    sys.executable, *GRAPH_MODULE, "inspect", thread_id,
                    "--checkpoint-db", str(restored_db),
                ],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(0, inspect_result.returncode, inspect_result.stderr)
            inspected = json.loads(inspect_result.stdout)
            self.assertEqual("usable", inspected["recovery_status"])
            self.assertEqual(thread_id, inspected["thread_id"])
            self.assertEqual(thread_id, inspected["values"]["thread_id"])
            self.assertEqual([], inspected["next"])
            self.assertTrue(inspected["values"]["node1_completed"])
            self.assertTrue(inspected["values"]["node2_completed"])

            resume_result = subprocess.run(
                [
                    sys.executable, *GRAPH_MODULE, "resume",
                    TARGET_WO, thread_id, str(marker),
                    "--checkpoint-db", str(restored_db),
                    "--idempotency-db", str(restored_idempotency_db),
                ],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(0, resume_result.returncode, resume_result.stderr)
            resumed = json.loads(resume_result.stdout)
            self.assertTrue(resumed["node2_completed"])
            self.assertEqual(
                [f"load_envelope:{TARGET_WO}"],
                marker.read_text(encoding="utf-8").splitlines(),
            )
            self.assertEqual(before, _digest_work_studio())

    def test_backup_restore_fail_closed_on_missing_or_existing_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            backup_dir = tmp / "backup"
            missing_source = tmp / "missing.sqlite"
            existing_target = tmp / "target.sqlite"
            before = _digest_work_studio()

            missing_backup_result = subprocess.run(
                [
                    sys.executable, *GRAPH_MODULE, "backup",
                    "--checkpoint-db", str(missing_source),
                    "--backup-dir", str(backup_dir),
                ],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            self.assertNotEqual(0, missing_backup_result.returncode)
            self.assertIn("checkpoint DB not found", missing_backup_result.stderr)

            source_db = tmp / "source.sqlite"
            with sqlite3.connect(str(source_db)) as conn:
                conn.execute("CREATE TABLE sentinel (id INTEGER PRIMARY KEY)")
            successful_backup = subprocess.run(
                [
                    sys.executable, *GRAPH_MODULE, "backup",
                    "--checkpoint-db", str(source_db),
                    "--backup-dir", str(backup_dir),
                ],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(0, successful_backup.returncode, successful_backup.stderr)
            backup_path = Path(json.loads(successful_backup.stdout)["backup_path"])
            existing_target.write_bytes(b"existing target must not be overwritten")

            refused_restore = subprocess.run(
                [
                    sys.executable, *GRAPH_MODULE, "restore",
                    "--backup", str(backup_path),
                    "--checkpoint-db", str(existing_target),
                ],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            self.assertNotEqual(0, refused_restore.returncode)
            self.assertIn("restore target already exists", refused_restore.stderr)
            self.assertEqual(
                b"existing target must not be overwritten",
                existing_target.read_bytes(),
            )
            self.assertEqual(before, _digest_work_studio())


class SerializerSafetyTests(unittest.TestCase):

    def test_explicit_serializer_is_strict_and_normal_resume_still_works(self):
        serializer = build_checkpoint_serializer()
        self.assertFalse(serializer.pickle_fallback)
        self.assertIsNone(serializer._allowed_msgpack_modules)

        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            checkpoint_db = tmp / "tracer.sqlite"
            idempotency_db = tmp / "idempotency.sqlite"
            marker = tmp / "marker.txt"
            thread_id = "serializer-normal"
            before = _digest_work_studio()

            run_result = subprocess.run(
                [
                    sys.executable, *GRAPH_MODULE, "run",
                    TARGET_WO, thread_id, str(marker),
                    "--checkpoint-db", str(checkpoint_db),
                    "--idempotency-db", str(idempotency_db),
                ],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(0, run_result.returncode, run_result.stderr)

            inspect_result = subprocess.run(
                [
                    sys.executable, *GRAPH_MODULE, "inspect", thread_id,
                    "--checkpoint-db", str(checkpoint_db),
                ],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(0, inspect_result.returncode, inspect_result.stderr)
            inspected = json.loads(inspect_result.stdout)
            self.assertEqual("usable", inspected["recovery_status"])
            self.assertIsNone(inspected["error"])
            self.assertEqual(thread_id, inspected["values"]["thread_id"])

            resume_result = subprocess.run(
                [
                    sys.executable, *GRAPH_MODULE, "resume",
                    TARGET_WO, thread_id, str(marker),
                    "--checkpoint-db", str(checkpoint_db),
                    "--idempotency-db", str(idempotency_db),
                ],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(0, resume_result.returncode, resume_result.stderr)
            self.assertEqual(
                [f"load_envelope:{TARGET_WO}"],
                marker.read_text(encoding="utf-8").splitlines(),
            )
            self.assertEqual(before, _digest_work_studio())

    def test_tampered_checkpoint_payload_fails_closed_without_marker_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            checkpoint_db = tmp / "tracer.sqlite"
            idempotency_db = tmp / "idempotency.sqlite"
            marker = tmp / "marker.txt"
            thread_id = "serializer-tampered"
            before = _digest_work_studio()

            run_result = subprocess.run(
                [
                    sys.executable, *GRAPH_MODULE, "run",
                    TARGET_WO, thread_id, str(marker),
                    "--checkpoint-db", str(checkpoint_db),
                    "--idempotency-db", str(idempotency_db),
                ],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(0, run_result.returncode, run_result.stderr)
            self.assertEqual(
                [f"load_envelope:{TARGET_WO}"],
                marker.read_text(encoding="utf-8").splitlines(),
            )

            with sqlite3.connect(str(checkpoint_db)) as conn:
                updated = conn.execute(
                    """
                    UPDATE checkpoints
                    SET checkpoint = ?
                    WHERE thread_id = ?
                    """,
                    (b"not a valid checkpoint payload", thread_id),
                ).rowcount
            self.assertGreater(updated, 0)

            inspect_result = subprocess.run(
                [
                    sys.executable, *GRAPH_MODULE, "inspect", thread_id,
                    "--checkpoint-db", str(checkpoint_db),
                ],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            self.assertEqual(0, inspect_result.returncode, inspect_result.stderr)
            inspected = json.loads(inspect_result.stdout)
            self.assertEqual(
                "unusable_checkpoint_payload",
                inspected["recovery_status"],
            )
            self.assertEqual({}, inspected["values"])
            self.assertEqual([], inspected["next"])
            self.assertIsNotNone(inspected["error"])

            resume_result = subprocess.run(
                [
                    sys.executable, *GRAPH_MODULE, "resume",
                    TARGET_WO, thread_id, str(marker),
                    "--checkpoint-db", str(checkpoint_db),
                    "--idempotency-db", str(idempotency_db),
                ],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            self.assertNotEqual(0, resume_result.returncode)
            self.assertIn("checkpoint execution failed", resume_result.stderr)
            self.assertEqual(
                [f"load_envelope:{TARGET_WO}"],
                marker.read_text(encoding="utf-8").splitlines(),
            )
            self.assertEqual(before, _digest_work_studio())


if __name__ == "__main__":
    unittest.main()
