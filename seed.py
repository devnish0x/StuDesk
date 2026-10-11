"""
seed.py  -  Module 4 owns this. Run once:  python seed.py
Creates demo users, departments, complaints and feedback.
WARNING: it overwrites everything in data/.
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
    {"id": "u8",  "name": "Asha Rao",   "email": "asha@college.edu",  "password_hash": PW, "role": "student", "department": None},
    {"id": "u9",  "name": "Ravi Kumar", "email": "ravi@college.edu",  "password_hash": PW, "role": "student", "department": None},
    {"id": "u10", "name": "Meera Nair", "email": "meera@college.edu", "password_hash": PW, "role": "student", "department": None},
]


def complaint(n, user, title, description, dept, status, day, predicted=None, responses=None):
    date = f"2026-10-{day:02d}T10:00:00"
    return {"id": f"c{n}", "user_id": user, "title": title, "description": description,
            "predicted_department": predicted or dept, "department": dept, "confidence": 0.85,
            "status": status, "priority": "normal", "created_at": date, "updated_at": date,
            "responses": responses or []}


complaints = [
    complaint(1, "u8", "Wi-Fi not working in Block B", "No internet since Monday in rooms 201 to 220. We cannot attend online classes.", "it", "in_progress", 2,
              responses=[{"by": "IT Services Staff", "message": "A technician has been assigned. Expect a fix by Friday.", "at": "2026-10-03T10:30:00"}]),
    complaint(2, "u9", "Hall ticket shows wrong subject", "My hall ticket lists a subject I did not register for this semester.", "exam", "pending", 3),
    complaint(3, "u8", "Mess food served cold", "Dinner has been served cold for the whole week in the boys hostel mess.", "hostel", "resolved", 1,
              responses=[{"by": "Hostel Staff", "message": "The warden spoke to the mess contractor. Hot food from tomorrow.", "at": "2026-10-02T09:00:00"}]),
    complaint(4, "u10", "Fee receipt not generated", "I paid the semester fee online but the receipt is not available on the portal.", "fees", "pending", 4),
    complaint(5, "u8", "Library books always missing", "Operating Systems textbooks are never on the shelf. Please buy more copies.", "library", "pending", 5, predicted="academics"),
    complaint(6, "u9", "Projector broken in room 305", "The projector in room 305 has not worked for two weeks.", "academics", "in_progress", 5,
              responses=[{"by": "Academics Staff", "message": "Maintenance has been informed.", "at": "2026-10-06T11:00:00"}]),
    complaint(7, "u10", "Student portal login error", "The student portal says invalid password even after a reset.", "it", "pending", 6),
    complaint(8, "u8", "Water cooler not working", "The water cooler on the second floor of the hostel stopped working.", "hostel", "pending", 6),
    complaint(9, "u9", "Revaluation result delayed", "I applied for revaluation two months ago and have no update.", "exam", "in_progress", 7, predicted="academics"),
    complaint(10, "u10", "Scholarship amount not credited", "My scholarship for this semester has not been credited yet.", "fees", "resolved", 1),
    complaint(11, "u8", "Reading room too noisy", "Students talk loudly in the library reading room during exam week.", "library", "resolved", 2),
    complaint(12, "u9", "Lab computers very slow", "Computers in lab 2 take ten minutes to start.", "it", "pending", 8),
]


def feedback(n, user, kind, category, title, message, rating, status, reply, anonymous, day):
    date = f"2026-10-{day:02d}T12:00:00"
    return {"id": f"f{n}", "user_id": user, "anonymous": anonymous, "type": kind, "category": category,
            "title": title, "message": message, "rating": rating, "status": status, "admin_reply": reply,
            "created_at": date, "updated_at": date}


feedback_list = [
    feedback(1, "u8", "suggestion", "library", "Extend library hours during exams", "Please keep the library open until 10 PM in exam weeks.", None, "new", None, False, 4),
    feedback(2, "u9", "feedback", "canteen", "Food quality has improved", "The new canteen menu is much better. Thank you!", 5, "reviewed", "Thanks, we have shared this with the canteen team.", True, 3),
    feedback(3, "u10", "suggestion", "hostel", "Add more charging points", "Rooms have only one socket for four students.", None, "implemented", "Extra sockets were installed in Block A.", False, 2),
    feedback(4, "u8", "feedback", "academics", "Great lecture series", "The guest lectures this month were very useful.", 5, "new", None, False, 6),
    feedback(5, "u9", "feedback", "hostel", "Laundry service is slow", "Clothes take five days to come back.", 2, "new", None, True, 7),
    feedback(6, "u10", "suggestion", "other", "Start a placement notice board", "A single board for company visits and deadlines would help a lot.", None, "reviewed", "Good idea, we will add this to the portal.", False, 7),
]

write_json("users.json", users)
write_json("departments.json", departments)
write_json("complaints.json", complaints)
write_json("feedback.json", feedback_list)
print("Done. Demo logins (password studesk123): admin@college.edu, it@college.edu, asha@college.edu")
