"""Translate directorial intent into a bounded, executable scene specification.

This tracer is deliberately local and side-effect free. It reads a caller-owned
fixture registry, selects only registered assets, and emits descriptions for
the bounded Blender operator; it never imports Blender or invokes a tool.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml


BOUNDED_OPS = frozenset(
    {
        "object.import_mesh",
        "camera.set",
        "light.set",
        "render.preview",
    }
)

_NEED_ALIASES = {
    "character": {"character", "person", "protagonist", "hero", "him", "her"},
    "landscape": {"landscape", "terrain", "mountain", "valley", "environment"},
    "prop": {"prop", "object", "weapon", "vehicle"},
}


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def _load_registry(path: Path) -> list[dict[str, Any]]:
    document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    assets = document.get("assets", [])
    if not isinstance(assets, list):
        raise ValueError("fixture registry 'assets' must be a list")
    return assets


def _need_matches(prompt_tokens: set[str], asset: dict[str, Any]) -> set[str]:
    tags = {str(tag).lower() for tag in asset.get("tags", [])}
    matches = set()
    for need, aliases in _NEED_ALIASES.items():
        if prompt_tokens & aliases and tags & aliases:
            matches.add(need)
    return matches


def _requested_needs(prompt_tokens: set[str]) -> list[str]:
    needs = []
    for need, aliases in _NEED_ALIASES.items():
        if prompt_tokens & aliases:
            needs.append(need)
    return needs or ["character", "landscape"]


def _emotional_parameters(prompt: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    tokens = _tokens(prompt)
    tiny = bool(tokens & {"tiny", "small", "isolated", "alone", "vast"})
    tense = bool(tokens & {"tense", "threat", "danger", "urgent"})

    camera = {
        "name": "ScenePlannerCamera",
        "lens_mm": 35 if tiny else 50,
        "location": [0.0, -18.0 if tiny else -10.0, 4.0 if tiny else 2.5],
        "target": [0.0, 0.0, 1.0],
        "dramatic_intent": "scale_and_isolation" if tiny else "direct_subject_attention",
    }
    lighting = {
        "name": "ScenePlannerKey",
        "energy": 900 if tense else 650,
        "color": [1.0, 0.78, 0.58] if tense else [1.0, 1.0, 1.0],
        "dramatic_intent": "urgent_contrast" if tense else "neutral_readability",
    }
    composition = {
        "subject_scale": "small_in_frame" if tiny else "medium_in_frame",
        "horizon_emphasis": "wide_landscape" if tiny else "subject_first",
        "emotional_read": "vulnerable_against_scale" if tiny else "clear_subject_presence",
    }
    return camera, lighting, composition


def plan_scene(prompt: str, registry_path: Path) -> dict[str, Any]:
    """Return a deterministic scene plan without executing any operation."""
    if not prompt or not prompt.strip():
        raise ValueError("directorial prompt must not be empty")

    assets = _load_registry(registry_path)
    prompt_tokens = _tokens(prompt)
    requested_needs = _requested_needs(prompt_tokens)
    matches = []
    matched_needs = set()
    for asset in assets:
        asset_needs = _need_matches(prompt_tokens, asset)
        if asset_needs:
            matches.append(
                {
                    "asset_id": asset["asset_id"],
                    "path": asset["path"],
                    "needs": sorted(asset_needs),
                    "match_reason": "registered_tag_match",
                }
            )
            matched_needs.update(asset_needs)

    gaps = [
        {"need": need, "reason": "no_registered_asset_match", "fabricated": False}
        for need in requested_needs
        if need not in matched_needs
    ]
    camera, lighting, composition = _emotional_parameters(prompt)
    command_plan = [
        {
            "op": "object.import_mesh",
            "params": {"path": asset["path"], "asset_id": asset["asset_id"]},
            "source_asset_id": asset["asset_id"],
        }
        for asset in matches
    ]
    command_plan.extend(
        [
            {"op": "camera.set", "params": {"name": camera["name"], "lens_mm": camera["lens_mm"]}},
            {"op": "light.set", "params": {"name": lighting["name"], "energy": lighting["energy"], "color": lighting["color"]}},
            {"op": "render.preview", "params": {"width": 1280, "height": 720}},
        ]
    )
    for command in command_plan:
        if command["op"] not in BOUNDED_OPS:
            raise AssertionError(f"planner emitted unsupported op: {command['op']}")

    return {
        "intent": {"prompt": prompt.strip(), "requested_needs": requested_needs},
        "asset_matches": matches,
        "asset_gaps": gaps,
        "camera": camera,
        "lighting": lighting,
        "composition": composition,
        "render_passes": [{"name": "preview", "format": "PNG", "resolution": [1280, 720]}],
        "blender_command_plan": command_plan,
    }


def plan_scene_yaml(prompt: str, registry_path: Path) -> str:
    """Return the scene plan as stable, human-readable YAML."""
    return yaml.safe_dump(plan_scene(prompt, registry_path), sort_keys=False)


class ScenePlanner:
    """Small object wrapper for callers that reuse one registry path."""

    def __init__(self, registry_path: Path):
        self.registry_path = Path(registry_path)

    def plan(self, prompt: str) -> dict[str, Any]:
        return plan_scene(prompt, self.registry_path)

    def plan_yaml(self, prompt: str) -> str:
        return plan_scene_yaml(prompt, self.registry_path)
