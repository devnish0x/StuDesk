"""
staff.py  -  Module 3.   The department staff workspace.

NOTE: main.py includes this router BEFORE complaints.py. That matters:
/api/complaints/department must be matched before /api/complaints/{id},
otherwise FastAPI thinks "department" is a complaint id.
"""
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from utils.auth_utils import require_role
from utils.storage import now, read_json, write_json

router = APIRouter(prefix="/api/complaints", tags=["staff"])


class StatusIn(BaseModel):
    status: Literal["pending", "in_progress", "resolved"]


class RespondIn(BaseModel):
    message: str = Field(min_length=2, max_length=1000)


class RerouteIn(BaseModel):
    department: str


def find_own_complaint(complaints, complaint_id, user):
    """Finds a complaint and checks it belongs to this staff member's department."""
    for c in complaints:
        if c["id"] == complaint_id:
            if c["department"] != user["department"]:
                raise HTTPException(403, "This complaint belongs to another department.")
            return c
    raise HTTPException(404, "Complaint not found.")


@router.get("/department")
def department_complaints(user=Depends(require_role("staff"))):
    """Complaints that belong to this staff member's department."""
    mine = [c for c in read_json("complaints.json") if c["department"] == user["department"]]
    return sorted(mine, key=lambda c: c["created_at"], reverse=True)


@router.patch("/{complaint_id}/status")
def update_status(complaint_id: str, data: StatusIn, user=Depends(require_role("staff"))):
    complaints = read_json("complaints.json")
    complaint = find_own_complaint(complaints, complaint_id, user)
    complaint["status"] = data.status
    complaint["updated_at"] = now()
    write_json("complaints.json", complaints)
    return complaint


@router.post("/{complaint_id}/respond")
def respond(complaint_id: str, data: RespondIn, user=Depends(require_role("staff"))):
    complaints = read_json("complaints.json")
    complaint = find_own_complaint(complaints, complaint_id, user)
    complaint["responses"].append({"by": user["name"], "message": data.message.strip(), "at": now()})
    complaint["updated_at"] = now()
    write_json("complaints.json", complaints)
    return complaint


@router.patch("/{complaint_id}/reroute")
def reroute(complaint_id: str, data: RerouteIn, user=Depends(require_role("staff"))):
    if data.department not in [d["id"] for d in read_json("departments.json")]:
        raise HTTPException(400, "That department does not exist.")
    complaints = read_json("complaints.json")
    complaint = find_own_complaint(complaints, complaint_id, user)
    complaint["department"] = data.department     # predicted_department stays as the model said
    complaint["updated_at"] = now()
    write_json("complaints.json", complaints)
    return complaint
