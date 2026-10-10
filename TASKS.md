# StuDesk: task checklist per member

Tick boxes as you go. Screenshot your ticks and commits as evidence for the team coordination marks.

## Everyone: shared setup (Days 1-2)
- [ ] One person creates the GitHub repo, adds everyone, makes branches `m1`, `m2`, `m3`, `m4`
- [ ] Everyone runs the starter and logs in with the demo accounts
- [ ] Read `style.css` and `common.js` together (30 min). Agree not to change tokens without telling the team
- [ ] Set up a task board (GitHub Projects or Trello) with these checklists as cards
- [ ] Fix meeting days; one person writes notes each time (date, who came, decisions)
- [ ] Ask maam: will members with 3 pages be marked on the whole module or on 2 chosen pages?

---

## Module 1: Entry, Auth, Feedback form
Pages: `index.html`, `login.html`, `feedback.html`
- [x] Starter home and login exist. Now make them yours
- [ ] Home: improve copy, add 2-3 more FAQs, check on a phone
- [ ] Login: clear errors; test wrong password, duplicate email, short password
- [ ] `feedback.html`: type toggle, category select, star rating from radio buttons in a `fieldset` with `legend`, anonymous checkbox, character counter (`aria-live`)
- [ ] "My submissions" list from `GET /api/feedback/mine` with status badge and admin reply; empty state
- [ ] Test `/api/register`, `/api/login`, `/api/feedback` in `/docs`
- [ ] Lighthouse and WAVE on your 3 pages, save screenshots
- [ ] Report section: your pages, screenshots, how login and tokens work

## Module 2: Student complaint flow
Pages: `submit.html`, `my-complaints.html`
- [ ] Connect your model in `model/predictor.py` (set `MODEL_URL`, fix the `ADJUST` lines)
- [ ] `submit.html`: title, description, "Suggest department" button calling `/api/predict`, result shown in a select the student can override, success message
- [ ] Validate (empty, too short) with error text linked to the field
- [ ] `my-complaints.html`: `GET /api/complaints/mine`, status badges, filter by status, link each row to `complaint-detail.html?id=c1`
- [ ] Use `stack-table` so the list becomes cards on phones
- [ ] Empty state with a button to submit a complaint
- [ ] Lighthouse and WAVE screenshots
- [ ] Report section: how the model fits in, screenshots

## Module 3: Department staff workspace
Pages: `staff-dashboard.html`, `complaint-detail.html`
- [ ] In `routers/staff.py` add: `PATCH .../status`, `POST .../respond`, `PATCH .../reroute` (copy the `department_complaints` pattern; check the complaint belongs to the staff member's department)
- [ ] `staff-dashboard.html`: table from `GET /api/complaints/department`, filter by status, search by title, pending count
- [ ] `complaint-detail.html?id=...`: full details and reply timeline
- [ ] Staff controls: status select, reply box, re-route select; `showToast()` after each action
- [ ] Students can open the same page to read replies but must not see staff controls (check `getUser().role`)
- [ ] Works at 320px width
- [ ] Lighthouse and WAVE screenshots
- [ ] Report section: status workflow diagram and screenshots

## Module 4: Admin, analytics, data
Pages: `admin-dashboard.html`, `admin-feedback.html`, `admin-manage.html`
- [ ] Extend `seed.py` to 15-20 complaints and 10 feedback entries (varied dates and statuses)
- [ ] Dashboard: stat cards from `GET /api/admin/stats`; chart by department (CSS bars first). Add a text table for screen readers
- [ ] Implement `GET /api/admin/feedback` (filters) and `PATCH /api/admin/feedback/{id}`; hide the name when `anonymous` is true
- [ ] `admin-feedback.html`: filters, list, reply box, status change
- [ ] Users and departments endpoints, plus `admin-manage.html` with add/delete and a confirm step before delete
- [ ] Optional: model accuracy card (`predicted_department == department`)
- [ ] Lighthouse and WAVE screenshots
- [ ] Report section: data files, schema, privacy handling of anonymous feedback

---

## Timeline
| Days | Goal |
|---|---|
| 1-2 | Shared setup, everyone runs the starter |
| 3-7 | Build your pages; test endpoints in `/docs` first |
| 8-9 | Join everything: navbar links, roles, real data, model connected |
| 10 | Test every page on a real phone; fix responsive and accessibility issues |
| 11-12 | Report and viva practice |
| Last day | Freeze code; full demo as student, staff, admin |

## Viva practice (each person, out loud)
- [ ] Walk through your page from browser click to JSON file and back
- [ ] Explain one `fetch` call line by line
- [ ] Explain why labels, `aria-live`, `aria-expanded` and the skip link exist
- [ ] Explain your media queries (640px and 960px)
- [ ] Explain how login is checked (token in `sessionStorage`, `Authorization` header)
- [ ] Explain how `/predict` is called and what happens if the model is down
