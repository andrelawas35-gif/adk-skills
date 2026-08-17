#!/usr/bin/env python3
"""Tracer-bullet tests for the append_history typed canonical adapter.

Covers WO 2026-08-16-001 Decision 2's four exit criteria: applied, replayed
(idempotent), rejected (stale baseline fails closed), and single-writer (no
other node touches the CLI).
"""

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from pydantic import ValidationError

from runtime.persistence import (
    CliAppendHistoryAdapter,
    HistoryReceiptEnvelope,
    HistoryReceiptPayload,
)


WO_ID = "2026-08-16-999"
BASELINE = "2026-08-16T00:00:00Z"


def _envelope(
    *,
    work_object_id: str = WO_ID,
    baseline: str = BASELINE,
    key: str = "history-receipt-demo-1",
) -> HistoryReceiptEnvelope:
    return HistoryReceiptEnvelope(
        work_object_id=work_object_id,
        baseline=baseline,
        idempotency_key=key,
        payload=HistoryReceiptPayload(
            action="Tracer-bullet receipt",
            state="build",
            status="active",
            actor="system",
            rationale="Phase 4 append_history tracer bullet fixture receipt",
        ),
    )


def _workspace() -> tempfile.TemporaryDirectory:
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    obj_dir = root / ".work-studio" / "objects" / "2026" / "08"
    obj_dir.mkdir(parents=True)
    (obj_dir / f"{WO_ID}-persistence-fixture.md").write_text(
        "\n".join(
            [
                "---",
                "schema_version: 1",
                f"id: {WO_ID}",
                "title: Persistence fixture",
                "type: inquiry",
                "status: active",
                "state: build",
                "consequence: low",
                "sensitivity: ordinary",
                "created_at: 2026-08-16T00:00:00Z",
                f"updated_at: {BASELINE}",
                "next_action: fixture",
                "---",
                "",
                "## Intent",
                "",
                "Fixture.",
                "",
                "## History",
                "",
                "### 2026-08-16T00:00:00Z — Fixture created",
                "",
                "- **State:** build",
                "- **Status:** active",
                "- **Actor:** system",
                "- **Rationale:** fixture",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return tmp


class HistoryReceiptEnvelopeTests(unittest.TestCase):
    def test_envelope_is_strict_and_single_operation(self) -> None:
        env = _envelope()
        self.assertEqual(env.operation, "append_history")
        with self.assertRaises(ValidationError):
            HistoryReceiptEnvelope(**dict(env.model_dump(), extra_field="nope"))


class AdapterExitCriteriaTests(unittest.TestCase):
    """Exit criteria 1-3 from Decision 2's bounded path."""

    def test_first_run_is_applied(self) -> None:
        env = _envelope()
        with _workspace() as tmp:
            root = Path(tmp)
            adapter = CliAppendHistoryAdapter(root, idempotency_db=root / "idempotency.sqlite")
            result = adapter.execute(env)
            self.assertEqual(("applied", "ok"), (result.status, result.code))
            wo_text = (root / ".work-studio" / "objects" / "2026" / "08" / f"{WO_ID}-persistence-fixture.md").read_text()
            self.assertIn("Tracer-bullet receipt", wo_text)

    def test_repeat_run_same_key_is_replayed_without_second_write(self) -> None:
        env = _envelope()
        with _workspace() as tmp:
            root = Path(tmp)
            adapter = CliAppendHistoryAdapter(root, idempotency_db=root / "idempotency.sqlite")
            first = adapter.execute(env)
            second = adapter.execute(env)

            self.assertEqual(("applied", "ok"), (first.status, first.code))
            self.assertEqual(("replayed", "duplicate_intended_effect"), (second.status, second.code))

            wo_text = (root / ".work-studio" / "objects" / "2026" / "08" / f"{WO_ID}-persistence-fixture.md").read_text()
            self.assertEqual(1, wo_text.count("Tracer-bullet receipt"))

    def test_stale_baseline_is_rejected_and_file_untouched(self) -> None:
        env = _envelope(baseline="1999-01-01T00:00:00Z")
        with _workspace() as tmp:
            root = Path(tmp)
            wo_path = root / ".work-studio" / "objects" / "2026" / "08" / f"{WO_ID}-persistence-fixture.md"
            before_text = wo_path.read_text()

            adapter = CliAppendHistoryAdapter(root, idempotency_db=root / "idempotency.sqlite")
            result = adapter.execute(env)

            self.assertEqual(("rejected", "stale_updated_at"), (result.status, result.code))
            self.assertEqual(before_text, wo_path.read_text())

    def test_failed_cli_call_leaves_no_idempotency_record_and_stays_retryable(self) -> None:
        """A crashed/failed attempt must not be silently remembered as applied."""
        env = _envelope()
        with _workspace() as tmp:
            root = Path(tmp)
            adapter = CliAppendHistoryAdapter(root, idempotency_db=root / "idempotency.sqlite")

            failed = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="boom")
            with mock.patch("runtime.persistence.subprocess.run", return_value=failed):
                first = adapter.execute(env)
            self.assertEqual("adapter_error", first.status)

            second = adapter.execute(env)
            self.assertEqual(("applied", "ok"), (second.status, second.code))


class SingleWriterTests(unittest.TestCase):
    """Exit criterion 4: no node other than the adapter touches the CLI."""

    def test_only_the_adapter_invokes_the_ws_subprocess(self) -> None:
        env = _envelope()
        with _workspace() as tmp:
            root = Path(tmp)
            adapter = CliAppendHistoryAdapter(root, idempotency_db=root / "idempotency.sqlite")

            calls = []
            real_run = subprocess.run

            def _tracking_run(cmd, *args, **kwargs):
                calls.append(cmd)
                return real_run(cmd, *args, **kwargs)

            with mock.patch("runtime.persistence.subprocess.run", side_effect=_tracking_run):
                # Simulate a second, non-persistence "reader" node that only
                # inspects state -- it must never reach for the CLI.
                from runtime.mutation_protocol import _find_work_object, _updated_at

                target = _find_work_object(root, WO_ID)
                _ = _updated_at(target)

                adapter.execute(env)

            self.assertEqual(1, len(calls))
            self.assertIn("tools.ws", " ".join(calls[0]))


if __name__ == "__main__":
    unittest.main()
