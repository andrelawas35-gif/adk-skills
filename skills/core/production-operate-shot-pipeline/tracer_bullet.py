"""
Shot Pipeline State Machine — Tracer Bullet (WO 2026-08-24-021 Decision 2)

Tests Tier A (fast sketch) with simulated failure and resume capability.
Proves the state-machine pattern before building the full tiered pipeline.
"""

import json
import os
import time
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Optional


class ShotState(str, Enum):
    BREAKDOWN = "breakdown"
    TIER_A = "tier_a"
    TIER_B = "tier_b"
    TIER_C = "tier_c"
    FINAL = "final"


class ShotStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ShotRecord:
    shot_id: str
    description: str
    current_state: ShotState
    status: ShotStatus
    retry_count: int
    max_retries: int
    state_history: list
    error_log: list
    output_path: Optional[str] = None


def create_shot_record(shot_id: str, description: str, output_path: str) -> ShotRecord:
    """Create a new shot record in breakdown state."""
    return ShotRecord(
        shot_id=shot_id,
        description=description,
        current_state=ShotState.BREAKDOWN,
        status=ShotStatus.PENDING,
        retry_count=0,
        max_retries=3,
        state_history=[],
        error_log=[],
        output_path=output_path,
    )


def save_shot_record(record: ShotRecord, path: Path):
    """Save shot record to JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(asdict(record), f, indent=2)


def load_shot_record(path: Path) -> ShotRecord:
    """Load shot record from JSON file."""
    with open(path) as f:
        data = json.load(f)
    data["current_state"] = ShotState(data["current_state"])
    data["status"] = ShotStatus(data["status"])
    return ShotRecord(**data)


def run_breakdown_stage(record: ShotRecord) -> ShotRecord:
    """Simulate screenplay breakdown (scene planner)."""
    print(f"[breakdown] Breaking down shot: {record.description}")
    time.sleep(0.1)  # Simulate work
    record.state_history.append({
        "from": record.current_state.value,
        "to": ShotState.TIER_A.value,
        "timestamp": time.time(),
        "result": "success",
    })
    record.current_state = ShotState.TIER_A
    record.status = ShotStatus.IN_PROGRESS
    record.retry_count = 0
    print(f"[breakdown] Breakdown complete. Transitioning to Tier A.")
    return record


def run_tier_a_stage(record: ShotRecord, simulate_failure: bool = False) -> ShotRecord:
    """Simulate Tier A (fast sketch — rough 3D blocking, proxy lighting)."""
    print(f"[tier_a] Generating fast sketch for: {record.description}")
    
    if simulate_failure and record.retry_count == 0:
        # Simulate a recoverable failure on first attempt
        record.retry_count += 1
        error_msg = "Simulated failure: Blender timeout on first attempt"
        record.error_log.append({
            "state": ShotState.TIER_A.value,
            "error": error_msg,
            "retry_count": record.retry_count,
            "timestamp": time.time(),
        })
        record.status = ShotStatus.FAILED
        print(f"[tier_a] FAILED: {error_msg} (retry {record.retry_count}/{record.max_retries})")
        return record
    
    time.sleep(0.1)  # Simulate work
    record.state_history.append({
        "from": record.current_state.value,
        "to": ShotState.TIER_B.value,
        "timestamp": time.time(),
        "result": "success",
    })
    record.current_state = ShotState.TIER_B
    record.status = ShotStatus.IN_PROGRESS
    record.retry_count = 0
    print(f"[tier_a] Tier A complete. Transitioning to Tier B.")
    return record


def resume_from_state(record: ShotRecord, simulate_failure: bool = False) -> ShotRecord:
    """Resume pipeline from the current state."""
    print(f"\n[resume] Resuming from state: {record.current_state.value}")
    print(f"[resume] Status: {record.status.value}")
    print(f"[resume] Retry count: {record.retry_count}")
    
    if record.current_state == ShotState.BREAKDOWN:
        return run_breakdown_stage(record)
    elif record.current_state == ShotState.TIER_A:
        return run_tier_a_stage(record, simulate_failure=simulate_failure)
    else:
        print(f"[resume] State {record.current_state.value} not implemented in tracer bullet")
        return record


def run_pipeline(shot_id: str, description: str, output_path: str, 
                 record_path: Path, simulate_failure: bool = True) -> ShotRecord:
    """Run the shot pipeline with optional simulated failure."""
    
    # Create or load shot record
    if record_path.exists():
        print(f"[pipeline] Loading existing shot record from: {record_path}")
        record = load_shot_record(record_path)
    else:
        print(f"[pipeline] Creating new shot record for: {shot_id}")
        record = create_shot_record(shot_id, description, output_path)
        save_shot_record(record, record_path)
    
    # Run pipeline stages
    stages = [run_breakdown_stage, run_tier_a_stage]
    
    for stage_fn in stages:
        # Resume from current state
        if record.current_state == ShotState.BREAKDOWN and stage_fn == run_breakdown_stage:
            record = stage_fn(record)
        elif record.current_state == ShotState.TIER_A and stage_fn == run_tier_a_stage:
            record = stage_fn(record, simulate_failure=simulate_failure)
        else:
            # Skip stages we've already completed
            continue
        
        save_shot_record(record, record_path)
        
        if record.status == ShotStatus.FAILED:
            print(f"\n[pipeline] Shot failed at state: {record.current_state.value}")
            print(f"[pipeline] Error: {record.error_log[-1]['error'] if record.error_log else 'unknown'}")
            return record
    
    print(f"\n[pipeline] Shot pipeline completed successfully!")
    print(f"[pipeline] Final state: {record.current_state.value}")
    print(f"[pipeline] Output: {output_path}")
    return record


def main():
    """Tracer bullet: test Tier A pipeline with simulated failure and resume."""
    
    # Setup
    test_dir = Path("C:/Users/Andre/AppData/Local/Temp/opencode/shot-pipeline-test")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    record_path = test_dir / "test-shot.json"
    output_path = str(test_dir / "test-shot-render.png")
    
    # Clean up any previous test
    if record_path.exists():
        record_path.unlink()
    
    print("=" * 60)
    print("SHOT PIPELINE TRACER BULLET")
    print("WO 2026-08-24-021 Decision 2")
    print("=" * 60)
    
    # Phase 1: Run with simulated failure
    print("\n--- Phase 1: Run with simulated failure at Tier A ---")
    record = run_pipeline(
        shot_id="tracer-bullet-001",
        description="Market establishing shot — wide angle, morning light",
        output_path=output_path,
        record_path=record_path,
        simulate_failure=True,
    )
    
    # Verify failure was recorded
    assert record.status == ShotStatus.FAILED, f"Expected FAILED, got {record.status.value}"
    assert record.current_state == ShotState.TIER_A, f"Expected TIER_A, got {record.current_state.value}"
    assert record.retry_count == 1, f"Expected retry_count=1, got {record.retry_count}"
    assert len(record.error_log) == 1, f"Expected 1 error, got {len(record.error_log)}"
    print("\n[verify] Failure correctly recorded at Tier A")
    print(f"[verify] State: {record.current_state.value}")
    print(f"[verify] Status: {record.status.value}")
    print(f"[verify] Retry count: {record.retry_count}")
    
    # Phase 2: Resume from failure
    print("\n--- Phase 2: Resume from Tier A (no failure) ---")
    record = resume_from_state(record, simulate_failure=False)
    save_shot_record(record, record_path)
    
    # Verify resume succeeded
    assert record.status == ShotStatus.IN_PROGRESS, f"Expected IN_PROGRESS, got {record.status.value}"
    assert record.current_state == ShotState.TIER_B, f"Expected TIER_B, got {record.current_state.value}"
    assert record.retry_count == 0, f"Expected retry_count=0, got {record.retry_count}"
    print("\n[verify] Resume from Tier A succeeded")
    print(f"[verify] State: {record.current_state.value}")
    print(f"[verify] Status: {record.status.value}")
    
    # Phase 3: Verify state history
    print("\n--- Phase 3: Verify state history ---")
    print(f"[verify] State transitions recorded: {len(record.state_history)}")
    for i, transition in enumerate(record.state_history):
        print(f"  {i+1}. {transition['from']} -> {transition['to']} ({transition['result']})")
    
    # Phase 4: Verify persistence
    print("\n--- Phase 4: Verify persistence ---")
    loaded_record = load_shot_record(record_path)
    assert loaded_record.current_state == record.current_state, "State mismatch after load"
    assert loaded_record.status == record.status, "Status mismatch after load"
    assert len(loaded_record.state_history) == len(record.state_history), "History mismatch after load"
    print("[verify] Shot record persists correctly across save/load")
    
    # Summary
    print("\n" + "=" * 60)
    print("TRACER BULLET RESULTS")
    print("=" * 60)
    print(f"Shot ID: {record.shot_id}")
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
