"""
admin.py  -  Module 4.   Stats, feedback review, users, departments.
Every endpoint here is admin-only.
"""
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from utils.auth_utils import hash_password, public_user, require_role
from utils.storage import new_id, now, read_json, write_json

router = APIRouter(prefix="/api/admin", tags=["admin"])


class FeedbackReviewIn(BaseModel):
    status: Literal["new", "reviewed", "implemented"] | None = None
    admin_reply: str | None = Field(default=None, max_length=1000)


class StaffIn(BaseModel):
    name: str = Field(min_length=2, max_length=60)
    email: str
    password: str = Field(min_length=6, max_length=100)
    department: str


class DepartmentIn(BaseModel):
    name: str = Field(min_length=2, max_length=40)
    description: str = Field(default="", max_length=120)


# ----------------------------------------------------------------- stats
@router.get("/stats")
def stats(user=Depends(require_role("admin"))):
    complaints = read_json("complaints.json")
    feedback = read_json("feedback.json")
    by_status, by_department = {}, {}
    correct = 0
    for c in complaints:
        by_status[c["status"]] = by_status.get(c["status"], 0) + 1
        by_department[c["department"]] = by_department.get(c["department"], 0) + 1
        if c["predicted_department"] == c["department"]:
            correct += 1
    ratings = [f["rating"] for f in feedback if f["rating"]]
    return {
        "total_complaints": len(complaints),
        "by_status": by_status,
        "by_department": by_department,
        "total_feedback": len(feedback),
        "average_rating": round(sum(ratings) / len(ratings), 1) if ratings else None,
        "model_accuracy": round(100 * correct / len(complaints)) if complaints else None,
    }


# -------------------------------------------------------------- feedback
@router.get("/feedback")
def list_feedback(type: str | None = None, category: str | None = None, status: str | None = None,
                  user=Depends(require_role("admin"))):
    users = read_json("users.json")
    result = []
    for f in read_json("feedback.json"):
        if type and f["type"] != type:
            continue
        if category and f["category"] != category:
            continue
        if status and f["status"] != status:
            continue
        item = dict(f)
        author = next((u["name"] for u in users if u["id"] == f["user_id"]), "Unknown")
        item["from_name"] = "Anonymous" if f["anonymous"] else author
        del item["user_id"]          # anonymous means anonymous: never send the id
        result.append(item)
    return sorted(result, key=lambda f: f["created_at"], reverse=True)


@router.patch("/feedback/{feedback_id}")
def review_feedback(feedback_id: str, data: FeedbackReviewIn, user=Depends(require_role("admin"))):
    items = read_json("feedback.json")
    for f in items:
        if f["id"] == feedback_id:
            if data.status:
                f["status"] = data.status
            if data.admin_reply is not None and data.admin_reply.strip():
                f["admin_reply"] = data.admin_reply.strip()
            f["updated_at"] = now()
            write_json("feedback.json", items)
            return f
    raise HTTPException(404, "Feedback not found.")


# ----------------------------------------------------------------- users
@router.get("/users")
def list_users(user=Depends(require_role("admin"))):
    return [public_user(u) for u in read_json("users.json")]


@router.post("/users")
def add_staff(data: StaffIn, user=Depends(require_role("admin"))):
    if "@" not in data.email:
        raise HTTPException(400, "Enter a valid email address.")
    if data.department not in [d["id"] for d in read_json("departments.json")]:
        raise HTTPException(400, "Choose a department.")
    users = read_json("users.json")
    if any(u["email"].lower() == data.email.lower() for u in users):
        raise HTTPException(400, "This email is already registered.")
    staff = {
        "id": new_id("u", users),
        "name": data.name.strip(),
        "email": data.email.lower(),
        "password_hash": hash_password(data.password),
        "role": "staff",
        "department": data.department,
    }
    users.append(staff)
    write_json("users.json", users)
    return public_user(staff)


@router.delete("/users/{user_id}")
def delete_user(user_id: str, user=Depends(require_role("admin"))):
    if user_id == user["id"]:
        raise HTTPException(400, "You cannot delete your own account.")
    users = read_json("users.json")
    remaining = [u for u in users if u["id"] != user_id]
    if len(remaining) == len(users):
        raise HTTPException(404, "User not found.")
    write_json("users.json", remaining)
    return {"deleted": user_id}


# ----------------------------------------------------------- departments
@router.get("/departments")
def list_departments(user=Depends(require_role("admin"))):
    return read_json("departments.json")


@router.post("/departments")
def add_department(data: DepartmentIn, user=Depends(require_role("admin"))):
    departments = read_json("departments.json")
    dept_id = data.name.strip().lower().replace(" ", "_")
    if any(d["id"] == dept_id for d in departments):
        raise HTTPException(400, "This department already exists.")
    department = {"id": dept_id, "name": data.name.strip(), "description": data.description.strip()}
    departments.append(department)
    write_json("departments.json", departments)
    return department


@router.delete("/departments/{dept_id}")
def delete_department(dept_id: str, user=Depends(require_role("admin"))):
    if any(c["department"] == dept_id for c in read_json("complaints.json")):
        raise HTTPException(400, "This department still has complaints, so it cannot be deleted.")
    departments = read_json("departments.json")
    remaining = [d for d in departments if d["id"] != dept_id]
    if len(remaining) == len(departments):
        raise HTTPException(404, "Department not found.")
    write_json("departments.json", remaining)
    return {"deleted": dept_id}
