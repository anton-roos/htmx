from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import psycopg

app = FastAPI()

conn_info = "postgresql://postgres:1212@localhost:5432/postgres"
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/fat", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("fat.html", {"request": request})

@app.get("/form", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.get("/iss-location", response_class=HTMLResponse)
def get_iss_location():
    res = requests.get("http://api.open-notify.org/iss-now.json")
    data = res.json()
    pos = data["iss_position"]
    return f"<div>Latitude: {pos['latitude']}, Longitude: {pos['longitude']}</div>"

@app.get("/db-test")
def test_db():
    with psycopg.connect(conn_info) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT NOW()")
            result = cur.fetchone()
            return {"now": result[0].isoformat()}

@app.post("/learners", response_class=HTMLResponse)
def create_learner(name: str = Form(...)):
    with psycopg.connect(conn_info) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO learners (name) VALUES (%s) RETURNING id;", (name,))
            new_id = cur.fetchone()[0]
    return f"<p>✅ Learner added with ID {new_id} and name: {name}</p>"