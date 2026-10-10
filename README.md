# StuDesk: complaint routing and feedback

## Run it (first time)
```
pip install -r requirements.txt
python seed.py                   # creates demo data (password for all demo users: studesk123)
uvicorn main:app --reload
```
Open http://127.0.0.1:8000  (try the API at http://127.0.0.1:8000/docs)

## Connect the ML model
Edit `MODEL_URL` in `model/predictor.py` and the two lines marked `>>> ADJUST`.
If the model is off, a keyword fallback is used so the site still works.

## Demo logins
| Role | Email |
|---|---|
| Student | asha@college.edu |
| Staff (IT) | it@college.edu (also hostel@, exam@, fees@, library@, academics@) |
| Admin | admin@college.edu |

## Who owns what
| Module | Pages | Backend |
|---|---|---|
| M1 | index, login, feedback | routers/auth.py, routers/feedback.py, utils/auth_utils.py |
| M2 | submit, my-complaints | routers/complaints.py, model/predictor.py |
| M3 | staff-dashboard, complaint-detail | routers/staff.py |
| M4 | admin-dashboard, admin-feedback, admin-manage | routers/admin.py, utils/storage.py, seed.py |

## Rules for everyone
1. Start every new page from `templates/page_template.html`.
2. Use only the colours and classes in `static/css/style.css`. Page-only CSS goes in `static/css/pages/`.
3. Call the backend only through `api()` in `common.js`.
4. Read/write data only through `read_json()` / `write_json()`.
5. Work on your own branch. Open a pull request, and at least one teammate reviews it.
6. Escape any user text you insert with `innerHTML` using `escapeHtml()`.
