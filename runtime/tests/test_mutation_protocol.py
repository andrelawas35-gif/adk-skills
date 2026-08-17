#!/usr/bin/env python3
"""Conformance tests for the append_evidence mutation protocol tracer."""

import tempfile
import unittest
from pathlib import Path

from pydantic import ValidationError

from runtime.mutation_protocol import (
    AppendEvidencePayload,
    CliAppendEvidenceAdapter,
    FakeAppendEvidenceAdapter,
    MutationResult,
    OperationEnvelope,
    conformance_key,
)


ROOT = Path(__file__).resolve().parents[2]
WO_ID = "2026-08-15-999"
BASELINE = "2026-08-15T00:00:00Z"


def _envelope(
    *,
    work_object_id: str = WO_ID,
    baseline: str = BASELINE,
    key: str = "append-evidence-demo-1",
    tag: str = "[system]",
    source: str = "runtime conformance fixture",
    text: str = "append_evidence protocol fixture",
) -> OperationEnvelope:
    return OperationEnvelope(
        operation="append_evidence",
        work_object_id=work_object_id,
        baseline=baseline,
        sensitivity="ordinary",
        requested_effects=("append_evidence",),
        authority_refs=("Decision 2",),
        constraints=("python3 -m tools.ws remains the only canonical writer",),
        idempotency_key=key,
        payload=AppendEvidencePayload(tag=tag, source=source, text=text),
    )


def _workspace() -> tempfile.TemporaryDirectory:
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    obj_dir = root / ".work-studio" / "objects" / "2026" / "08"
    obj_dir.mkdir(parents=True)
    (obj_dir / f"{WO_ID}-protocol-fixture.md").write_text(
        "\n".join(
            [
                "---",
                "schema_version: 1",
                f"id: {WO_ID}",
                "title: Protocol fixture",
                "type: inquiry",
                "status: active",
                "state: build",
                "consequence: low",
                "sensitivity: ordinary",
                "created_at: 2026-08-15T00:00:00Z",
                f"updated_at: {BASELINE}",
                "next_action: fixture",
                "---",
                "",
                "## Intent",
                "",
                "Fixture.",
                "",
                "## Evidence ledger",
                "",
                "| Tag | Source | Entry |",
                "|-----|--------|-------|",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return tmp


class OperationEnvelopeTests(unittest.TestCase):
    def test_operation_envelope_is_strict_and_single_operation(self) -> None:
        env = _envelope()
        self.assertEqual(env.operation, "append_evidence")

        with self.assertRaises(ValidationError):
            OperationEnvelope(**dict(env.model_dump(), extra_field="nope"))

        data = env.model_dump()
        data["requested_effects"] = ("append_evidence", "transition")
        with self.assertRaises(ValidationError):
            OperationEnvelope(**data)

    def test_result_protocol_can_represent_required_failure_codes(self) -> None:
        for code in (
            "ok",
            "stale_updated_at",
            "invalid_tag",
            "missing_work_object",
            "duplicate_intended_effect",
            "adapter_failure",
        ):
            with self.subTest(code=code):
                status = "applied" if code == "ok" else "replayed" if code == "duplicate_intended_effect" else "rejected"
                result = MutationResult(
                    operation="append_evidence",
                    work_object_id=WO_ID,
                    idempotency_key="k",
                    status=status,
                    code=code,
                    adapter="fixture",
                    detail="fixture",
                )
                self.assertEqual(result.code, code)


class AdapterConformanceTests(unittest.TestCase):
    def test_cli_and_fake_adapter_agree_on_success_category(self) -> None:
        env = _envelope()
        fake = FakeAppendEvidenceAdapter({WO_ID: BASELINE})
        with _workspace() as tmp:
            cli = CliAppendEvidenceAdapter(Path(tmp), module_root=ROOT)
            self.assertEqual(conformance_key(fake.execute(env)), conformance_key(cli.execute(env)))

    def test_cli_and_fake_adapter_agree_on_stale_baseline(self) -> None:
        env = _envelope(baseline="1999-01-01T00:00:00Z")
        fake = FakeAppendEvidenceAdapter({WO_ID: BASELINE})
        with _workspace() as tmp:
            cli = CliAppendEvidenceAdapter(Path(tmp), module_root=ROOT)
            self.assertEqual(conformance_key(fake.execute(env)), conformance_key(cli.execute(env)))

    def test_cli_and_fake_adapter_agree_on_missing_object(self) -> None:
        env = _envelope(work_object_id="2026-08-15-998")
        fake = FakeAppendEvidenceAdapter({WO_ID: BASELINE})
        with _workspace() as tmp:
            cli = CliAppendEvidenceAdapter(Path(tmp), module_root=ROOT)
            self.assertEqual(conformance_key(fake.execute(env)), conformance_key(cli.execute(env)))

    def test_cli_adapter_replays_duplicate_intended_effect_without_second_write(self) -> None:
        env = _envelope()
        with _workspace() as tmp:
            cli = CliAppendEvidenceAdapter(Path(tmp), module_root=ROOT)
            first = cli.execute(env)
            second = cli.execute(env)

        self.assertEqual(("applied", "ok"), (first.status, first.code))
        self.assertEqual(("replayed", "duplicate_intended_effect"), (second.status, second.code))

    def test_cli_adapter_can_classify_invalid_tag_from_cli(self) -> None:
        # Bypass Pydantic validation to prove the result protocol and adapter can
        # normalize the underlying CLI failure if invalid transport input leaks in.
        payload = AppendEvidencePayload.model_construct(
            tag="[bad]", source="runtime conformance fixture", text="bad tag"
        )
        env = OperationEnvelope.model_construct(
            operation="append_evidence",
            work_object_id=WO_ID,
            baseline=BASELINE,
            sensitivity="ordinary",
            requested_effects=("append_evidence",),
            authority_refs=("Decision 2",),
            constraints=(),
            idempotency_key="bad-tag",
            payload=payload,
        )
        with _workspace() as tmp:
            result = CliAppendEvidenceAdapter(Path(tmp), module_root=ROOT).execute(env)

        self.assertEqual(("rejected", "invalid_tag"), (result.status, result.code))


if __name__ == "__main__":
    unittest.main()
