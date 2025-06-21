from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import asyncpg

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Async connection pool
@app.on_event("startup")
async def startup():
    app.state.db_pool = await asyncpg.create_pool(
        user="postgres",
        password="1212",
        database="postgres",
        host="localhost",
        port=5432
    )

@app.on_event("shutdown")
async def shutdown():
    await app.state.db_pool.close()

# ROUTES

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/fat", response_class=HTMLResponse)
async def read_fat(request: Request):
    return templates.TemplateResponse("fat.html", {"request": request})

@app.get("/form", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.get("/iss-location", response_class=HTMLResponse)
async def get_iss_location():
    res = requests.get("http://api.open-notify.org/iss-now.json")
    data = res.json()
    pos = data["iss_position"]
    return f"<div>Latitude: {pos['latitude']}, Longitude: {pos['longitude']}</div>"

@app.get("/db-test")
async def test_db():
    async with app.state.db_pool.acquire() as conn:
        now = await conn.fetchval("SELECT NOW()")
        return {"now": str(now)}

@app.post("/learners", response_class=HTMLResponse)
async def create_learner(name: str = Form(...)):
    async with app.state.db_pool.acquire() as conn:
        new_id = await conn.fetchval(
            "INSERT INTO learners (name) VALUES ($1) RETURNING id;", name
        )
    return f"<p>✅ Learner added with ID {new_id} and name: {name}</p>"
