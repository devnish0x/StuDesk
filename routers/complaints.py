"""
complaints.py  -  Module 2.   Predict, submit, list my complaints, view one.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from model.predictor import predict
from utils.auth_utils import get_current_user, require_role
from utils.storage import new_id, now, read_json, write_json

router = APIRouter(prefix="/api", tags=["complaints"])


class PredictIn(BaseModel):
    text: str = Field(min_length=3, max_length=2000)


class ComplaintIn(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=10, max_length=2000)
    department: str | None = None   # set only if the student overrides the suggestion


@router.get("/departments")
def list_departments():
    """Public: the dropdowns on the pages need the department names."""
    return read_json("departments.json")


@router.post("/predict")
def predict_department(data: PredictIn):
    """Public on purpose, so the home page can show a live demo."""
    department, confidence = predict(data.text)
    return {"department": department, "confidence": confidence}


@router.post("/complaints")
def submit_complaint(data: ComplaintIn, user=Depends(require_role("student"))):
    predicted, confidence = predict(data.title + ". " + data.description)
    chosen = data.department or predicted
    if chosen not in [d["id"] for d in read_json("departments.json")]:
        raise HTTPException(400, "That department does not exist.")
    complaints = read_json("complaints.json")
    complaint = {
        "id": new_id("c", complaints),
        "user_id": user["id"],
        "title": data.title.strip(),
        "description": data.description.strip(),
        "predicted_department": predicted,
        "department": chosen,
        "confidence": confidence,
        "status": "pending",
        "priority": "normal",
        "created_at": now(),
        "updated_at": now(),
        "responses": [],
    }
    complaints.append(complaint)
    write_json("complaints.json", complaints)
    return complaint


@router.get("/complaints/mine")
def my_complaints(user=Depends(require_role("student"))):
    mine = [c for c in read_json("complaints.json") if c["user_id"] == user["id"]]
    return sorted(mine, key=lambda c: c["created_at"], reverse=True)


@router.get("/complaints/{complaint_id}")
def get_complaint(complaint_id: str, user=Depends(get_current_user)):
    for c in read_json("complaints.json"):
        if c["id"] == complaint_id:
            allowed = (user["role"] == "admin"
                       or c["user_id"] == user["id"]
                       or (user["role"] == "staff" and user["department"] == c["department"]))
            if not allowed:
                raise HTTPException(403, "You can't view this complaint.")
            return c
    raise HTTPException(404, "Complaint not found.")
