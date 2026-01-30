"""
This file contains functions that are used by several different endpoints
"""
import jwt
from sqlmodel import Session, select
from app.database import engine
from app.models import Course,User,CourseModule, Module
from fastapi import Request, HTTPException
from jwt import PyJWTError
import bcrypt

def get_session():
    with Session(engine) as session:
        yield session

def get_jwt_key(request:Request) -> str:
    """
    Function for retrieving the key used in jwt creation
    
    Args:
        request (Request): object containing metadata
    
    Returns:
        str: the currently used secret key
    """
    return request.app.state.jwt_key

def validate_jwt(request: Request) -> str:
    """
    Function for validating a token

    Args:
        request (Request): object containing metadata
    
    Returns:
        str: the username contained in the token, if valid
    """

    token = request.cookies.get("token")

    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized - header missing")

    secret_key = request.app.state.jwt_key

    try:
        payload = jwt.decode(token,secret_key,algorithms=["HS256"])
        username = payload.get("username")
        if not username:
            raise HTTPException(status_code=401,detail = "invalid token payload")
    except PyJWTError:
        raise HTTPException(status_code=401, detail = "invalid token")

    return username


def write_starting_data(session:Session):
    """
    Writes some starting data to database
    
    Args:
        session (Session)
    Returns:
        null
    """

    with session:
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
            db_user = User( name = "Jürgen Anke",
                            faculty = "Informatik",
                            curr_semester=6,
                            id = 1,
                            course_id=1,
                            username="test@htw.de",
                            passwd=hashed_passwd)
            session.add(db_user)
            session.commit()

        startingmodules = [
            Module(name = "Mathemathik 1",
                   lecturer = "Prof. Dr. rer. nat. Fabian Schwarzenberger",
                   semester=1,
                   id=1),
            Module(name = "Betriebssysteme 1",
                   lecturer = "Prof. Dr. Robert Baumgartl",
                   semester=1,
                   id=2),
            Module(name = "Mathemathik 2",
                   lecturer = "Prof. Dr. rer. nat. Fabian Schwarzenberger",
                   semester=2,
                   id=3),
            Module(name = "Theoretische Informatik",
                   lecturer = "Prof. Dr. Boris Hollas",
                   semester=2,
                   id=4),
            Module(name = "Datenbanksysteme 1",
                   lecturer = "Prof. Dr. Axel Toll",
                   semester=2,
                   id=5),
            Module(name = "Datenbanksysteme 2",
                   lecturer = "Prof. Dr. Axel Toll",
                   semester=3,
                   id=6),
            Module(name = "Computergrafik 1",
                   lecturer = "PD Prof. Dr. Marco Block-Berlitz",
                   semester=3,
                   id=7),
            Module(name = "Stochastik",
                   lecturer = "Prof. Dr. rer. nat. Fabian Schwarzenberger",
                   semester=3,
                   id=8),
            Module(name = "Rechnerarchitektur",
                   lecturer = "Prof. Dr. Jens Schönthier",
                   semester=3,
                   id=9),
            Module(name = "Software Engineering 1",
                   lecturer =  "Prof. Dr. Jürgen Anke",
                   semester=4,
                   id=10),
            Module(name = "Künstliche Intelligenz",
                   lecturer = "Prof. Dr. Boris Hollas",
                   semester=4,
                   id=11),
            Module(name = "Betriebssysteme 2",
                   lecturer = "Prof. Dr. Robert Baumgartl",
                   semester=4,
                   id=12),
            Module(name = "Software Engineering 2",
                   lecturer = "Prof. Dr. Jürgen Anke",
                   semester=5,
                   id=13),
            Module(name = "Neuroinformationsverarbeitung",
                   lecturer = "Prof. Dr. Hans-Joachim Böhme",
                   semester=5,
                   id=14),
            Module(name = "Rechnernetze",
                   lecturer = "Prof. Dr. Jörg Vogt",
                   semester=3,
                   id=15),
            Module(name = "Webprogrammierung",
                   lecturer = "Prof. Dr. Jörg Vogt",
                   semester=4,
                   id=16)
        ]

        #creating starter module if needed
        for module in startingmodules:
            db_module = session.get(Module,module.id)
            if not db_module:
                session.add(module)
                session.commit()
                session.add(CourseModule(course_id = 1,module_id = module.id))
                session.commit()
