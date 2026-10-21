# StuDesk: complaint routing and feedback

## Run it
```
pip install -r requirements.txt
python seed.py                     # demo data (run again any time to reset)
uvicorn main:app --reload
```
Open http://127.0.0.1:8000  (try every API at http://127.0.0.1:8000/docs)

Demo logins, password for all: `studesk123`
| Role | Email |
|---|---|
| Student | asha@college.edu |
| Staff | hostel@, exam@, fees@, library@, it@, academics@ (all @college.edu) |
| Admin | admin@college.edu |

## Folder structure
```
studesk/
├── main.py                 starts the app, plugs in the routers, serves the pages
├── seed.py                 creates the demo data
├── model/predictor.py      predict(text) -> department  (keyword fallback or your model)
├── routers/
│   ├── auth.py             register, login
│   ├── complaints.py       departments, predict, submit, mine, one complaint
│   ├── staff.py            department list, status, respond, reroute
│   ├── feedback.py         send feedback, my feedback
│   └── admin.py            stats, feedback review, users, departments
├── utils/
│   ├── storage.py          read_json(), write_json()
│   └── auth_utils.py       password hashing, tokens, require_role()
├── data/                   users.json, complaints.json, feedback.json, departments.json
├── templates/              the 10 HTML pages
└── static/
    ├── css/common.css      styles for every page (colours, navbar, buttons, forms, tables)
    ├── css/pages/          one CSS file per page
    ├── js/common.js        helpers for every page (api(), checkLogin(), esc() ...)
    └── js/pages/           one JS file per page
```

## The 10 pages (each has its own .css and .js with the same name)
| Page | Who | Backend it uses |
|---|---|---|
| index | everyone | POST /api/predict |
| login | everyone | POST /api/login, /api/register |
| submit | student | GET /api/departments, POST /api/predict, POST /api/complaints |
| my-complaints | student | GET /api/complaints/mine |
| feedback | student | POST /api/feedback, GET /api/feedback/mine |
| staff-dashboard | staff | GET /api/complaints/department |
| complaint-detail | staff, and the student who owns it | GET /api/complaints/{id}, PATCH .../status, POST .../respond, PATCH .../reroute |
| admin-dashboard | admin | GET /api/admin/stats |
| admin-feedback | admin | GET /api/admin/feedback, PATCH /api/admin/feedback/{id} |
| admin-manage | admin | /api/admin/users, /api/admin/departments |

## Every page follows the same 3 steps
1. HTML draws the page (navbar, form, empty table).
2. The page's JS calls the backend with `api("/...")` (this uses `fetch` and sends the token).
3. The JS puts the answer into the page with `innerHTML`.

## Good to know
- Tokens live in memory: restarting the server logs everyone out (the pages send you back to login).
- The token is saved in sessionStorage, so each browser tab has its own login. This makes it easy to test student, staff and admin in different tabs.
- Staff replies store the staff member's name in `by`.
