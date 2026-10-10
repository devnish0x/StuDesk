"""
admin.py  -  Module 4.   Stats, feedback review, users, departments.
"""
from fastapi import APIRouter, Depends

from utils.auth_utils import require_role
from utils.storage import read_json

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats")
def stats(user=Depends(require_role("admin"))):
    """WORKING EXAMPLE: simple counts for the dashboard."""
    complaints = read_json("complaints.json")
    feedback = read_json("feedback.json")
    by_status, by_department = {}, {}
    for c in complaints:
        by_status[c["status"]] = by_status.get(c["status"], 0) + 1
        by_department[c["department"]] = by_department.get(c["department"], 0) + 1
    ratings = [f["rating"] for f in feedback if f["rating"]]
    return {
        "total_complaints": len(complaints),
        "by_status": by_status,
        "by_department": by_department,
        "total_feedback": len(feedback),
        "average_rating": round(sum(ratings) / len(ratings), 1) if ratings else None,
    }


# ---- TODO (Module 4) ----
# GET   /api/admin/feedback          filter by ?type= &category= &status=
#                                    IMPORTANT: if "anonymous" is true, do NOT send the student's name.
# PATCH /api/admin/feedback/{id}     body {"status": "reviewed", "admin_reply": "..."}
# GET / POST / DELETE /api/admin/users
# GET / POST / DELETE /api/admin/departments
# Optional: model accuracy = share of complaints where predicted_department == department.
