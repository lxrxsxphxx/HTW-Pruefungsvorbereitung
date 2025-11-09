from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select

from app.models import LearningSetBase, LearningSet, LearningSetResponse
from app.dependencies import get_session

router = APIRouter(
    prefix="/api/learning_set",
    tags=["learning_set"]
)

#create new learning set
@router.post("/")
def create_learning_set(learning_set: LearningSetBase, session: Session = Depends(get_session))-> LearningSet:
    print("create_learning_set called")

@router.get("/")
def get_learning_sets(session: Session = Depends(get_session))-> list[LearningSetResponse]:
    print("here, you get all learning sets")
    return session.exec(select(LearningSet)).all()

#TO DO
@router.delete("/{id}")
def delete_learning_set() -> bool:
    return True


#get new question in learning set id
@router.get("/{id}/questions")
def get_learning_set_question():
    print("get_learning_set_question called")
    #TO DO

#create new answer in learning set id
#@router.post("/{id}/answer")
#def create_learning_set_answer():
#    print("create_learning_set_answer called")
