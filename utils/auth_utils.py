"""
auth_utils.py  -  shared. Owned by Module 1.
Password hashing, login tokens, and "who is calling?" checks.
"""
import hashlib
import hmac
import secrets

from fastapi import Depends, Header, HTTPException

from utils.storage import read_json

# token -> user id. Lives in memory, so restarting the server logs everyone out.
# (Fine for a mini project. Mention it in the report as future scope.)
TOKENS = {}


def hash_password(password, salt=None):
    """Returns 'salt$hash'. We never store the real password."""
    salt = salt or secrets.token_hex(8)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()
    return f"{salt}${digest}"


def verify_password(password, stored):
    salt, _ = stored.split("$")
    return hmac.compare_digest(hash_password(password, salt), stored)


def create_token(user_id):
    token = secrets.token_urlsafe(24)
    TOKENS[token] = user_id
    return token


def public_user(user):
    """User info that is safe to send to the browser (no password)."""
    return {k: user[k] for k in ("id", "name", "email", "role", "department")}


def get_current_user(authorization: str = Header(default="")):
    """Use as:  user = Depends(get_current_user)  - rejects anyone not logged in."""
    token = authorization.replace("Bearer ", "").strip()
    user_id = TOKENS.get(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Please log in first.")
    for user in read_json("users.json"):
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=401, detail="Account not found.")


def require_role(*roles):
    """Use as:  user = Depends(require_role('staff'))  - only these roles allowed."""
    def checker(user=Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="You don't have access to this.")
        return user
    return checker
