# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import create_indexes, ping_db
from app.routes import router as users_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic (sync allowed here)
    if not ping_db():
        print("⚠️ Warning: MongoDB not reachable at startup")
    create_indexes()
    print("Indexes created successfully.")
    
    yield

    print("Shutting down...")

app = FastAPI(
    lifespan=lifespan
)

app.include_router(users_router)
