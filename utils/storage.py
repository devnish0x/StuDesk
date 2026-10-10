"""
storage.py  -  shared by EVERYONE.
Reads and writes our JSON "database" files in the data/ folder.

Rule: never open the JSON files directly in your router. Always use
read_json() and write_json() so we all handle files the same safe way.
"""
import json
import os
import tempfile
import threading
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
_lock = threading.Lock()  # stops two requests writing at the exact same moment


def read_json(filename):
    """Return the list stored in data/<filename>. Empty list if file is missing."""
    path = DATA_DIR / filename
    if not path.exists():
        return []
    with _lock:
        with open(path, encoding="utf-8") as f:
            return json.load(f)


def write_json(filename, data):
    """Save a list to data/<filename>.
    We write to a temp file first and then rename it, so a crash in the
    middle of writing can never leave a half-written (corrupted) file."""
    path = DATA_DIR / filename
    with _lock:
        fd, tmp_path = tempfile.mkstemp(dir=DATA_DIR, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, path)


def new_id(prefix, items):
    """Make the next id, e.g. new_id('c', complaints) -> 'c7'."""
    numbers = [int(i["id"][len(prefix):]) for i in items
               if i["id"].startswith(prefix) and i["id"][len(prefix):].isdigit()]
    return f"{prefix}{max(numbers, default=0) + 1}"


def now():
    """Current time as text, e.g. '2026-10-10T16:30:00'."""
    return datetime.now().isoformat(timespec="seconds")
