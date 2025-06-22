from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
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

@router.get("/location", response_class=HTMLResponse)
async def location(request: Request):
    # Fetch current ISS position
    res = requests.get("http://api.open-notify.org/iss-now.json")
    data = res.json()["iss_position"]
    lat = float(data["latitude"])
    lng = float(data["longitude"])
    return templates.TemplateResponse(
        "sandbox/location.html",
        {"request": request, "lat": lat, "lng": lng},
    )

@router.get("/location-data")
async def location_data():
    res = requests.get("http://api.open-notify.org/iss-now.json")
    return JSONResponse(res.json())

@router.post("/learners", response_class=HTMLResponse)
async def create_learner(request: Request, name: str = Form(...)):
    async with request.app.state.db_pool.acquire() as conn:
        new_id = await conn.fetchval(
            "INSERT INTO learners (name) VALUES ($1) RETURNING id;", name
        )
    return f"<p>✅ Learner added with ID {new_id} and name: {name}</p>"
