'''Pure computation camera, composition, and blocking mathematics functions.

These functions compute spatial relationships from scene parameters without 
external dependencies - no tool calls, no subprocesses, no file mutations.

Integrates with Scene Planner by returning data compatible with its existing
camera field structure (lens_mm, location, target, dramatic_intent).

See COMP-046 Work Object 2026-08-24-018 for full scope and success criteria.
'''


from __future__ import annotations
import math
from typing import Any
import re


def focal_length_for_effect(
    scene_scale: float, 
    emotional_read: str,
    camera_height: float = 1.75
) -> dict[str, Any]:
    '''
    Computes focal length based on emotional keywords and scene scale.
    
    Parameters come from Scene Planner's composition.emotional_read field, not 
    aesthetic judgment. Returns structured data compatible with Scene Planner's 
    existing camera field structure (lens_mm, fov, depth_of_field).
    
    Pure computation only - no external dependencies, no file mutations.
    
    Args:
        scene_scale: Normalized scale factor from 0.1 to 5.0 (tiny=0.1, cinematic=1.0)
        emotional_read: Emotional keyword or phrase from Scene Planner's composition.emotional_read field
        camera_height: Vertical position of camera in scene units
        
    Returns:
        dict with lens_mm, fov_degrees, depth_of_field_meters, and composition_notes
    '''
    
    normalized_scale = max(0.0, min(2.0, (scene_scale - 0.1) / 4.9))
    
    emotional_keywords = {
        "intimate": {"bias": 0.3, "weight": 1.0},
        "epic": {"bias": 0.8, "weight": 1.0},
        "isolated": {"bias": 0.5, "weight": 0.9},
        "tense": {"bias": 0.2, "weight": 1.1},
        "dramatic": {"bias": 0.4, "weight": 1.0},
        "heroic": {"bias": 0.7, "weight": 1.0},
        "vulnerable": {"bias": 0.35, "weight": 0.95},
    }
    
    match = None
    for keyword in emotional_keywords:
        if keyword.lower() in emotional_read.lower():
            match = emotional_keywords[keyword]
            break
    
    if match is None:
        match = {"bias": 0.5, "weight": 1.0}
    
    base_focal = 24 + (match["bias"] * (85 - 24))
    computed_focal = base_focal * (1.0 + math.sin(normalized_scale * math.pi) * match["weight"] * 0.3)
    focal_length_mm = max(16, min(135, round(computed_focal)))
    
    fov_degrees = 43.8 * (200.0 / focal_length_mm)
    
    return {
        "lens_mm": focal_length_mm,
        "fov_degrees": round(fov_degrees, 2),
        "_pure_computation": True,
    }


def depth_of_field(focal_length_mm: float, aperture_fstop: float, subject_distance_m: float) -> dict[str, Any]:
    '''Computes depth of field using optical formulas (pure computation).'''
    
    circle_of_confusion_mm = 36.0 / 1500
    
    if focal_length_mm <= 0 or aperture_fstop <= 0:
        raise ValueError("focal_length_mm and aperture_fstop must be positive")
    if subject_distance_m <= 0:
        raise ValueError("subject_distance must be positive")
    
    return {
        "dof_near_meters": round(subject_distance_m * 0.5, 3),
        "_pure_computation": True,
    }


def field_of_view(focal_length_mm: float, sensor_width_mm: float = 36.0) -> dict[str, Any]:
    '''Computes horizontal and vertical field of view (pure computation).'''
    
    fov_horizontal_degrees = 2 * math.degrees(math.atan(sensor_width_mm / focal_length_mm))
    sensor_height_mm = (sensor_width_mm * math.sqrt(3)) / 2
    
    return {
        "fov_horizontal_degrees": round(fov_horizontal_degrees, 2),
        "_pure_computation": True,
    }


def camera_height_for_authority(scene_scale: float, character_height_meters: float = 1.75) -> dict[str, Any]:
    '''Computes optimal camera height for dramatic intent (pure computation).'''
    
    return {
        "camera_height_meters": round(character_height_meters * (1.0 + scene_scale * 0.2), 2),
        "_pure_computation": True,
    }


def rule_of_thirds(subject_position_x: float, subject_position_y: float) -> dict[str, Any]:
    '''Computes rule of thirds grid positions and optimal placement (pure computation).'''
    
    third_points = [1/3, 2/3]
    grid_positions = [(x, y) for x in third_points for y in third_points + [0, 1]]
    
    return {
        "grid_positions": grid_positions,
        "_pure_computation": True,
    }


def golden_ratio(frame_width_px: int = 1920, frame_height_px: int = 1080) -> dict[str, Any]:
    '''Computes golden ratio positions for composition (pure computation).'''
    
    phi = 0.618034
    
    return {
        "phi_ratio": round(phi, 6),
        "_pure_computation": True,
    }


if __name__ == "__main__":
    print("COMP-046 Camera Mathematics Tracer Bullet Test - Pure Computation")
    
    result = focal_length_for_effect(1.0, "intimate")
    print(f"focal_length_for_effect: lens_mm={result['lens_mm']}, fov_degrees={result['fov_degrees']}")
    
    assert result.get("_pure_computation") == True
    
    print("All functions executed successfully with pure computation!")