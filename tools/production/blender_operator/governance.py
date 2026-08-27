"""Governance checks for the bounded Blender operator (COMP-042).

Pure Python (no bpy) so the two governance gates in WO 2026-08-24-014 are
unit-testable without a live Blender session:

1. **Protect-field governance** — before any mutating command executes, the
   caller declares ``protect`` (names that must not change). A command whose
   mutation target is in the protected set is rejected before touching Blender.
2. **execute_blender_python escalation gate** — arbitrary Python is a
   high-consequence escalation (WO 2026-08-23-001 §4.2). It only runs with an
   explicit director authority record in the command; otherwise rejected.
"""

from __future__ import annotations

from typing import Any, Optional

# Ops that may mutate scene state (target a named element).
MUTATING_OPS = frozenset({
    "object.set_transform",
    "object.duplicate",
    "object.delete",
    "object.set_parent",
    "object.select",
    "object.deselect",
    "camera.set",
    "camera.lock",
    "light.set",
    "rig.set_bone_rotation",
    "animation.move_keyframe",
    "animation.set_interpolation",
    "mesh.move_vertices",
    "mesh.extrude",
    "mesh.separate_by_material",
    "mesh.add_modifier",
    "mesh.set_dimensions",
    "mesh.set_origin",
    "mesh.decimate",
    "mesh.remove_doubles",
    "material.set",
    "material.assign",
    "material.set_texture",
})

# Ops that load GPU-heavy work into VRAM (need a GPU claim first).
VRAM_OPS = frozenset({
    "render.preview",
    "render.final",
    "object.import_mesh",
    "image.set_as_reference",
    "image.import_as_plane",
    "material.set_texture",
})


def mutation_targets(op: str, params: dict) -> list[str]:
    """Return the named element(s) a mutating command targets.

    Falls back to a declared ``target`` field; the caller (Layer 2/3 skill)
    is expected to name the element a mutation touches so ``protect`` can be
    enforced. Returns [] for read-only ops (nothing to protect against).
    """
    if op not in MUTATING_OPS:
        return []
    target = params.get("target")
    if target is None:
        target = params.get("name")
    if target is None:
        return []
    if isinstance(target, list):
        return [str(t) for t in target]
    return [str(target)]


def check_protect(op: str, params: dict, protect: Optional[list]) -> Optional[dict]:
    """Reject a mutation whose target is in the protected set.

    Returns an error dict ``{"code": "protected_element", ...}`` when the
    mutation must be blocked, else ``None`` (safe to proceed). ``protect`` is
    the caller-declared list of names that must not change (from Shot/Scene
    Work Object ``Protect:`` fields per the plan §8 constraint).
    """
    if not protect:
        return None
    protected = {str(p) for p in protect}
    targets = mutation_targets(op, params)
    for target in targets:
        if target in protected:
            return {
                "code": "protected_element",
                "message": (
                    f"mutation target {target!r} is protected and must not change"
                ),
                "target": target,
            }
    return None


def authorize_execute_blender_python(params: dict) -> Optional[dict]:
    """Gate the high-consequence ``execute_blender_python`` escalation.

    Arbitrary Blender Python (WO 2026-08-23-001 §4.2) requires an explicit
    director authority record in the command params:
    ``{"authority": {"granted_by": "director", "work_object": "<id>", ...}}``.
    Returns an error dict when the gate blocks, else ``None`` (authorized).
    """
    authority = params.get("authority")
    if not isinstance(authority, dict):
        return {
            "code": "requires_director_authority",
            "message": (
                "execute_blender_python is a high-consequence escalation that "
                "requires an explicit director authority record "
                "({authority: {granted_by: 'director', work_object: <id>}})"
            ),
        }
    if authority.get("granted_by") != "director":
        return {
            "code": "requires_director_authority",
            "message": "authority.granted_by must be 'director'",
        }
    if not authority.get("work_object"):
        return {
            "code": "requires_director_authority",
            "message": "authority.work_object (the approving Work Object id) is required",
        }
    return None


def validate_command(op: str, params: dict, protect: Optional[list]) -> Optional[dict]:
    """Run all governance gates for one command before execution.

    Returns the first blocking error dict, or ``None`` to proceed.
    """
    if op == "execute_blender_python":
        return authorize_execute_blender_python(params)
    if op in MUTATING_OPS:
        return check_protect(op, params, protect)
    return None
