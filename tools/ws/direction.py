"""Direction object parser (V0 tracer, WO 2026-08-23-001).

Parses natural-language director input into a structured Direction object:
  basis, protect, change, desired_effect, avoid, mode (inquiry/direction/command).

V0 uses simple keyword extraction — no LLM required. The structured Direction
is recorded as [testimony] evidence on the target Scene Work Object via the
ws CLI.
"""
import re


def parse_direction(text: str) -> dict:
    """Parse director prose into a structured Direction object.

    Returns a dict with: raw, mode, basis, protect, change, desired_effect, avoid.
    """
    lower = text.lower().strip()

    # Detect mode
    if lower.startswith("why ") or lower.endswith("?") and not any(
        w in lower for w in ["make", "keep", "change", "remove", "add"]
    ):
        mode = "inquiry"
    elif any(lower.startswith(w) for w in [
        "keep ", "remove ", "delete ", "rename ", "set ", "cut ", "add "
    ]):
        mode = "command"
    else:
        mode = "direction"

    result = {
        "raw": text.strip(),
        "mode": mode,
        "basis": [],
        "protect": [],
        "change": [],
        "desired_effect": [],
        "avoid": [],
    }

    # Extract explicit markers if present
    # Pattern: "Keep X" / "Keep the X" / "Keep X and Y"
    for m in re.finditer(
        r"[Kk]eep\s+(?:the\s+)?(.+?)(?:\.|,|$| but )", text
    ):
        phrase = m.group(1).strip()
        for part in re.split(r"\s+and\s+", phrase):
            p = re.sub(r"^the\s+", "", part.strip())
            if p:
                result["protect"].append(p)

    # Pattern: "Don't change X" / "without changing X"
    for m in re.finditer(
        r"(?:[Dd]on'?t\s+(?:change|touch|modify|alter)\s+|[Ww]ithout\s+changing\s+)(.+?)(?:\.|,|$| and | but )",
        text,
    ):
        result["protect"].append(m.group(1).strip())

    # Pattern: "Make X feel/seem/look Y"
    for m in re.finditer(
        r"[Mm]ake\s+(?:this|it|the\s+\w+)\s+(?:feel|seem|look)\s+(.+?)(?:\.|,|$| and | but )",
        text,
    ):
        result["desired_effect"].append(m.group(1).strip())

    # Pattern: "less X" / "more X"
    for m in re.finditer(r"(?:less|more)\s+(\w+(?:\s+\w+)?)", text):
        result["change"].append(m.group(0).strip())

    # Pattern: "no X" / "avoid X" / "don't X"
    for m in re.finditer(
        r"(?:[Aa]void\s+|[Nn]o\s+)(.+?)(?:\.|,|$| and | but )", text
    ):
        result["avoid"].append(m.group(1).strip())

    # Pattern: "B is closer" / "Keep B" / "variant B"
    for m in re.finditer(
        r"(?:^|\s)([A-C])\s+(?:is\s+closer|is\s+better|works)", text
    ):
        result["basis"].append(f"Variant {m.group(1)}")

    # Dedup
    for key in ["basis", "protect", "change", "desired_effect", "avoid"]:
        result[key] = list(dict.fromkeys(result[key]))

    return result


def format_direction(d: dict) -> str:
    """Format a structured Direction as readable text for evidence recording."""
    lines = [f"Direction ({d['mode']}): {d['raw']}"]
    if d["basis"]:
        lines.append(f"  Basis: {', '.join(d['basis'])}")
    if d["protect"]:
        lines.append(f"  Protect: {', '.join(d['protect'])}")
    if d["change"]:
        lines.append(f"  Change: {', '.join(d['change'])}")
    if d["desired_effect"]:
        lines.append(f"  Desired effect: {', '.join(d['desired_effect'])}")
    if d["avoid"]:
        lines.append(f"  Avoid: {', '.join(d['avoid'])}")
    return "\n".join(lines)


def format_direction_yaml(d: dict) -> str:
    """Format as YAML-style block for embedding in Work Object evidence."""
    lines = [f"mode: {d['mode']}"]
    if d["basis"]:
        lines.append(f"basis: [{', '.join(d['basis'])}]")
    if d["protect"]:
        lines.append(f"protect: [{', '.join(d['protect'])}]")
    if d["change"]:
        lines.append(f"change: [{', '.join(d['change'])}]")
    if d["desired_effect"]:
        lines.append(f"desired_effect: [{', '.join(d['desired_effect'])}]")
    if d["avoid"]:
        lines.append(f"avoid: [{', '.join(d['avoid'])}]")
    return "\n".join(lines)


def format_direction_single_line(d: dict) -> str:
    """Format a structured Direction as a single physical line for a table cell.

    Reuses ``format_direction`` but joins its lines with ``<br>`` so the
    persisted Evidence ledger row stays one valid markdown table row instead of
    leaking the structured-field lines outside the table (Incident WO
    2026-08-23-005). The multi-line form is still used for console display.
    """
    return "<br>".join(format_direction(d).split("\n"))
