#!/usr/bin/env python3
"""Regression tests for the committed runtime envelope (WO 2026-08-15-006).

Covers the accepted boundary (Decision 1): strict Pydantic envelope with
`extra="forbid"` in the Python 3.11 runtime contract layer, enums sourced from
`tools/ws/schema.py`, the 5 declared corpus fields, and committed JSON Schema
snapshot diff-testing.

Run under the runtime's isolated environment (Python 3.11 + Pydantic, managed
by uv; nothing committed beyond pyproject.toml/uv.lock):

    uv run python -m unittest discover -s runtime/tests -v

These tests live under runtime/tests/ (not tests/) so the system-Python CLI
suite (`python3 -m unittest discover -s tests`) never imports Pydantic and
stays dependency-free, preserving the dual-runtime boundary.
"""

import json
import unittest
from pathlib import Path

from pydantic import ValidationError

from runtime.envelope import WorkObjectEnvelope, envelope_json_schema

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT_PATH = ROOT / "runtime" / "schema_snapshots" / "work_object_envelope.schema.json"

# A minimal valid frontmatter dict shared by several tests.
VALID_FRONTMATTER = {
    "schema_version": 1,
    "id": "2026-08-15-006",
    "title": "Test object",
    "type": "change",
    "status": "active",
    "state": "design",
    "consequence": "meaningful",
    "sensitivity": "ordinary",
    "created_at": "2026-08-14T17:39:50Z",
    "updated_at": "2026-08-14T17:39:50Z",
}


def _all_work_objects() -> list[tuple[Path, dict]]:
    """Return (path, frontmatter dict) for every .md under .work-studio/objects.

    A workable, dependency-free YAML-subset parser for the flat frontmatter
    blocks this studio writes. Returns only files whose first line is `---`.
    """
    out = []
    for p in sorted(ROOT.glob(".work-studio/objects/*/*/*.md")):
        text = p.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        lines = text.splitlines()
        fields: dict = {}
        for line in lines[1:]:
            if line.strip() == "---":
                break
            if not line.strip() or line.startswith((" ", "\t")):
                continue
            if ":" not in line:
                continue
            key, _, raw = line.partition(":")
            value = raw.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
                value = value[1:-1]
            fields[key.strip()] = value
        out.append((p, fields))
    return out


class EnvelopeRoundTripTests(unittest.TestCase):
    """Every live Work Object must round-trip the strict envelope cleanly."""

    def test_all_live_work_objects_round_trip(self) -> None:
        items = _all_work_objects()
        self.assertGreaterEqual(len(items), 130, "expected the live corpus to be present")
        failures = []
        for path, fm in items:
            try:
                WorkObjectEnvelope(**fm)
            except ValidationError as exc:
                failures.append(f"{path.name}: {exc.errors()}")
        self.assertEqual([], failures, "live corpus objects must all round-trip")


class StrictRejectionTests(unittest.TestCase):
    """extra='forbid' must reject unknown fields and invalid values."""

    def test_unknown_field_rejected(self) -> None:
        bad = dict(VALID_FRONTMATTER, unknown_field="surprise")
        with self.assertRaises(ValidationError):
            WorkObjectEnvelope(**bad)

    def test_extra_field_rejected_even_when_declared_corpus_field_present(self) -> None:
        # The 5 corpus fields are now declared; a SIXTH unknown one must fail.
        good = dict(VALID_FRONTMATTER, revisit_trigger="When X; then Y.")
        env = WorkObjectEnvelope(**good)
        self.assertEqual(env.revisit_trigger, "When X; then Y.")
        bad = dict(good, still_unknown="nope")
        with self.assertRaises(ValidationError):
            WorkObjectEnvelope(**bad)

    def test_invalid_enum_rejected(self) -> None:
        bad = dict(VALID_FRONTMATTER, type="not-a-type")
        with self.assertRaises(ValidationError):
            WorkObjectEnvelope(**bad)

    def test_invalid_datetime_rejected(self) -> None:
        bad = dict(VALID_FRONTMATTER, created_at="not-a-date")
        with self.assertRaises(ValidationError):
            WorkObjectEnvelope(**bad)

    def test_non_integer_schema_version_rejected(self) -> None:
        bad = dict(VALID_FRONTMATTER, schema_version="one")
        with self.assertRaises(ValidationError):
            WorkObjectEnvelope(**bad)

    def test_declared_corpus_fields_are_accepted(self) -> None:
        for field in ("revisit_trigger", "responds_to", "supersedes", "superseded_by", "unblocks"):
            with self.subTest(field=field):
                env = WorkObjectEnvelope(**dict(VALID_FRONTMATTER, **{field: "2026-07-22-001"}))
                self.assertEqual(getattr(env, field), "2026-07-22-001")


class EnumSyncTests(unittest.TestCase):
    """The envelope's enums must equal tools/ws/schema.py's VALID_* sets."""

    def test_enums_match_schema_module(self) -> None:
        from tools.ws import schema as ws_schema

        env_schema = envelope_json_schema()
        props = env_schema["properties"]

        def allowed(field: str) -> set:
            return set(props[field].get("enum", []))

        self.assertEqual(allowed("type"), set(ws_schema.VALID_TYPES))
        self.assertEqual(allowed("status"), set(ws_schema.VALID_STATUSES))
        self.assertEqual(allowed("state"), set(ws_schema.VALID_STATES))
        self.assertEqual(allowed("consequence"), set(ws_schema.VALID_CONSEQUENCES))
        self.assertEqual(allowed("sensitivity"), set(ws_schema.VALID_SENSITIVITIES))


class JsonSchemaSnapshotTests(unittest.TestCase):
    """The committed JSON Schema snapshot must match the generated schema."""

    def test_snapshot_matches_generated_schema(self) -> None:
        self.assertTrue(SNAPSHOT_PATH.is_file(), "committed snapshot must exist")
        committed = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
        generated = envelope_json_schema()
        self.assertEqual(committed, generated)

    def test_snapshot_forbids_extra_properties(self) -> None:
        committed = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
        self.assertFalse(committed.get("additionalProperties", True))


if __name__ == "__main__":
    unittest.main()
