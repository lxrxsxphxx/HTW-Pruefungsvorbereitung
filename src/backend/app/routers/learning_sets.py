from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select

from app.models import LearningSetBase, LearningSet, LearningSetResponse
from app.dependencies import get_session

router = APIRouter(
    prefix="/api/learning_set",
    tags=["learning_set"]
)

@router.post("/")
def create_learning_set(learning_set: LearningSetBase, session: Session = Depends(get_session)) -> LearningSet:
    """ Adds a learning set to DB
        learning_set: The learning set that is added to the database
        session: the database session
        
        returns the learning set as it is in the database after adding"""

    db_learning_set = LearningSet.model_validate(learning_set)
    session.add(db_learning_set)
    session.commit()
    session.refresh(db_learning_set)

    return db_learning_set

@router.get("/")
def get_learning_sets(session: Session = Depends(get_session), modul: str | None = None) -> list[LearningSetResponse]:
    """Get all Learning Sets in DB
        session: the database session
        
        returns list of LearningSets in LearningSetResponse type"""
    if modul:
        return session.exec(select(LearningSet).where(LearningSet.modul == modul)).all()
    return session.exec(select(LearningSet)).all()

@router.delete("/{id}")
def delete_learning_set(id: int, session: Session = Depends(get_session)) -> bool:
    """Deletes a learning set from DB
        id: id of the learning set that is deleted
        session: the database session
        
        returns information about success or failure"""

    db_learning_set = session.get(LearningSet,id)

    if not db_learning_set:
        raise HTTPException(status_code = 404, detail="Learning set not found")

    session.delete(db_learning_set)
    session.commit()
