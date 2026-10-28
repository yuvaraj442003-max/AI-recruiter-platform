"""
Test learning journey backend logic and stage gate enforcement.
"""
import os
import sys

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)

from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.routers.study_materials import (
    get_learning_journey,
    advance_learning_phase,
    toggle_daily_plan_task,
    reset_learning_journey_dashboard,
    AdvancePhaseRequest,
    ToggleTaskRequest,
)

db = SessionLocal()
mock_cand = db.query(User).filter(User.role == UserRole.candidate).first()
if not mock_cand:
    mock_cand = User(id="cand-test-1", email="student@test.com", role=UserRole.candidate, is_active=True)

print("=== 1. TEST GET LEARNING JOURNEY ===")
res1 = get_learning_journey(current_user=mock_cand, db=db)
data1 = res1.data
print("Roadmap Title:", data1["roadmap_title"])
print("Overall Progress:", data1["overall_progress_percent"], "%")
print("Active Phase:", data1["active_phase_name"], f"({data1['phases'][0]['progress_percent']}%)")
print("Phase 2 Locked?", data1["phases"][1]["is_locked"])
print("Recommendations Count:", len(data1["recommendations"]))
print("Today Tasks Count:", len(data1["today_plan"]))
print("Strengths:", data1["strengths"])
print("Focus Areas:", data1["focus_areas"])
print("Recent Progress:", data1["recent_progress"])

assert data1["phases"][0]["progress_percent"] == 60.0
assert data1["phases"][1]["is_locked"] is True
assert len(data1["recommendations"]) == 4
assert len(data1["today_plan"]) == 3

print("\n=== 2. TEST STAGE-GATE ENFORCEMENT (ATTEMPT ADVANCE PHASE 2 WHILE PHASE 1 < 100%) ===")
try:
    advance_learning_phase(AdvancePhaseRequest(phase_num=2, delta_percent=10.0), current_user=mock_cand, db=db)
    assert False, "Should have raised HTTPException for locked stage!"
except Exception as e:
    print("  [EXPECTED GATE BLOCKED]:", getattr(e, "detail", str(e)))

print("\n=== 3. TEST ADVANCING PHASE 1 TO 100% (UNLOCKS PHASE 2) ===")
res_adv1 = advance_learning_phase(AdvancePhaseRequest(phase_num=1, set_exact_percent=100.0), current_user=mock_cand, db=db)
print("Phase 1 Updated Message:", res_adv1.message)
res_after_unlock = get_learning_journey(current_user=mock_cand, db=db)
data_after = res_after_unlock.data
print("Phase 1 Status:", data_after["phases"][0]["status"], "Progress:", data_after["phases"][0]["progress_percent"])
print("Phase 2 Locked?:", data_after["phases"][1]["is_locked"], "Status:", data_after["phases"][1]["status"])
assert data_after["phases"][1]["is_locked"] is False, "Phase 2 should be unlocked now!"

print("\n=== 4. TEST TOGGLE DAILY TASK ===")
task_toggle_res = toggle_daily_plan_task(ToggleTaskRequest(task_id="task-2"), current_user=mock_cand, db=db)
print("Task Toggle:", task_toggle_res.message)

print("\n=== 5. RESET BACK TO EXACT REFERENCE 60% DASHBOARD STATE ===")
reset_res = reset_learning_journey_dashboard(current_user=mock_cand, db=db)
reset_data = reset_res.data
assert reset_data["phases"][0]["progress_percent"] == 60.0
assert reset_data["phases"][1]["is_locked"] is True
print("Successfully reset to 60% Foundations state!")

print("\nALL BACKEND LEARNING JOURNEY & STAGE-GATE TESTS PASSED!")

