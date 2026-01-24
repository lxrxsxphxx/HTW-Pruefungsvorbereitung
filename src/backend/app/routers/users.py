"""
This file describes the REST endpoint for database interactions with users.
"""

from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select

from app.models import User, UserResponse, LoginData
from app.dependencies import get_session

import bcrypt
import jwt

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

@router.post("/login")
def user_login(data:LoginData, session: Session = Depends(get_session))->str:
    """
    Handles an attempted user login
    
    Args:
        username (str): The username of the user trying to login
        passwd (str:): The plaintext password of the user
        session (Session): the database session
    
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
        #TODO - generate JWT
        token = jwt.encode({"username": user.username},"0")
        return token

    raise HTTPException(status = 401,detail = "username or password is wrong")
