"""
This file connects the different endoints to a single application
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from app.routers import cards
from app.routers import questions
from app.routers import learning_sets
from app.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tabels
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

app.include_router(cards.router)
app.include_router(questions.router)
app.include_router(learning_sets.router)
