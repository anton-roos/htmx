from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("sandbox/index.html", {"request": request})

@router.get("/form", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("sandbox/form.html", {"request": request})

@router.get("/iss-location", response_class=HTMLResponse)
async def get_iss_location():
    res = requests.get("http://api.open-notify.org/iss-now.json")
    data = res.json()
    pos = data["iss_position"]
    return f"<div>Latitude: {pos['latitude']}, Longitude: {pos['longitude']}</div>"

@router.post("/learners", response_class=HTMLResponse)
async def create_learner(request: Request, name: str = Form(...)):
    async with request.app.state.db_pool.acquire() as conn:
        new_id = await conn.fetchval(
            "INSERT INTO learners (name) VALUES ($1) RETURNING id;", name
        )
    return f"<p>✅ Learner added with ID {new_id} and name: {name}</p>"
