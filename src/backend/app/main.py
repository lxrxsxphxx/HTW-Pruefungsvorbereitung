"""
This file connects the different endoints to a single application
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session

from app.routers import cards, questions, learning_sets, modules, courses, users
from app.models import User, Course
from app.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:

        #creating informatik course if needed
        course = session.get(Course,1)
        if not course:
            db_course = Course(name="Informatik",faculty="Informatik/Mathematik",id=1)
            session.add(db_course)
            session.commit()

        #creating dummy user if needed
        db_user = session.get(User, 1)
        if not db_user:
            db_user = User( name = "Dummy Dummbatz",
                            faculty = "Metaphysik",
                            curr_semester=99,
                            id = 1,
                            course_id=1)
            session.add(db_user)
            session.commit()
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

