"""
Full Pipeline Integration — Tracer Bullet (WO 2026-08-25-007)

Tests the full 6-stage asset pipeline with live adapters:
- ComfyUIAdapter for concept and mesh stages
- BlenderAdapter for cleanup, material, and rig stages

Proves the adapter layer pattern works for full pipeline integration.
"""

import json
import time
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Optional

# Import adapters from the adapter layer
import sys
sys.path.insert(0, str(Path(__file__).parent / "adapters"))
from tracer_bullet import ComfyUIAdapter, BlenderAdapter, JobStatus


class AssetState(str, Enum):
    CONCEPT = "concept"
    MESH = "mesh"
    CLEANUP = "cleanup"
    MATERIAL = "material"
    RIG = "rig"
    REGISTERED = "registered"


class AssetStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AssetRecord:
    asset_id: str
    description: str
    current_state: AssetState
    status: AssetStatus
    retry_count: int
    max_retries: int
    state_history: list
    error_log: list
    output_path: Optional[str] = None
    registry_path: Optional[str] = None


def create_asset_record(asset_id: str, description: str, output_path: str) -> AssetRecord:
    """Create a new asset record in concept state."""
    return AssetRecord(
        asset_id=asset_id,
        description=description,
        current_state=AssetState.CONCEPT,
        status=AssetStatus.PENDING,
        retry_count=0,
        max_retries=3,
        state_history=[],
        error_log=[],
        output_path=output_path,
    )


