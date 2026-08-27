"""
Asset Pipeline State Machine — Tracer Bullet (WO 2026-08-24-020 Decision 2)

Tests 3 stages (concept → mesh → cleanup) with simulated failure at mesh stage
and resume capability. Proves the state-machine assumption before full pipeline.
"""

import json
import os
import time
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Optional


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


def run_concept_stage(record: AssetRecord) -> AssetRecord:
    """Simulate concept art generation (ComfyUI Flux)."""
    print(f"[concept] Generating concept art for: {record.description}")
    time.sleep(0.1)  # Simulate work
    record.state_history.append({
        "from": record.current_state.value,
        "to": AssetState.MESH.value,
        "timestamp": time.time(),
        "result": "success",
    })
    record.current_state = AssetState.MESH
    record.status = AssetStatus.IN_PROGRESS
    record.retry_count = 0
    print(f"[concept] Concept art generated. Transitioning to mesh state.")
    return record


def run_mesh_stage(record: AssetRecord, simulate_failure: bool = False) -> AssetRecord:
    """Simulate 3D mesh generation (ComfyUI Hunyuan3D-2)."""
    print(f"[mesh] Generating 3D mesh for: {record.description}")
    
    if simulate_failure and record.retry_count == 0:
        # Simulate a recoverable failure on first attempt
        record.retry_count += 1
        error_msg = "Simulated failure: ComfyUI timeout on first attempt"
        record.error_log.append({
            "state": AssetState.MESH.value,
            "error": error_msg,
            "retry_count": record.retry_count,
            "timestamp": time.time(),
        })
        record.status = AssetStatus.FAILED
        print(f"[mesh] FAILED: {error_msg} (retry {record.retry_count}/{record.max_retries})")
        return record
    
    time.sleep(0.1)  # Simulate work
    record.state_history.append({
        "from": record.current_state.value,
        "to": AssetState.CLEANUP.value,
        "timestamp": time.time(),
        "result": "success",
    })
    record.current_state = AssetState.CLEANUP
    record.status = AssetStatus.IN_PROGRESS
    record.retry_count = 0
    print(f"[mesh] 3D mesh generated. Transitioning to cleanup state.")
    return record


def run_cleanup_stage(record: AssetRecord) -> AssetRecord:
    """Simulate Blender import and cleanup."""
    print(f"[cleanup] Importing and cleaning up mesh for: {record.description}")
    time.sleep(0.1)  # Simulate work
    record.state_history.append({
        "from": record.current_state.value,
        "to": AssetState.MATERIAL.value,
        "timestamp": time.time(),
        "result": "success",
    })
    record.current_state = AssetState.MATERIAL
    record.status = AssetStatus.COMPLETED
    record.retry_count = 0
    print(f"[cleanup] Cleanup complete. Asset ready for material stage.")
    return record


def resume_from_state(record: AssetRecord, simulate_failure: bool = False) -> AssetRecord:
    """Resume pipeline from the current state."""
    print(f"\n[resume] Resuming from state: {record.current_state.value}")
    print(f"[resume] Status: {record.status.value}")
    print(f"[resume] Retry count: {record.retry_count}")
    
    if record.current_state == AssetState.CONCEPT:
        return run_concept_stage(record)
    elif record.current_state == AssetState.MESH:
        return run_mesh_stage(record, simulate_failure=simulate_failure)
    elif record.current_state == AssetState.CLEANUP:
        return run_cleanup_stage(record)
    else:
        print(f"[resume] State {record.current_state.value} not implemented in tracer bullet")
        return record


def run_pipeline(asset_id: str, description: str, output_path: str, 
                 record_path: Path, simulate_failure: bool = True) -> AssetRecord:
    """Run the asset pipeline with optional simulated failure."""
    
    # Create or load asset record
    if record_path.exists():
        print(f"[pipeline] Loading existing asset record from: {record_path}")
        record = load_asset_record(record_path)
    else:
        print(f"[pipeline] Creating new asset record for: {asset_id}")
        record = create_asset_record(asset_id, description, output_path)
        save_asset_record(record, record_path)
    
    # Run pipeline stages
    stages = [run_concept_stage, run_mesh_stage, run_cleanup_stage]
    
    for stage_fn in stages:
        # Resume from current state
        if record.current_state == AssetState.CONCEPT and stage_fn == run_concept_stage:
            record = stage_fn(record)
        elif record.current_state == AssetState.MESH and stage_fn == run_mesh_stage:
            record = stage_fn(record, simulate_failure=simulate_failure)
        elif record.current_state == AssetState.CLEANUP and stage_fn == run_cleanup_stage:
            record = stage_fn(record)
        else:
            # Skip stages we've already completed
            continue
        
        save_asset_record(record, record_path)
        
        if record.status == AssetStatus.FAILED:
            print(f"\n[pipeline] Asset failed at state: {record.current_state.value}")
            print(f"[pipeline] Error: {record.error_log[-1]['error'] if record.error_log else 'unknown'}")
            return record
    
    print(f"\n[pipeline] Asset pipeline completed successfully!")
    print(f"[pipeline] Final state: {record.current_state.value}")
    print(f"[pipeline] Output: {output_path}")
    return record


