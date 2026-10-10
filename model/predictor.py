"""
predictor.py  -  Owned by Module 2.
One job: predict(text) -> (department_id, confidence).

HOW TO CONNECT YOUR MODEL
Your model has one endpoint called predict. Set its address in MODEL_URL
below (or as an environment variable). We send {"text": "..."} and expect
something like {"department": "it", "confidence": 0.87} back.
Change the lines marked  >>> ADJUST  to match what your model really returns.

If the model is off or fails, we fall back to simple keywords, so the
website never breaks during the demo.
"""
import json
import os
import urllib.request

MODEL_URL = os.environ.get("MODEL_URL", "http://127.0.0.1:5000/predict")  # >>> ADJUST

KEYWORDS = {
    "hostel":    ["hostel", "room", "mess", "warden", "roommate", "laundry"],
    "exam":      ["exam", "result", "hall ticket", "revaluation", "marks", "grade"],
    "fees":      ["fee", "payment", "scholarship", "refund", "receipt"],
    "library":   ["library", "book", "journal", "reading room"],
    "it":        ["wifi", "wi-fi", "internet", "lab", "computer", "portal", "password"],
    "academics": ["class", "faculty", "timetable", "syllabus", "attendance", "lecture"],
}


def _keyword_guess(text):
    text = text.lower()
    scores = {dept: sum(w in text for w in words) for dept, words in KEYWORDS.items()}
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "academics", 0.0  # default when nothing matches
    return best, 0.5


def predict(text):
    try:
        request = urllib.request.Request(
            MODEL_URL,
            data=json.dumps({"text": text}).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=3) as response:
            result = json.loads(response.read())
        department = result["department"]            # >>> ADJUST key name
        confidence = float(result.get("confidence", 0))  # >>> ADJUST key name
        return department, confidence
    except Exception:
        return _keyword_guess(text)
