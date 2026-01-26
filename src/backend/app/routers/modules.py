"""
This file describes the REST endpoint for database interactions with modules.
"""

from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select

from app.models import ModuleBase, Module, ModuleResponse, Course, CourseResponse, CourseModule, User, ModuleUser
from app.dependencies import get_session, validate_jwt

router = APIRouter(
    prefix="/api/modules",
    tags=["modules"]
)

@router.post("/")
def post_module(module:ModuleBase,session: Session = Depends(get_session),
                username:str = Depends(validate_jwt)) -> ModuleResponse:

    """
    Adds a module to DB

    Args:
        module (ModuleBase): The module that is added to the database
        session (Session): the database session
        username (str): Username of the current user - extracted from jwt
    
    Returns: 
        ModuleResponse: the module as it is in the database after adding
    """

    db_module = Module.model_validate(module)
    session.add(db_module)
    session.commit()
    session.refresh(db_module)

    return db_module

@router.get("/")
def read_modules(session: Session = Depends(get_session),
                 username:str = Depends(validate_jwt)) -> list[ModuleResponse]:
    """
    Gets all modules currently in the database
    
    Args:
        session (Session): the database session
        username (str): Username of the current user - extracted from jwt
    
    Returns:
        list[ModuleResponse]: The cards currently stored in database
    """

    return session.exec(select(Module)).all()

@router.get("/{id}/courses")
def get_courses(id:int,session:Session = Depends(get_session),
                username:str = Depends(validate_jwt)) -> list[CourseResponse]:
    """
    Gets the courses of study containing a certain module
    
    Args:
        id (int): the id of the module
        session (Session): the database session
        username (str): Username of the current user - extracted from jwt
    
    Returns:
        list[CourseResponse]: the list of the wanted courses of study 
    """

    db_course = session.get(Module,id)
    if not db_course:
        raise HTTPException(status_code=404, detail="This module does not exist")

    courses = session.exec(select(Course)
                           .join(CourseModule)
                           .where(CourseModule.course_id == id)).all()
    return courses

@router.post("/{id}/user")
def add_module_to_user(id: int, session:Session = Depends(get_session),
                username:str = Depends(validate_jwt)):
    """
    Handles adding a module to a users profile
    
    Args:
        id (int): the id of the module
        session (Session): the database session
        username (str): Username of the current user - extracted from jwt
    
    Returns:
        null
    """
    db_module = session.get(Module, id)
    if not db_module:
        raise HTTPException(status_code=404, detail="This module does not exist")
    
    db_user = session.exec(select(User).where(User.username == username)).all()
    if not db_user or len(db_user)>1:
        raise HTTPException(status_code=500,detail="something has gone terribly wrong")
    
    db_modeluser = session.get(ModuleUser, (db_module.id, db_user[0].id))
    if db_modeluser:
        raise HTTPException(status_code=400, detail="This module is already assigned to the user")
    
    module_user = ModuleUser(module_id=db_module.id, user_id=db_user[0].id)
    session.add(module_user)
    session.commit()

@router.delete("/{id}/user")
def remove_module_from_user(id: int, session:Session = Depends(get_session),
                username:str = Depends(validate_jwt)):
    """
    Handles removing a module from a users profile
    
    Args:
        id (int): the id of the module
        session (Session): the database session
        username (str): Username of the current user - extracted from jwt
    
    Returns:
        null
    """
    db_module = session.get(Module, id)
    if not db_module:
        raise HTTPException(status_code=404, detail="This module does not exist")
    
    db_user = session.exec(select(User).where(User.username == username)).all()
    if not db_user or len(db_user)>1:
        raise HTTPException(status_code=500,detail="something has gone terribly wrong")
    
    db_modeluser = session.get(ModuleUser, (db_module.id, db_user[0].id))
    if not db_modeluser:
        raise HTTPException(status_code=404, detail="This module is not assigned to the user")
    
    session.delete(db_modeluser)
    session.commit()
