"""
This file describes the REST endpoint for database interactions with users.
"""

from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select

from app.models import UserBase,User, UserResponse
from app.dependencies import get_session

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

@router.get("/")
def read_users(session: Session = Depends(get_session)) -> list[UserResponse]:
    """
    Gets all users currently in the database
    
    Args:
        session (Session): the database session
    
    Returns:
        list[UserResponse]: The users currently stored in database
    """
    
    return session.exec(select(User)).all()