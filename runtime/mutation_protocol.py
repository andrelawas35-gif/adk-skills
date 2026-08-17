"""Transport-neutral mutation protocol tracer (WO 2026-08-15-004).

This module implements only the accepted tracer bullet: a versioned
`append_evidence` operation envelope, normalized result protocol, a CLI adapter
over `python3 -m tools.ws append-evidence`, and a no-write fake adapter for
conformance checks. It does not change `tools/ws` behavior and does not add a
second canonical writer.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from tools.ws import schema as _ws_schema
from tools.ws.sections import VALID_EVIDENCE_TAGS


EvidenceTag = Literal[tuple(sorted(VALID_EVIDENCE_TAGS))]
Sensitivity = Literal[tuple(sorted(_ws_schema.VALID_SENSITIVITIES))]

MutationStatus = Literal["applied", "replayed", "rejected", "adapter_error"]
MutationCode = Literal[
    "ok",
    "duplicate_intended_effect",
    "stale_updated_at",
    "invalid_tag",
    "missing_work_object",
    "adapter_failure",
]


class AppendEvidencePayload(BaseModel):
    """Payload for the one operation in this tracer."""

    model_config = ConfigDict(extra="forbid")

    tag: EvidenceTag
    source: str = Field(min_length=1)
    text: str = Field(min_length=1)
    sha: Optional[str] = None


class OperationEnvelope(BaseModel):
    """Versioned transport-neutral envelope for one append_evidence attempt."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1] = 1
    operation: Literal["append_evidence"]
    work_object_id: str = Field(min_length=1)
    baseline: str = Field(min_length=1)
    sensitivity: Sensitivity
    requested_effects: tuple[Literal["append_evidence"], ...]
    authority_refs: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()
    idempotency_key: str = Field(min_length=1)
    payload: AppendEvidencePayload

    @model_validator(mode="after")
    def _single_requested_effect(self) -> "OperationEnvelope":
        if self.requested_effects != ("append_evidence",):
            raise ValueError("requested_effects must be exactly ('append_evidence',)")
        return self


