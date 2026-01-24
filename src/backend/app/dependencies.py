"""
This file contains functions that are used by several different endpoints
"""

from sqlmodel import Session
from app.database import engine
from fastapi import Request

def get_session():
    with Session(engine) as session:
        yield session

def get_jwt_key(request:Request) -> str:
    """
    Funcion for retrieving the key used in jwt creation
    
    Args:
        request (Request): object containing metadata
    
    Returns:
        str: the currently used secret key
    """
    return request.app.state.jwt_key
