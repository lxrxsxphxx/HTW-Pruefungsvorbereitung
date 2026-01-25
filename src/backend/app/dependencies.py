"""
This file contains functions that are used by several different endpoints
"""
import jwt
from sqlmodel import Session
from app.database import engine
from fastapi import Request, HTTPException
from jwt import PyJWTError

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
