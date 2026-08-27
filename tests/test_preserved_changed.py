"""Focused regression tests for PRESERVED/CHANGED reporting (WO 2026-08-24-005).

Covers the accepted tracer-bullet design (Decision 2): a read-only report
derived from a Work Object's frontmatter + append-only History. Verifies the
honest preserved-vs-changed classification and the insufficient-History
failure mode. Also guards the '**Field:** value' (colon inside the bold)
History bullet format that generate_history_entry() writes — the same root
cause as the scene_board thesis fix (WO 2026-08-23-001).
"""

import sys
import tempfile
import unittest
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS_DIR))

from ws.preserved_changed import generate  # noqa: E402


HISTORY_FRONTMATTER = """---
schema_version: 1
id: 2099-02-02-001
title: Test Change Object
type: change
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
domain: [engineering]
created_at: 2099-02-02T00:00:00Z
updated_at: 2099-02-02T04:00:00Z
next_action: none
---"""

HISTORY_BODY = """
## Intent

Fixture for PRESERVED/CHANGED report tests.

## Decisions and revisit triggers

### Decision 1 — Sample decision

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | test |
| **Authorization** | user |
| **Confidence** | high |
| **Actor** | system |
| **Revisit trigger** | never |
| **Rationale** | testing |

## Evidence ledger

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | test | Evidence A |
| [system] | test | Evidence B |

## History

### 2099-02-02T00:00:00Z — Created

- **State:** notice
- **Status:** active
- **Actor:** system
- **Rationale:** Created.

### 2099-02-02T01:00:00Z — Transitioned to explore

- **State:** explore
- **Status:** active
- **Actor:** director
- **Rationale:** Explore.

### 2099-02-02T02:00:00Z — Transitioned to build

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Build.

### 2099-02-02T04:00:00Z — Aligned next_action

- **State:** verify
- **Status:** active
- **Actor:** system
- **Rationale:** next move synced.
"""

EMPTY_HISTORY_FRONTMATTER = """---
schema_version: 1
id: 2099-02-02-002
title: Empty History Object
type: change
status: active
state: notice
consequence: low
sensitivity: ordinary
domain: [engineering]
created_at: 2099-02-02T00:00:00Z
updated_at: 2099-02-02T00:00:00Z
next_action: none
---"""

EMPTY_HISTORY_BODY = """
## Intent

Fixture with no History entries.

## Evidence ledger

| Tag | Source | Entry |
|-----|--------|-------|

## Next move

None.
"""


def _write_wo(ws_root: Path, filename: str, frontmatter: str, body: str) -> Path:
    objects_dir = ws_root / ".work-studio" / "objects" / "2099" / "02"
    objects_dir.mkdir(parents=True, exist_ok=True)
    path = objects_dir / filename
    path.write_text(frontmatter + "\n" + body, encoding="utf-8")
    return path


class TestPreservedChanged(unittest.TestCase):
    def test_classifies_preserved_and_changed_from_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_wo(
                Path(tmp), "2099-02-02-001-test-change.md",
                HISTORY_FRONTMATTER, HISTORY_BODY,
            )
            result = generate(path)
            text = result["out_text"]
            self.assertEqual(result["id"], "2099-02-02-001")
            self.assertIn("PRESERVED (no recorded change", text)
            # identity/classification fields are reported preserved
            for field in ("id", "type", "consequence", "sensitivity", "domain"):
                self.assertIn(field, text)
            # changed state trajectory is ordered and complete
            self.assertIn("State: notice -> explore -> build -> verify", text)
            # counts derived from the record
            self.assertIn("Decisions recorded: 1", text)
            self.assertIn("Evidence entries: 2", text)
            self.assertIn("History entries: 4", text)
            self.assertIn(
                "Next-action/next-move updates (from History action wording): 1",
                text,
            )

    def test_insufficient_history_is_reported_not_fabricated(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_wo(
                Path(tmp), "2099-02-02-002-empty-history.md",
                EMPTY_HISTORY_FRONTMATTER, EMPTY_HISTORY_BODY,
            )
            result = generate(path)
            self.assertIn("Insufficient History to classify", result["out_text"])
            self.assertNotIn("PRESERVED (no recorded change", result["out_text"])


if __name__ == "__main__":
    unittest.main()
