"""
This file describes the REST endpoint for database interactions with users.
"""

from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, select

from app.models import User, UserResponse, LoginData
from app.dependencies import get_session, get_jwt_key, validate_jwt

import bcrypt
import jwt

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

@router.post("/login")
def user_login(data:LoginData,
               session: Session = Depends(get_session),
               key:str = Depends(get_jwt_key))->JSONResponse:
    """
    Handles an attempted user login
    
    Args:
        data (LoginData): object containing username and password
        session (Session): the database session
        key:str: A secret string needed for creating tokens
    
    Returns:
        JSONResponse: Response Object containing a string and the cookie with the token
    """

    db_user = session.exec(select(User).where(User.username == data.username)).all()

    if not db_user:
        raise HTTPException(status = 401,detail = "username or password is wrong")

    if len(db_user)>1:
        raise HTTPException(status = 500,detail="something has gone terribly wrong")

    #now the user exist without question - we can check if credentials are correct
    user = db_user[0]
    if bcrypt.checkpw(data.passwd.encode("utf-8"),user.passwd):
        token = jwt.encode({"username": user.username},key,algorithm="HS256")
        content = {"message":"successfully logged in!"}
        response = JSONResponse(content=content)
        response.set_cookie(key="token",
                            value=token,
                            httponly=True,
                            samesite="lax")

        return response

    raise HTTPException(status = 401,detail = "username or password is wrong")
