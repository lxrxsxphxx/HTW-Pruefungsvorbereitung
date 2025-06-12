from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from app.routers import cards
from app.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tabels
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(cards.router)
