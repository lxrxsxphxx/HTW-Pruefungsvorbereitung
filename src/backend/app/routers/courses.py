"""
This file describes the REST endpoint for database interactions with courses of study.
"""

from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select

from app.models import CourseBase,Course, CourseResponse, ModuleResponse,CourseModule,Module
from app.dependencies import get_session, validate_jwt

router = APIRouter(
    prefix="/api/courses",
    tags=["courses"]
)

@router.get("/")
def read_courses(session: Session = Depends(get_session), username:str = Depends(validate_jwt)) -> list[CourseResponse]:
    """
    Gets all courses of study currently in the database
    
    Args:
        session (Session): the database session
        username (str): Username of the current user - extracted from jwt
    
    Returns:
        list[CourseResponse]: The courses of study currently stored in database
    """

    return session.exec(select(Course)).all()

@router.post("/")
def post_course(course:CourseBase, session: Session = Depends(get_session), username:str = Depends(validate_jwt)) -> Course:
    """
    Adds a new course of study to the database
    
    Args:
        course (CourseBase): The course that is added to the database
        session (Session): the database session
        username (str): Username of the current user - extracted from jwt
    
    Returns:
        CourseResponse: The course as it is in the database after adding
    """

    db_course = Course.model_validate(course)
    session.add(db_course)
    session.commit()
    session.refresh(db_course)

    return db_course

@router.get("/{id}")
def get_single_course(id:int,session:Session = Depends(get_session), username:str = Depends(validate_jwt)) -> CourseResponse:
    """
    Gets a single course of study by its id
    
    Args:
        id (int): the id of the course
        session (Session): the database session
        username (str): Username of the current user - extracted from jwt
    
    Returns:
        CourseResponse: The course as it is in the database after adding
    """

    db_course = session.get(Course,id)
    if not db_course:
        raise HTTPException(status_code=404, detail="This course does not exist")
    return db_course

@router.get("/{id}/modules")
def get_modules(id:int,session:Session = Depends(get_session), username = Depends(validate_jwt)) -> list[ModuleResponse]:
    """
    Gets the modules associated with a course of study
    
    Args:
        id (int): the id of the course
        session (Session): the database session
        username (str): Username of the current user - extracted from jwt
    
    Returns:
        list[ModuleResponse]: the list of the wanted modules 
    """

    db_course = session.get(Course,id)
    if not db_course:
        raise HTTPException(status_code=404, detail="This course does not exist")

    modules = session.exec(select(Module)
                           .join(CourseModule)
                           .where(CourseModule.course_id == id)).all()
    return modules
