#!/usr/bin/env python3
"""Build and measure an isolated, scenario-aware skill prompt package.

This tracer is deliberately independent of the platform adapter generator. It
compiles only the declared transitive closure for one Work Studio skill and
records enough evidence to compare it with the current generated adapter.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path


class TraceError(ValueError):
    """Raised when a manifest or scenario violates the tracer contract."""


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_spec(root: Path) -> tuple[dict, dict]:
    manifest = read_json(root / "tools" / "prompt-tracer-manifest.json")
    scenarios = read_json(root / "fixtures" / "prompt-payload-scenarios.json")
    return manifest, scenarios


def closure(manifest: dict, entry: str) -> list[str]:
    nodes = manifest["nodes"]
    if entry not in nodes:
        raise TraceError(f"unknown entry node: {entry}")
    ordered: list[str] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(name: str) -> None:
        if name in visiting:
            raise TraceError(f"dependency cycle at {name}")
        if name in visited:
            return
        if name not in nodes:
            raise TraceError(f"unknown dependency node: {name}")
        visiting.add(name)
        for dependency in nodes[name].get("requires", []):
            visit(dependency)
        visiting.remove(name)
        visited.add(name)
        ordered.append(name)

    visit(entry)
    return ordered


def scenario_trace(manifest: dict, scenarios: dict, scenario: str, *, authorized: bool = True) -> dict:
    record = scenarios["scenarios"].get(scenario)
    if record is None:
        raise TraceError(f"unknown scenario: {scenario}")
    if record.get("requires_authorization") and not authorized:
        raise TraceError(f"authorization required for scenario: {scenario}")
    loaded = closure(manifest, record["entry"])
    expected = record["expected_nodes"]
    prohibited = set(record.get("prohibited_nodes", []))
    if loaded != expected:
        raise TraceError(f"{scenario}: expected {expected}, loaded {loaded}")
    forbidden = prohibited.intersection(loaded)
    if forbidden:
        raise TraceError(f"{scenario}: prohibited nodes loaded: {sorted(forbidden)}")
    return {
        "scenario": scenario,
        "entry": record["entry"],
        "loaded_nodes": loaded,
        "prohibited_nodes": sorted(prohibited),
        "authorized": authorized,
    }


def file_digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def package(root: Path, output: Path, scenario: str) -> dict:
    manifest, scenarios = load_spec(root)
    trace = scenario_trace(manifest, scenarios, scenario)
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    files = []
    for node in trace["loaded_nodes"]:
        source = root / manifest["nodes"][node]["path"]
        if not source.is_file():
            raise TraceError(f"missing source for {node}: {source}")
        destination = output / manifest["nodes"][node]["package_path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        data = source.read_bytes()
        destination.write_bytes(data)
        files.append({
            "node": node,
            "path": destination.relative_to(output).as_posix(),
            "bytes": len(data),
            "sha256": file_digest(data),
        })

    description = manifest["description"]
    if "turn-signal-into-work" not in description or "signal" not in description:
        raise TraceError("description must remain meaningful and trigger-bearing")
    package_manifest = {
        "schema_version": 1,
        "skill": manifest["skill"],
        "scenario": scenario,
        "description": description,
        "loaded_nodes": trace["loaded_nodes"],
        "files": sorted(files, key=lambda item: item["path"]),
        "total_bytes": sum(item["bytes"] for item in files),
        "total_words": sum(len((output / item["path"]).read_text(encoding="utf-8").split()) for item in files),
    }
    (output / "package.json").write_text(
        json.dumps(package_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return {"manifest": package_manifest, "trace": trace}


def baseline(root: Path) -> dict:
    adapter = root / "adapters" / "codex" / "skills" / "alawas-turn-signal-into-work"
    files = sorted(path for path in adapter.rglob("*") if path.is_file())
    if not files:
        raise TraceError(f"generated Codex adapter is missing: {adapter}")
    return {
        "source": adapter.relative_to(root).as_posix(),
        "files": [
            {"path": path.relative_to(adapter).as_posix(), "bytes": path.stat().st_size}
            for path in files
        ],
        "total_bytes": sum(path.stat().st_size for path in files),
        "total_words": sum(len(path.read_text(encoding="utf-8").split()) for path in files),
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("trace", "package", "baseline"))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--scenario", default="capture")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if args.command == "trace":
        manifest, scenarios = load_spec(root)
        result = scenario_trace(manifest, scenarios, args.scenario)
    elif args.command == "baseline":
        result = baseline(root)
    else:
        if args.output is None:
            parser.error("package requires --output")
        result = package(root, args.output.resolve(), args.scenario)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
