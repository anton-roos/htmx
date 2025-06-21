from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import asyncpg
import os
from dotenv import load_dotenv
from sandbox.routes import router as sandbox_router

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

templates = Jinja2Templates(directory="templates")

# Lifespan for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_pool = await asyncpg.create_pool(DATABASE_URL)
    yield
    await app.state.db_pool.close()

app = FastAPI(lifespan=lifespan)

app.include_router(sandbox_router, prefix="")