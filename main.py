"""
main.py  -  the front door of StuDesk.
Run with:   uvicorn main:app --reload
Then open:  http://127.0.0.1:8000        (API tester: http://127.0.0.1:8000/docs)
"""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from routers import admin, auth, complaints, feedback, staff

BASE = Path(__file__).parent
app = FastAPI(title="StuDesk")

# staff BEFORE complaints (see note inside routers/staff.py)
for module in (auth, staff, complaints, feedback, admin):
    app.include_router(module.router)

app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")


# ---- Pages: /login.html opens templates/login.html, and "/" opens index.html ----
@app.get("/", include_in_schema=False)
def home():
    return FileResponse(BASE / "templates" / "index.html")


@app.get("/{page}.html", include_in_schema=False)
def page(page: str):
    path = BASE / "templates" / f"{page}.html"
    if not path.is_file():
        raise HTTPException(404, "Page not found")
    return FileResponse(path)
