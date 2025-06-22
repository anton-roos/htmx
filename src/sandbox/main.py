from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncpg
import os
from dotenv import load_dotenv
from src.sandbox.routes import router as sandbox_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_pool = await asyncpg.create_pool(DATABASE_URL)
    yield
    await app.state.db_pool.close()

app = FastAPI(lifespan=lifespan)

# Mount static directory for assets like favicon
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(sandbox_router, prefix="")