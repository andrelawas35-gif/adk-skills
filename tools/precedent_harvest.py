#!/usr/bin/env python3
"""Scaffold Creative Precedent Ledger entries from closed Work Object Decisions.

WO 2026-08-23-001 (Decisions 6-8): the Component-Ledger-pattern precedent
ledger (.work-studio/precedent-ledger.md) is the storage for Recipe /
Revision / TastePrinciple records -- ws relation/ws graph cannot hold these
sub-Work-Object edges (Decision 6, verified against the CLI).

This tool is deliberately NOT a fully-automatic Recipe generator. The tracer
bullet (Decisions 7-8) proved that populating fields like `purpose`,
`applicable_when`, `avoid_when`, and correctly distinguishing "N/A -- this
recipe's mechanism has no prompt step" from "[gap] -- a prompt exists but
wasn't captured in Decision prose" requires judgment a script cannot safely
fake. Auto-generating those fields would silently reintroduce the exact
capture-at-generation risk the plan (section 5.5) and the report critique
(section 3.7) both warn about: retroactive, unreliable tagging.

What this tool DOES mechanically and reliably: extract the raw Decision
record (result, scope, authorization, confidence, rationale, revisit_trigger)
via the existing `parse_decisions_table` utility, and scaffold a Recipe entry
in the ledger with those raw fields filled in and the judgment-requiring
fields explicitly marked for a human or LLM to complete -- never silently
left blank, never guessed.

Usage:
    python3 tools/precedent_harvest.py <wo-id> <decision-number> [<recipe-id>]

Example:
    python3 tools/precedent_harvest.py 2026-08-23-007 16 R-003
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.ws.sections import parse_decisions_table  # noqa: E402

LEDGER_PATH = ROOT / ".work-studio" / "precedent-ledger.md"


def find_work_object_path(wo_id: str) -> Path:
    matches = list((ROOT / ".work-studio" / "objects").glob(f"*/*/{wo_id}-*.md"))
    if not matches:
        raise FileNotFoundError(f"No Work Object file found for id {wo_id!r} under .work-studio/objects/")
    if len(matches) > 1:
        raise RuntimeError(f"Ambiguous match for {wo_id!r}: {matches}")
    return matches[0]


def scaffold_entry(wo_id: str, decision_number: str, recipe_id: str) -> str:
    wo_path = find_work_object_path(wo_id)
    body = wo_path.read_text(encoding="utf-8")
    decisions = parse_decisions_table(body)

    record = next((d for d in decisions if d.get("number") == decision_number), None)
    if record is None:
        available = ", ".join(sorted(d.get("number", "?") for d in decisions))
        raise ValueError(f"Decision {decision_number} not found in {wo_id}. Available: {available}")

    result = record.get("result", "[gap: not recorded]")
    scope = record.get("scope", "[gap: not recorded]")
    authorization = record.get("authorization", "[gap: not recorded]")
    confidence = record.get("confidence", "[gap: not recorded]")
    rationale = record.get("rationale", "[gap: not recorded]")
    revisit_trigger = record.get("revisit_trigger", "[gap: not recorded]")
    summary = record.get("summary", "[gap: not recorded]")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    return f"""
## {recipe_id} — [NEEDS A SHORT KEBAB-CASE NAME]

<!-- Scaffolded by tools/precedent_harvest.py from {wo_id} Decision {decision_number}.
     Raw fields below are extracted mechanically and are reliable. The
     [NEEDS INTERPRETATION] fields require a human or LLM to read the source
     Decision and the WO's surrounding evidence and fill them in honestly --
     do not guess; mark [gap] or N/A explicitly per the tracer's own finding
     (WO 2026-08-23-001 Decisions 7-8) rather than leaving them blank. -->

- **status:** candidate
- **kind:** [NEEDS INTERPRETATION -- recipe (image revision) / recipe (3D asset generation) / other]
- **source_decision_summary:** {summary}
- **purpose:** [NEEDS INTERPRETATION]
- **applicable_when:** [NEEDS INTERPRETATION]
- **avoid_when:** [NEEDS INTERPRETATION]
- **inputs:** [NEEDS INTERPRETATION]
- **operations:** [NEEDS INTERPRETATION]
- **prompt_template:** [NEEDS INTERPRETATION -- mark N/A if this recipe's
  mechanism has no text-prompt step at all; mark [gap] if a prompt exists but
  isn't captured in the source Decision's own prose]
- **negative_constraints:** [NEEDS INTERPRETATION -- same N/A-vs-[gap] rule as prompt_template]
- **verification:** [NEEDS INTERPRETATION]
- **known_limits:** [NEEDS INTERPRETATION]
- **provenance:**
  - derived_from: `{wo_id}` Decision {decision_number} ({result})
  - raw scope: {scope}
  - raw authorization: {authorization}
  - raw confidence: {confidence}
  - raw revisit_trigger: {revisit_trigger}
  - raw rationale: {rationale}
- **scaffolded:** {today} (tools/precedent_harvest.py)
"""


def main() -> int:
    if len(sys.argv) not in (3, 4):
        print(__doc__)
        return 2

    wo_id, decision_number = sys.argv[1], sys.argv[2]
    recipe_id = sys.argv[3] if len(sys.argv) == 4 else "R-XXX"

    try:
        entry = scaffold_entry(wo_id, decision_number, recipe_id)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if not LEDGER_PATH.exists():
        print(f"error: {LEDGER_PATH} does not exist -- create it first", file=sys.stderr)
        return 1

    with LEDGER_PATH.open("a", encoding="utf-8") as f:
        f.write(entry)

    print(f"Scaffolded {recipe_id} from {wo_id} Decision {decision_number} into {LEDGER_PATH}")
    print("Fields marked [NEEDS INTERPRETATION] still require human/LLM completion before this entry is usable.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
