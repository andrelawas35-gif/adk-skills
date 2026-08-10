"""Shared assertions for namespaced generated adapter contracts."""

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def _generator():
    """Load tools/generate-adapters.py once via importlib (hyphenated name)."""
    spec = importlib.util.spec_from_file_location(
        "generate_adapters", ROOT / "tools" / "generate-adapters.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def namespaced_core_body(core_file):
    """The core body exactly as the generator would emit it in an adapter.

    Mirrors the generator's build pipeline (namespace_skill_references +
    inject_shared_preamble) by delegating to the generator itself, so the
    helper can never drift from what the generator actually produces.
    """
    ga = _generator()
    body = ga.namespace_skill_references(
        ga.extract_body(core_file)
    )
    body = ga.inject_shared_preamble(body, core_file.parent.name)
    return body.rstrip("\n")
