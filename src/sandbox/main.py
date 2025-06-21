from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncpg
import os
from dotenv import load_dotenv
from src.sandbox.routes import router as sandbox_router

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_pool = await asyncpg.create_pool(DATABASE_URL)
    yield
    await app.state.db_pool.close()

app = FastAPI(lifespan=lifespan)

app.include_router(sandbox_router, prefix="")