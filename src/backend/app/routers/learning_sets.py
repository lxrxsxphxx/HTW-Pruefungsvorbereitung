from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select

from app.models import LearningSetBase, LearningSet, LearningSetResponse
from app.dependencies import get_session

router = APIRouter(
    prefix="/api/learning_set",
    tags=["learning_set"]
)

@router.post("/")
def create_learning_set(learning_set: LearningSetBase, session: Session = Depends(get_session))-> LearningSet:
    """Adds a new learning set to DB"""

    print("create_learning_set called")

    db_learning_set = LearningSet.model_validate(learning_set)
    session.add(db_learning_set)
    session.commit()
    session.refresh(db_learning_set)

    return db_learning_set

@router.get("/")
def get_learning_sets(session: Session = Depends(get_session))-> list[LearningSetResponse]:
    """Returns list of all learning sets in DB"""

    return session.exec(select(LearningSet)).all()

@router.delete("/{id}")
def delete_learning_set(id: int, session: Session = Depends(get_session)) -> bool:
    """Deletes a learning set from DB"""
    db_learning_set = session.get(LearningSet,id)

    if not db_learning_set:
        raise HTTPException(status_code = 404, detail="Learning set not found")

    session.delete(db_learning_set)
    session.commit()