class MutationResult(BaseModel):
    """Normalized result from any adapter implementing the tracer protocol."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1] = 1
    operation: Literal["append_evidence"]
    work_object_id: str
    idempotency_key: str
    status: MutationStatus
    code: MutationCode
    adapter: str
    detail: str
    updated_at_before: Optional[str] = None
    updated_at_after: Optional[str] = None
    command: tuple[str, ...] = ()


def conformance_key(result: MutationResult) -> tuple[str, str, str, str]:
    """Return the stable fields adapters must agree on in conformance tests."""

    return (
        result.operation,
        result.work_object_id,
        result.status,
        result.code,
    )


def _frontmatter(text: str) -> dict:
    return _ws_schema.parse_frontmatter(text)


def _find_work_object(workspace_root: Path, work_object_id: str) -> Optional[Path]:
    objects_dir = workspace_root / ".work-studio" / "objects"
    if not objects_dir.is_dir():
        return None
    matches = sorted(objects_dir.glob(f"*/*/{work_object_id}-*.md"))
    if len(matches) != 1:
        return None
    return matches[0]


def _updated_at(path: Path) -> Optional[str]:
    try:
        return str(_frontmatter(path.read_text(encoding="utf-8")).get("updated_at", ""))
    except (OSError, ValueError):
        return None


def _effect_row(payload: AppendEvidencePayload) -> str:
    if payload.sha:
        return f"| {payload.tag} | {payload.source} | {payload.text} | {payload.sha} |"
    return f"| {payload.tag} | {payload.source} | {payload.text} |"


def _effect_already_present(path: Path, payload: AppendEvidencePayload) -> bool:
    try:
        return _effect_row(payload) in path.read_text(encoding="utf-8")
    except OSError:
        return False


class FakeAppendEvidenceAdapter:
    """No-write adapter for conformance fixtures."""

    adapter_name = "fake-no-write"

    def __init__(self, baselines: dict[str, str]):
        self._baselines = dict(baselines)
        self._applied_effects: set[tuple[str, str]] = set()

    def execute(self, envelope: OperationEnvelope) -> MutationResult:
        current = self._baselines.get(envelope.work_object_id)
        effect_key = (envelope.work_object_id, envelope.idempotency_key)

        if current is None:
            return self._result(envelope, "rejected", "missing_work_object", "target not found")
        if effect_key in self._applied_effects:
            return self._result(
                envelope,
                "replayed",
                "duplicate_intended_effect",
                "idempotency key already applied",
                current,
                current,
            )
        if current != envelope.baseline:
            return self._result(envelope, "rejected", "stale_updated_at", "baseline mismatch", current, current)

        self._applied_effects.add(effect_key)
        return self._result(envelope, "applied", "ok", "accepted by no-write adapter", current, current)

    def _result(
        self,
        envelope: OperationEnvelope,
        status: MutationStatus,
        code: MutationCode,
        detail: str,
        before: Optional[str] = None,
        after: Optional[str] = None,
    ) -> MutationResult:
        return MutationResult(
            operation=envelope.operation,
            work_object_id=envelope.work_object_id,
            idempotency_key=envelope.idempotency_key,
            status=status,
            code=code,
            adapter=self.adapter_name,
            detail=detail,
            updated_at_before=before,
            updated_at_after=after,
        )


class CliAppendEvidenceAdapter:
    """Adapter that writes only by invoking the existing `tools.ws` CLI."""

    adapter_name = "cli-tools-ws"

    def __init__(
        self,
        workspace_root: Path,
        module_root: Optional[Path] = None,
        python_executable: str = sys.executable,
    ):
        self.workspace_root = workspace_root
        self.module_root = module_root or Path(__file__).resolve().parents[1]
        self.python_executable = python_executable

    def execute(self, envelope: OperationEnvelope) -> MutationResult:
        target = _find_work_object(self.workspace_root, envelope.work_object_id)
        if target is None:
            return self._result(envelope, "rejected", "missing_work_object", "target not found")

        before = _updated_at(target)
        if _effect_already_present(target, envelope.payload):
            return self._result(
                envelope,
                "replayed",
                "duplicate_intended_effect",
                "intended evidence row already present",
                before,
                before,
            )
        if before != envelope.baseline:
            return self._result(envelope, "rejected", "stale_updated_at", "baseline mismatch", before, before)

        cmd = [
            self.python_executable,
            "-m",
            "tools.ws",
            "append-evidence",
            envelope.work_object_id,
            "--tag",
            envelope.payload.tag,
            "--source",
            envelope.payload.source,
            "--text",
            envelope.payload.text,
            "--expect-updated",
            envelope.baseline,
        ]
        if envelope.payload.sha:
            cmd.extend(["--sha", envelope.payload.sha])

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
            return self._result(
                envelope,
                "applied",
                "ok",
                "append_evidence applied through tools.ws",
                before,
                after,
                cmd,
            )

        stderr = proc.stderr.strip()
        return self._result(
            envelope,
            "rejected" if self._classify_error(stderr) != "adapter_failure" else "adapter_error",
            self._classify_error(stderr),
            stderr or proc.stdout.strip() or "adapter failed without output",
            before,
            after,
            cmd,
        )

    def _classify_error(self, stderr: str) -> MutationCode:
        if "Invalid evidence tag" in stderr:
            return "invalid_tag"
        if "Work Object not found" in stderr:
            return "missing_work_object"
        if "Concurrent write detected" in stderr:
            return "stale_updated_at"
        return "adapter_failure"

    def _result(
        self,
        envelope: OperationEnvelope,
        status: MutationStatus,
        code: MutationCode,
        detail: str,
        before: Optional[str] = None,
        after: Optional[str] = None,
        command: Optional[list[str]] = None,
    ) -> MutationResult:
        return MutationResult(
            operation=envelope.operation,
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
