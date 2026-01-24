"""
This file describes the REST endpoint for database interactions with learning sets.
"""

from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select

from app.models import LearningSetBase, LearningSet, LearningSetResponse,Module
from app.dependencies import get_session, validate_jwt

router = APIRouter(
    prefix="/api/learning_set",
    tags=["learning_set"]
)

@router.post("/")
def create_learning_set(learning_set: LearningSetBase, session: Session = Depends(get_session),
                        modul_id:int | None = None, username:str = Depends(validate_jwt)) -> LearningSetResponse:
    """ 
    Adds a learning set to DB

    Args:
        learning_set (LearningSetBase): The learning set that is added to the database
        session (Session): the database session
        username (str): Username of the current user - extracted from jwt
    
    Returns: 
        LearningSetResponse: the learning set as it is in the database after adding
    """

    db_learning_set = LearningSet.model_validate(learning_set)
    if modul_id:
        db_module = session.get(Module,modul_id)
        if not db_module:
            raise HTTPException(status_code=404, detail="Module does not exist")
        db_learning_set.module_id=modul_id
    session.add(db_learning_set)
    session.commit()
    session.refresh(db_learning_set)

    return db_learning_set

@router.get("/")
def get_learning_sets(session: Session = Depends(get_session), modul: int | None = None, username:str = Depends(validate_jwt)) -> list[LearningSetResponse]:
    """
    Get all Learning Sets in DB
    Args:
        session (Session): the database session
        modul (int|None): id of the module the set belongs to
        username (str): Username of the current user - extracted from jwt
        
    Returns:
        list[LearningSetResponse]: List of stored learning sets
    """

    if modul:
        return session.exec(select(LearningSet).where(LearningSet.module_id == modul)).all()
    return session.exec(select(LearningSet)).all()

@router.get("/{learning_set_id}")
def get_single_learning_set(learning_set_id:int,session: Session = Depends(get_session), username:str = Depends(validate_jwt)) -> LearningSetResponse:
    """
    Get a single learning set by its id
    Args:
        learning_set_id (int): the id of the learning set you're looking for
        session (Session): the database session
        username (str): Username of the current user - extracted from jwt
        
    Returns:
        LearningSetResponse: The wanted learning set
    """

    learning_set = session.get(LearningSet, learning_set_id)
    if not learning_set:
        raise HTTPException(status_code=404, detail="Learning set not found")
    return learning_set

@router.delete("/{id}")
def delete_learning_set(id: int, session: Session = Depends(get_session), username:str = Depends(validate_jwt)):
    """
    Deletes a learning set from DB
    
    Args:
        id (int): id of the learning set that is deleted
        session (Session): the database session
        username (str): Username of the current user - extracted from jwt
        
    Returns:
        null
    """

    db_learning_set = session.get(LearningSet,id)

    if not db_learning_set:
        raise HTTPException(status_code = 404, detail="Learning set not found")

    session.delete(db_learning_set)
    session.commit()
