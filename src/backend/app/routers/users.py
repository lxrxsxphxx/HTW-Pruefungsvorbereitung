"""
This file describes the REST endpoint for database interactions with users.
"""

from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, select

from app.models import ModuleResponse, Module, ModuleUser, User, UserResponse, LoginData
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
        raise HTTPException(status_code=401,detail = "username or password is wrong")

    if len(db_user)>1:
        raise HTTPException(status_code=500,detail="something has gone terribly wrong")

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

    raise HTTPException(status_code=401,detail = "username or password is wrong")

@router.get("/data")
def get_user_data(session: Session = Depends(get_session), username:str = Depends(validate_jwt)) -> UserResponse:
    """
    Gets data of the logged in user
    
    Args:
        session (Session): the database session
        username (str): Username of the current user - extracted from jwt
    
    Returns:
        UserResponse: The user currently logged in
    """

    db_user = session.exec(select(User).where(User.username == username)).all()

    if not db_user or len(db_user)>1:
        raise HTTPException(status_code=500,detail="something has gone terribly wrong")
    
    user = db_user[0]
    return user

@router.get("/modules")
def get_user_modules(session: Session = Depends(get_session), username:str = Depends(validate_jwt)) -> list[ModuleResponse]:
    """
    Gets modules of the logged in user
    
    Args:
        session (Session): the database session
        username (str): Username of the current user - extracted from jwt
    
    Returns:
        List[ModulesResponse]: The modules of the user currently logged in
    """
    db_user = session.exec(select(User).where(User.username == username)).all()

    if not db_user or len(db_user)>1:
        raise HTTPException(status_code=500,detail="something has gone terribly wrong")
    
    user = db_user[0]
    modules = session.exec(select(Module)
                 .join(ModuleUser)
                 .where(User.id == user.id)).all()
    return modules
