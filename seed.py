"""
seed.py  -  Module 4 owns this. Run once:  python seed.py
Creates demo users, departments, complaints and feedback.
WARNING: it overwrites everything in data/. Add more sample rows to make it look real.
All demo accounts use the password:  studesk123
"""
from utils.auth_utils import hash_password
from utils.storage import write_json

PW = hash_password("studesk123")

departments = [
    {"id": "hostel",    "name": "Hostel",      "description": "Rooms, mess, warden issues"},
    {"id": "exam",      "name": "Examination", "description": "Results, hall tickets, revaluation"},
    {"id": "fees",      "name": "Fees",        "description": "Payments, receipts, scholarships"},
    {"id": "library",   "name": "Library",     "description": "Books, journals, reading rooms"},
    {"id": "it",        "name": "IT Services", "description": "Wi-Fi, labs, student portal"},
    {"id": "academics", "name": "Academics",   "description": "Classes, timetable, faculty"},
]

users = [{"id": "u1", "name": "Admin", "email": "admin@college.edu", "password_hash": PW, "role": "admin", "department": None}]
for i, d in enumerate(departments, start=2):
    users.append({"id": f"u{i}", "name": f"{d['name']} Staff", "email": f"{d['id']}@college.edu",
                  "password_hash": PW, "role": "staff", "department": d["id"]})
users += [
    {"id": "u8", "name": "Asha Rao", "email": "asha@college.edu", "password_hash": PW, "role": "student", "department": None},
    {"id": "u9", "name": "Ravi Kumar", "email": "ravi@college.edu", "password_hash": PW, "role": "student", "department": None},
]


def complaint(n, user, title, desc, dept, status, day, predicted=None, replies=None):
    return {"id": f"c{n}", "user_id": user, "title": title, "description": desc,
            "predicted_department": predicted or dept, "department": dept, "confidence": 0.85,
            "status": status, "priority": "normal",
            "created_at": f"2026-10-{day:02d}T10:00:00", "updated_at": f"2026-10-{day:02d}T10:00:00",
            "responses": replies or []}


complaints = [
    complaint(1, "u8", "Wi-Fi not working in Block B", "No internet since Monday in rooms 201 to 220.", "it", "in_progress", 6,
              replies=[{"by": "u6", "message": "Technician assigned.", "at": "2026-10-07T10:30:00"}]),
    complaint(2, "u9", "Hall ticket shows wrong subject", "My hall ticket lists a subject I did not register for.", "exam", "pending", 7),
    complaint(3, "u8", "Mess food served cold", "Dinner has been cold for the whole week.", "hostel", "resolved", 3),
    complaint(4, "u9", "Fee receipt not generated", "I paid the fee online but the receipt is missing.", "fees", "pending", 8),
    complaint(5, "u8", "Library books missing from shelf", "Operating Systems textbooks are never available.", "library", "pending", 9,
              predicted="academics"),
]

feedback = [
    {"id": "f1", "user_id": "u8", "anonymous": False, "type": "suggestion", "category": "library",
     "title": "Extend library hours during exams", "message": "Please keep the library open until 10 PM in exam weeks.",
     "rating": None, "status": "new", "admin_reply": None, "created_at": "2026-10-08T11:20:00", "updated_at": "2026-10-08T11:20:00"},
    {"id": "f2", "user_id": "u9", "anonymous": True, "type": "feedback", "category": "canteen",
     "title": "Food quality has improved", "message": "The new menu is much better. Thank you!",
     "rating": 5, "status": "reviewed", "admin_reply": "Thanks, we've shared this with the canteen team.",
     "created_at": "2026-10-07T13:05:00", "updated_at": "2026-10-08T09:00:00"},
]

for name, data in [("users.json", users), ("departments.json", departments),
                   ("complaints.json", complaints), ("feedback.json", feedback)]:
    write_json(name, data)
print("Done. Demo logins (password studesk123): admin@college.edu, it@college.edu, asha@college.edu")