def save_asset_record(record: AssetRecord, path: Path):
    """Save asset record to JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(asdict(record), f, indent=2)


def load_asset_record(path: Path) -> AssetRecord:
    """Load asset record from JSON file."""
    with open(path) as f:
        data = json.load(f)
    data["current_state"] = AssetState(data["current_state"])
    data["status"] = AssetStatus(data["status"])
    return AssetRecord(**data)


def run_concept_stage(record: AssetRecord, adapter: ComfyUIAdapter) -> AssetRecord:
    """Generate concept art using ComfyUIAdapter."""
    print(f"[concept] Generating concept art for: {record.description}")
    
    # Submit job to ComfyUI
    job_id = adapter.submit_job("concept_art", {
        "prompt": record.description,
        "model": "flux",
    })
    
    # Poll for completion
    time.sleep(0.3)
    status = adapter.poll_status(job_id)
    assert status == JobStatus.COMPLETED, f"Expected COMPLETED, got {status}"
    
    # Get result
    result = adapter.get_result(job_id)
    assert result.status == JobStatus.COMPLETED
    
    # Update record
    record.state_history.append({
        "from": record.current_state.value,
        "to": AssetState.MESH.value,
        "timestamp": time.time(),
        "result": "success",
        "job_id": job_id,
        "output": result.output,
    })
    record.current_state = AssetState.MESH
    record.status = AssetStatus.IN_PROGRESS
    record.retry_count = 0
    print(f"[concept] Concept art generated. Transitioning to mesh state.")
    return record


def run_mesh_stage(record: AssetRecord, adapter: ComfyUIAdapter) -> AssetRecord:
    """Generate 3D mesh using ComfyUIAdapter."""
    print(f"[mesh] Generating 3D mesh for: {record.description}")
    
    # Submit job to ComfyUI
    job_id = adapter.submit_job("mesh_generation", {
        "image_path": f"/tmp/comfyui/{record.asset_id}-concept.png",
        "model": "hunyuan3d",
    })
    
    # Poll for completion
    time.sleep(0.3)
    status = adapter.poll_status(job_id)
    assert status == JobStatus.COMPLETED, f"Expected COMPLETED, got {status}"
    
    # Get result
    result = adapter.get_result(job_id)
    assert result.status == JobStatus.COMPLETED
    
    # Update record
    record.state_history.append({
        "from": record.current_state.value,
        "to": AssetState.CLEANUP.value,
        "timestamp": time.time(),
        "result": "success",
        "job_id": job_id,
        "output": result.output,
    })
    record.current_state = AssetState.CLEANUP
    record.status = AssetStatus.IN_PROGRESS
    record.retry_count = 0
    print(f"[mesh] 3D mesh generated. Transitioning to cleanup state.")
    return record


def run_cleanup_stage(record: AssetRecord, adapter: BlenderAdapter) -> AssetRecord:
    """Import and cleanup mesh using BlenderAdapter."""
    print(f"[cleanup] Importing and cleaning up mesh for: {record.description}")
    
    # Submit job to Blender
    job_id = adapter.submit_job("cleanup", {
        "object_name": record.asset_id,
        "scene": "default",
    })
    
    # Poll for completion
    time.sleep(0.3)
    status = adapter.poll_status(job_id)
    assert status == JobStatus.COMPLETED, f"Expected COMPLETED, got {status}"
    
    # Get result
    result = adapter.get_result(job_id)
    assert result.status == JobStatus.COMPLETED
    
    # Update record
    record.state_history.append({
        "from": record.current_state.value,
        "to": AssetState.MATERIAL.value,
        "timestamp": time.time(),
        "result": "success",
        "job_id": job_id,
        "output": result.output,
    })
    record.current_state = AssetState.MATERIAL
    record.status = AssetStatus.IN_PROGRESS
    record.retry_count = 0
    print(f"[cleanup] Cleanup complete. Transitioning to material state.")
    return record


def run_material_stage(record: AssetRecord, adapter: BlenderAdapter) -> AssetRecord:
    """Assign materials using BlenderAdapter."""
    print(f"[material] Assigning materials for: {record.description}")
    
    # Submit job to Blender
    job_id = adapter.submit_job("assign_material", {
        "object_name": record.asset_id,
        "material_name": "default",
        "scene": "default",
    })
    
    # Poll for completion
    time.sleep(0.3)
    status = adapter.poll_status(job_id)
    assert status == JobStatus.COMPLETED, f"Expected COMPLETED, got {status}"
    
    # Get result
    result = adapter.get_result(job_id)
    assert result.status == JobStatus.COMPLETED
    
    # Update record
    record.state_history.append({
        "from": record.current_state.value,
        "to": AssetState.RIG.value,
        "timestamp": time.time(),
        "result": "success",
        "job_id": job_id,
        "output": result.output,
    })
    record.current_state = AssetState.RIG
    record.status = AssetStatus.IN_PROGRESS
    record.retry_count = 0
    print(f"[material] Materials assigned. Transitioning to rig state.")
    return record


def run_rig_stage(record: AssetRecord, adapter: BlenderAdapter) -> AssetRecord:
    """Rig asset using BlenderAdapter."""
    print(f"[rig] Rigging asset: {record.description}")
    
    # Submit job to Blender
    job_id = adapter.submit_job("rig", {
        "object_name": record.asset_id,
        "scene": "default",
    })
    
    # Poll for completion
    time.sleep(0.3)
    status = adapter.poll_status(job_id)
    assert status == JobStatus.COMPLETED, f"Expected COMPLETED, got {status}"
    
    # Get result
    result = adapter.get_result(job_id)
    assert result.status == JobStatus.COMPLETED
    
    # Update record
    record.state_history.append({
        "from": record.current_state.value,
        "to": AssetState.REGISTERED.value,
        "timestamp": time.time(),
        "result": "success",
        "job_id": job_id,
        "output": result.output,
    })
    record.current_state = AssetState.REGISTERED
    record.status = AssetStatus.IN_PROGRESS
    record.retry_count = 0
    print(f"[rig] Rigging complete. Transitioning to registered state.")
    return record


def run_registered_stage(record: AssetRecord, registry_path: Path) -> AssetRecord:
    """Register asset in the asset registry."""
    print(f"[registered] Registering asset: {record.asset_id}")
    
    # Create registry entry
    registry_entry = {
        "asset_id": record.asset_id,
        "description": record.description,
        "output_path": record.output_path,
        "state": record.current_state.value,
        "registered_at": time.time(),
    }
    
    # Save to registry
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    if registry_path.exists():
        with open(registry_path) as f:
            registry = json.load(f)
    else:
        registry = []
    
    registry.append(registry_entry)
    
    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2)
    
    record.registry_path = str(registry_path)
    record.state_history.append({
        "from": record.current_state.value,
        "to": "completed",
        "timestamp": time.time(),
        "result": "success",
    })
    record.status = AssetStatus.COMPLETED
    record.retry_count = 0
    print(f"[registered] Asset registered in registry: {registry_path}")
    return record


def run_pipeline(asset_id: str, description: str, output_path: str, 
                 record_path: Path, registry_path: Path) -> AssetRecord:
    """Run the asset pipeline with live adapters."""
    
    # Create adapters
    comfyui_adapter = ComfyUIAdapter()
    blender_adapter = BlenderAdapter()
    
    # Create or load asset record
    if record_path.exists():
        print(f"[pipeline] Loading existing asset record from: {record_path}")
        record = load_asset_record(record_path)
    else:
        print(f"[pipeline] Creating new asset record for: {asset_id}")
        record = create_asset_record(asset_id, description, output_path)
        save_asset_record(record, record_path)
    
    # Run pipeline stages
    if record.current_state == AssetState.CONCEPT:
        record = run_concept_stage(record, comfyui_adapter)
        save_asset_record(record, record_path)
    
    if record.current_state == AssetState.MESH:
        record = run_mesh_stage(record, comfyui_adapter)
        save_asset_record(record, record_path)
    
    if record.current_state == AssetState.CLEANUP:
        record = run_cleanup_stage(record, blender_adapter)
        save_asset_record(record, record_path)
    
    if record.current_state == AssetState.MATERIAL:
        record = run_material_stage(record, blender_adapter)
        save_asset_record(record, record_path)
    
    if record.current_state == AssetState.RIG:
        record = run_rig_stage(record, blender_adapter)
        save_asset_record(record, record_path)
    
    if record.current_state == AssetState.REGISTERED:
        record = run_registered_stage(record, registry_path)
        save_asset_record(record, record_path)
    
    print(f"\n[pipeline] Asset pipeline completed successfully!")
    print(f"[pipeline] Final state: {record.current_state.value}")
    print(f"[pipeline] Output: {output_path}")
    return record


def main():
    """Full pipeline integration tracer bullet."""
    
    # Setup
    test_dir = Path("C:/Users/Andre/AppData/Local/Temp/opencode/full-pipeline-integration-test")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    record_path = test_dir / "full-pipeline-integration-asset.json"
    output_path = str(test_dir / "full-pipeline-integration-asset.blend")
    registry_path = test_dir / "asset-registry.json"
    
    # Clean up any previous test
    if record_path.exists():
        record_path.unlink()
    if registry_path.exists():
        registry_path.unlink()
    
    print("=" * 60)
    print("FULL PIPELINE INTEGRATION TRACER BULLET")
    print("WO 2026-08-25-007 Decision 1")
    print("=" * 60)
    
    # Run pipeline
    record = run_pipeline(
        asset_id="full-pipeline-integration-001",
        description="A simple cube prop for testing",
        output_path=output_path,
        record_path=record_path,
        registry_path=registry_path,
    )
    
    # Verify completion
    assert record.status == AssetStatus.COMPLETED, f"Expected COMPLETED, got {record.status.value}"
    assert record.current_state == AssetState.REGISTERED, f"Expected REGISTERED, got {record.current_state.value}"
    print("\n[verify] Full pipeline completed successfully")
    print(f"[verify] State: {record.current_state.value}")
    print(f"[verify] Status: {record.status.value}")
    
    # Verify state history
    print("\n--- Verify state history ---")
    print(f"[verify] State transitions recorded: {len(record.state_history)}")
    for i, transition in enumerate(record.state_history):
        print(f"  {i+1}. {transition['from']} -> {transition['to']} ({transition['result']})")
    
    # Verify persistence
    print("\n--- Verify persistence ---")
    loaded_record = load_asset_record(record_path)
    assert loaded_record.current_state == record.current_state, "State mismatch after load"
    assert loaded_record.status == record.status, "Status mismatch after load"
    assert len(loaded_record.state_history) == len(record.state_history), "History mismatch after load"
    print("[verify] Asset record persists correctly across save/load")
    
    # Verify registry
    print("\n--- Verify registry ---")
    assert registry_path.exists(), "Registry file does not exist"
    with open(registry_path) as f:
        registry = json.load(f)
    assert len(registry) == 1, f"Expected 1 registry entry, got {len(registry)}"
    assert registry[0]["asset_id"] == "full-pipeline-integration-001", "Asset ID mismatch in registry"
    print(f"[verify] Asset registered in registry: {registry_path}")
    print(f"[verify] Registry entries: {len(registry)}")
    
    # Verify adapter usage
    print("\n--- Verify adapter usage ---")
    comfyui_jobs = [t for t in record.state_history if "comfyui" in t.get("job_id", "")]
    blender_jobs = [t for t in record.state_history if "blender" in t.get("job_id", "")]
    print(f"[verify] ComfyUI jobs: {len(comfyui_jobs)} (concept, mesh)")
    print(f"[verify] Blender jobs: {len(blender_jobs)} (cleanup, material, rig)")
    assert len(comfyui_jobs) == 2, f"Expected 2 ComfyUI jobs, got {len(comfyui_jobs)}"
    assert len(blender_jobs) == 3, f"Expected 3 Blender jobs, got {len(blender_jobs)}"
    
    # Summary
    print("\n" + "=" * 60)
    print("FULL PIPELINE INTEGRATION RESULTS")
    print("=" * 60)
    print(f"Asset ID: {record.asset_id}")
    print(f"Final state: {record.current_state.value}")
    print(f"Final status: {record.status.value}")
    print(f"State transitions: {len(record.state_history)}")
    print(f"ComfyUI jobs: {len(comfyui_jobs)}")
    print(f"Blender jobs: {len(blender_jobs)}")
    print(f"Registry entries: {len(registry)}")
    print(f"Full pipeline integration: VERIFIED")
    print("=" * 60)


if __name__ == "__main__":
    main()
