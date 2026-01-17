"""
This file describes the REST endpoint for database interactions with courses of study.
"""

from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select

from app.models import CourseBase,Course, CourseResponse
from app.dependencies import get_session

router = APIRouter(
    prefix="/api/courses",
    tags=["courses"]
)

@router.get("/")
def read_cards(session: Session = Depends(get_session)) -> list[CourseResponse]:
    """
    Gets all courses of study currently in the database
    
    Args:
        session (Session): the database session
    
    Returns:
        list[CourseResponse]: The courses of study currently stored in database
    """

    return session.exec(select(Course)).all()

@router.post("/")
def post_course(course:CourseBase, session: Session = Depends(get_session)) -> Course:
    """
    Adds a new course of study to the database
    
    Args:
        course (CourseBase): The course that is added to the database
        session (Session): the database session
    
    Returns:
        CourseResponse: The course as it is in the database after adding
    """

    db_course = Course.model_validate(course)
    session.add(db_course)
    session.commit()
    session.refresh(db_course)

    return db_course