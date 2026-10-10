"""
feedback.py  -  Module 1.   Students send feedback or suggestions.
"""
from typing import Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from utils.auth_utils import require_role
from utils.storage import new_id, now, read_json, write_json

router = APIRouter(prefix="/api", tags=["feedback"])


class FeedbackIn(BaseModel):
    type: Literal["feedback", "suggestion"]
    category: Literal["hostel", "library", "academics", "canteen", "other"]
    title: str = Field(min_length=3, max_length=120)
    message: str = Field(min_length=10, max_length=1500)
    rating: int | None = Field(default=None, ge=1, le=5)
    anonymous: bool = False


@router.post("/feedback")
def submit_feedback(data: FeedbackIn, user=Depends(require_role("student"))):
    items = read_json("feedback.json")
    item = {
        "id": new_id("f", items),
        "user_id": user["id"],      # stored even if anonymous, so "My submissions" works
        "anonymous": data.anonymous,
        "type": data.type,
        "category": data.category,
        "title": data.title.strip(),
        "message": data.message.strip(),
        "rating": data.rating if data.type == "feedback" else None,
        "status": "new",
        "admin_reply": None,
        "created_at": now(),
        "updated_at": now(),
    }
    items.append(item)
    write_json("feedback.json", items)
    return item


@router.get("/feedback/mine")
def my_feedback(user=Depends(require_role("student"))):
    mine = [f for f in read_json("feedback.json") if f["user_id"] == user["id"]]
    return sorted(mine, key=lambda f: f["created_at"], reverse=True)