def main():
    """Tracer bullet: test 3-stage pipeline with simulated failure and resume."""
    
    # Setup
    test_dir = Path("C:/Users/Andre/AppData/Local/Temp/opencode/asset-pipeline-test")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    record_path = test_dir / "test-asset.json"
    output_path = str(test_dir / "test-asset.blend")
    
    # Clean up any previous test
    if record_path.exists():
        record_path.unlink()
    
    print("=" * 60)
    print("ASSET PIPELINE TRACER BULLET")
    print("WO 2026-08-24-020 Decision 2")
    print("=" * 60)
    
    # Phase 1: Run with simulated failure
    print("\n--- Phase 1: Run with simulated failure at mesh stage ---")
    record = run_pipeline(
        asset_id="tracer-bullet-001",
        description="A simple cube prop for testing",
        output_path=output_path,
        record_path=record_path,
        simulate_failure=True,
    )
    
    # Verify failure was recorded
    assert record.status == AssetStatus.FAILED, f"Expected FAILED, got {record.status.value}"
    assert record.current_state == AssetState.MESH, f"Expected MESH, got {record.current_state.value}"
    assert record.retry_count == 1, f"Expected retry_count=1, got {record.retry_count}"
    assert len(record.error_log) == 1, f"Expected 1 error, got {len(record.error_log)}"
    print("\n[verify] Failure correctly recorded at mesh stage")
    print(f"[verify] State: {record.current_state.value}")
    print(f"[verify] Status: {record.status.value}")
    print(f"[verify] Retry count: {record.retry_count}")
    
    # Phase 2: Resume from failure
    print("\n--- Phase 2: Resume from mesh stage (no failure) ---")
    record = resume_from_state(record, simulate_failure=False)
    save_asset_record(record, record_path)
    
    # Verify mesh stage succeeded
    assert record.current_state == AssetState.CLEANUP, f"Expected CLEANUP, got {record.current_state.value}"
    assert record.retry_count == 0, f"Expected retry_count=0, got {record.retry_count}"
    print("\n[verify] Resume from mesh stage succeeded")
    print(f"[verify] State: {record.current_state.value}")
    
    # Phase 2b: Continue to cleanup stage
    print("\n--- Phase 2b: Continue to cleanup stage ---")
    record = resume_from_state(record, simulate_failure=False)
    save_asset_record(record, record_path)
    
    # Verify cleanup succeeded
    assert record.status == AssetStatus.COMPLETED, f"Expected COMPLETED, got {record.status.value}"
    assert record.current_state == AssetState.MATERIAL, f"Expected MATERIAL, got {record.current_state.value}"
    print("\n[verify] Cleanup stage succeeded")
    print(f"[verify] State: {record.current_state.value}")
    print(f"[verify] Status: {record.status.value}")
    
    # Phase 3: Verify state history
    print("\n--- Phase 3: Verify state history ---")
    print(f"[verify] State transitions recorded: {len(record.state_history)}")
    for i, transition in enumerate(record.state_history):
        print(f"  {i+1}. {transition['from']} -> {transition['to']} ({transition['result']})")
    
    # Phase 4: Verify persistence
    print("\n--- Phase 4: Verify persistence ---")
    loaded_record = load_asset_record(record_path)
    assert loaded_record.current_state == record.current_state, "State mismatch after load"
    assert loaded_record.status == record.status, "Status mismatch after load"
    assert len(loaded_record.state_history) == len(record.state_history), "History mismatch after load"
    print("[verify] Asset record persists correctly across save/load")
    
    # Summary
    print("\n" + "=" * 60)
    print("TRACER BULLET RESULTS")
    print("=" * 60)
    print(f"Asset ID: {record.asset_id}")
    print(f"Final state: {record.current_state.value}")
    print(f"Final status: {record.status.value}")
    print(f"State transitions: {len(record.state_history)}")
    print(f"Errors recorded: {len(record.error_log)}")
    print(f"Resume from failure: SUCCESS")
    print(f"State machine tracks progress: SUCCESS")
    print(f"Persistence across save/load: SUCCESS")
    print("=" * 60)
    
    return record


if __name__ == "__main__":
    main()
