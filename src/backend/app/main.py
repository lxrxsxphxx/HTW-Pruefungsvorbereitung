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


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    SQLModel.metadata.create_all(engine)

    # Generate random key for jwt creation later on

    app.state.jwt_key = secrets.token_urlsafe()

    #writing default data to database
    with Session(engine) as session:

        #creating informatik course if needed
        db_course = course = session.get(Course,1)
        if not course:
            db_course = Course(name="Informatik",faculty="Informatik/Mathematik",id=1)
            session.add(db_course)
            session.commit()

        #creating dummy user if needed
        db_user = session.get(User, 1)
        if not db_user:

            salt = bcrypt.gensalt()
            hashed_passwd = bcrypt.hashpw(b'1234',salt)

            db_user = User( name = "Dummy Dummbatz",
                            faculty = "Metaphysik",
                            curr_semester=99,
                            id = 1,
                            course_id=1,
                            username="test@htw.de",
                            passwd=hashed_passwd)
            session.add(db_user)
            session.commit()

        #creating starter module if needed
        db_module = session.get(Module,1)
        if not db_module:
            db_module = Module(name="Grundlagen der Informatik",
                               lecturer="Prof. Dr. Boris Hollas",
                               semester=1,
                               id = 1)
            session.add(db_module)
            session.commit()

        #connecting created module and course if needed
        db_coursemodule = session.exec(select(CourseModule).where(CourseModule.module_id == 1,
                                                                  CourseModule.course_id==1)).all()
        if not db_coursemodule:
            db_coursemodule=CourseModule(course_id=1,module_id=1)
            session.add(db_coursemodule)
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
