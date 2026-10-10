"""
staff.py  -  Module 3.   The department staff workspace.

NOTE: main.py includes this router BEFORE complaints.py. That matters:
/api/complaints/department must be matched before /api/complaints/{id},
otherwise FastAPI thinks "department" is a complaint id.
"""
from fastapi import APIRouter, Depends, HTTPException

from utils.auth_utils import require_role
from utils.storage import read_json

router = APIRouter(prefix="/api/complaints", tags=["staff"])


@router.get("/department")
def department_complaints(user=Depends(require_role("staff"))):
    """WORKING EXAMPLE: complaints that belong to this staff member's department."""
    mine = [c for c in read_json("complaints.json") if c["department"] == user["department"]]
    return sorted(mine, key=lambda c: c["created_at"], reverse=True)


# ---- TODO (Module 3): copy the pattern above and build these ----
# PATCH /api/complaints/{id}/status    body {"status": "in_progress"}   -> update status + updated_at
# POST  /api/complaints/{id}/respond   body {"message": "..."}          -> append to responses[]
# PATCH /api/complaints/{id}/reroute   body {"department": "it"}        -> change department only
# Hints: read_json -> find the complaint -> change it -> write_json -> return it.
#        Check the complaint belongs to user["department"] before changing it.
#        Reject statuses other than pending / in_progress / resolved.
