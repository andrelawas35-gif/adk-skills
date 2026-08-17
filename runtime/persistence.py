"""Typed canonical adapter for the append_history operation (WO 2026-08-16-001).

Implements the accepted Phase 4 tracer bullet (Decision 2): a single
append_history operation flowing through one typed adapter that revalidates
the Work Object's baseline immediately before writing and never bypasses
`python3 -m tools.ws` (ADR 0025 single-writer rule). Idempotency is keyed in a
sqlite ledger recorded only after a confirmed successful write -- a failed
attempt stays retryable rather than being silently remembered as done.

Mirrors runtime/mutation_protocol.py's envelope/result shape for
append_evidence, extended for append_history's own fields. Not a modification
of that module: append_history's fields (state/status/actor/rationale) and
verbatim-timestamped History entries differ enough that a shared Literal
operation type would weaken both. The idempotency ledger uses a dedicated
sqlite file, following the pattern already proven in
runtime/graph.py::claim_idempotency_receipt -- a sibling table inside the
LangGraph checkpoint DB was considered and rejected: `SqliteSaver` owns
exactly two tables (`checkpoints`, `writes`) in that file, and a separate file
avoids any question of interference with LangGraph's own schema.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from runtime.mutation_protocol import _find_work_object, _updated_at


HistoryMutationStatus = Literal["applied", "replayed", "rejected", "adapter_error"]
HistoryMutationCode = Literal[
    "ok",
    "duplicate_intended_effect",
    "stale_updated_at",
    "missing_work_object",
    "adapter_failure",
]


class HistoryReceiptPayload(BaseModel):
    """The append_history fields carried by one receipt."""

    model_config = ConfigDict(extra="forbid")

    action: str = Field(min_length=1)
    state: str = Field(min_length=1)
    status: str = Field(min_length=1)
    actor: str = Field(min_length=1)
    rationale: str = Field(min_length=1)


class HistoryReceiptEnvelope(BaseModel):
    """Versioned transport-neutral envelope for one append_history attempt."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1] = 1
    operation: Literal["append_history"] = "append_history"
    work_object_id: str = Field(min_length=1)
    baseline: str = Field(min_length=1)
    idempotency_key: str = Field(min_length=1)
    payload: HistoryReceiptPayload


class HistoryMutationResult(BaseModel):
    """Normalized result from the append_history adapter."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1] = 1
    operation: Literal["append_history"] = "append_history"
    work_object_id: str
    idempotency_key: str
    status: HistoryMutationStatus
    code: HistoryMutationCode
    adapter: str
    detail: str
    updated_at_before: Optional[str] = None
    updated_at_after: Optional[str] = None
    command: tuple[str, ...] = ()


def _idempotency_already_applied(
    idempotency_db: Path, work_object_id: str, idempotency_key: str
) -> bool:
    import sqlite3

    idempotency_db.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(idempotency_db)) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS history_receipts (
                work_object_id TEXT NOT NULL,
                idempotency_key TEXT NOT NULL,
                applied_at REAL NOT NULL,
                PRIMARY KEY (work_object_id, idempotency_key)
            )
            """
        )
        row = conn.execute(
            "SELECT 1 FROM history_receipts WHERE work_object_id = ? AND idempotency_key = ?",
            (work_object_id, idempotency_key),
        ).fetchone()
        return row is not None


def _record_applied(
    idempotency_db: Path, work_object_id: str, idempotency_key: str
) -> None:
    import sqlite3

    with sqlite3.connect(str(idempotency_db)) as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO history_receipts
                (work_object_id, idempotency_key, applied_at)
            VALUES (?, ?, ?)
            """,
            (work_object_id, idempotency_key, time.time()),
        )


class CliAppendHistoryAdapter:
    """Adapter that writes only by invoking the existing `tools.ws` CLI.

    Idempotency is recorded ONLY after the CLI call returns success (exit 0),
    never before: a failed or crashed attempt leaves no ledger row, so a retry
    with the same idempotency_key still attempts the write rather than being
    reported as already-applied against a write that never happened.
    """

    adapter_name = "cli-tools-ws"

    def __init__(
        self,
        workspace_root: Path,
        idempotency_db: Path,
        module_root: Optional[Path] = None,
        python_executable: str = sys.executable,
    ):
        self.workspace_root = workspace_root
        self.idempotency_db = idempotency_db
        self.module_root = module_root or Path(__file__).resolve().parents[1]
        self.python_executable = python_executable

    def execute(self, envelope: HistoryReceiptEnvelope) -> HistoryMutationResult:
        target = _find_work_object(self.workspace_root, envelope.work_object_id)
        if target is None:
            return self._result(envelope, "rejected", "missing_work_object", "target not found")

        if _idempotency_already_applied(
            self.idempotency_db, envelope.work_object_id, envelope.idempotency_key
        ):
            before = _updated_at(target)
            return self._result(
                envelope,
                "replayed",
                "duplicate_intended_effect",
                "idempotency key already applied",
                before,
                before,
            )

        before = _updated_at(target)
        if before != envelope.baseline:
            return self._result(envelope, "rejected", "stale_updated_at", "baseline mismatch", before, before)

        cmd = [
            self.python_executable,
            "-m",
            "tools.ws",
            "append-history",
            envelope.work_object_id,
            "--action",
            envelope.payload.action,
            "--state",
            envelope.payload.state,
            "--status",
            envelope.payload.status,
            "--actor",
            envelope.payload.actor,
            "--rationale",
            envelope.payload.rationale,
            "--expect-updated",
            envelope.baseline,
        ]

        env = dict(os.environ)
        module_path = str(self.module_root)
        existing = env.get("PYTHONPATH")
        env["PYTHONPATH"] = module_path if not existing else f"{module_path}{os.pathsep}{existing}"

        proc = subprocess.run(
            cmd,
            cwd=self.workspace_root,
            env=env,
            capture_output=True,
            text=True,
        )

        after = _updated_at(target)
        if proc.returncode == 0:
            _record_applied(self.idempotency_db, envelope.work_object_id, envelope.idempotency_key)
            return self._result(
                envelope,
                "applied",
                "ok",
                "append_history applied through tools.ws",
                before,
                after,
                cmd,
            )

        stderr = proc.stderr.strip()
        code = self._classify_error(stderr)
        status = "rejected" if code != "adapter_failure" else "adapter_error"
        return self._result(
            envelope,
            status,
            code,
            stderr or proc.stdout.strip() or "adapter failed without output",
            before,
            after,
            cmd,
        )

    def _classify_error(self, stderr: str) -> HistoryMutationCode:
        if "Work Object not found" in stderr:
            return "missing_work_object"
        if "Concurrent write detected" in stderr:
            return "stale_updated_at"
        return "adapter_failure"

    def _result(
        self,
        envelope: HistoryReceiptEnvelope,
        status: HistoryMutationStatus,
        code: HistoryMutationCode,
        detail: str,
        before: Optional[str] = None,
        after: Optional[str] = None,
        command: Optional[list[str]] = None,
    ) -> HistoryMutationResult:
        return HistoryMutationResult(
            work_object_id=envelope.work_object_id,
            idempotency_key=envelope.idempotency_key,
            status=status,
            code=code,
            adapter=self.adapter_name,
            detail=detail,
            updated_at_before=before,
            updated_at_after=after,
            command=tuple(command or ()),
        )
