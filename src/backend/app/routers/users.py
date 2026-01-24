"""
This file describes the REST endpoint for database interactions with users.
"""

from fastapi import Depends, APIRouter, HTTPException, Request
from sqlmodel import Session, select

from app.models import User, UserResponse, LoginData
from app.dependencies import get_session, get_jwt_key, validate_jwt

import bcrypt
import jwt

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

@router.get("/")
def read_users(session: Session = Depends(get_session), username:str = Depends(validate_jwt)) -> list[UserResponse]:
    """
    Gets all users currently in the database
    
    Args:
        session (Session): the database session
        username (str): Username of the current user - extracted from jwt
    
    Returns:
        list[UserResponse]: The users currently stored in database
    """

    return session.exec(select(User)).all()

@router.post("/login")
def user_login(data:LoginData,
               session: Session = Depends(get_session),
               key:str = Depends(get_jwt_key))->str:
    """
    Handles an attempted user login
    
    Args:
        data (LoginData): object containing username and password
        session (Session): the database session
        key:str: A secret string needed for creating tokens
    
    Returns:
        str: Encoded JSON Web Token as a string
    """

    db_user = session.exec(select(User).where(User.username == data.username)).all()

    if not db_user:
        raise HTTPException(status = 401,detail = "username or password is wrong")

    if len(db_user)>1:
        raise HTTPException(status = 500,detail="something has gone terribly wrong")

    #now the user exist without question - we can check if credentials are correct
    user = db_user[0]
    if bcrypt.checkpw(data.passwd.encode("utf-8"),user.passwd):
        token = jwt.encode({"username": user.username},key)
        return token

    raise HTTPException(status = 401,detail = "username or password is wrong")
