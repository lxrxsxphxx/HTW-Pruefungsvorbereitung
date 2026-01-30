"""
This file connects the different endoints to a single application
"""

from contextlib import asynccontextmanager
import secrets
import bcrypt
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, select

from app.routers import cards, questions, learning_sets, modules, courses, users
from app.models import User, Course,Module,CourseModule
from app.database import engine
from app.dependencies import write_starting_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    SQLModel.metadata.create_all(engine)

    # Generate random key for jwt creation later on

    app.state.jwt_key = secrets.token_urlsafe()

    write_starting_data(Session(engine))
    
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
app.include_router(modules.router)
app.include_router(users.router)
app.include_router(courses.router)
