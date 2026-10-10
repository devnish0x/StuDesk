"""
auth.py  -  Module 1.   Register, login, "who am I".
"""
import re

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from utils.auth_utils import (create_token, get_current_user, hash_password,
                              public_user, verify_password)
from utils.storage import new_id, read_json, write_json

router = APIRouter(prefix="/api", tags=["auth"])


class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=60)
    email: str
    password: str = Field(min_length=6, max_length=100)


class LoginIn(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(data: RegisterIn):
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", data.email):
        raise HTTPException(400, "Enter a valid email address.")
    users = read_json("users.json")
    if any(u["email"].lower() == data.email.lower() for u in users):
        raise HTTPException(400, "This email is already registered.")
    user = {
        "id": new_id("u", users),
        "name": data.name.strip(),
        "email": data.email.lower(),
        "password_hash": hash_password(data.password),
        "role": "student",          # only students can self-register
        "department": None,
    }
    users.append(user)
    write_json("users.json", users)
    return {"token": create_token(user["id"]), "user": public_user(user)}


@router.post("/login")
def login(data: LoginIn):
    for user in read_json("users.json"):
        if user["email"] == data.email.lower() and verify_password(data.password, user["password_hash"]):
            return {"token": create_token(user["id"]), "user": public_user(user)}
    raise HTTPException(401, "Email or password is incorrect.")


@router.get("/me")
def me(user=Depends(get_current_user)):
    return public_user(user)
