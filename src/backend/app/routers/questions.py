"""
This file describes the endpoint for database interactions with multiple choice questions.
"""

from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select

from app.models import QuestionBase, Question, QuestionResponse, AnswerBase, Answer, AnswerResponse, LearningSet
from app.dependencies import get_session, validate_jwt

router = APIRouter(
    prefix="/api/questions",
    tags=["questions"]
)

@router.post("/", response_model=QuestionResponse)
def create_question(question: QuestionBase,
                    answers: list[AnswerBase],
                    learning_set_id:int,
                    session: Session = Depends(get_session),
                    username:str = Depends(validate_jwt)) -> QuestionResponse:
    """
    Docstring for create_question
    
    Args:
        question (QuestionBase): The Question that is going to be added
        answers (list[AnswerBase]): the possible answers a user can give
        learning_set_id (int): the id of the learning set the question should belong to
        session (Session): the database session
        username (str): Username of the current user - extracted from jwt

    Returns:
        QuestionResponse: The Question that has been added
    """
    db_question = Question.model_validate(question)

    db_learning_set=session.get(LearningSet,learning_set_id)
    if not db_learning_set:
        raise HTTPException(status_code=404, detail="learning_set does not exist")

    db_question.learning_set_id = learning_set_id
    session.add(db_question)
    session.commit()
    session.refresh(db_question)
    for a in answers:
        db_answer = Answer.model_validate(a)
        db_answer.question_id = db_question.id
        session.add(db_answer)
        session.commit()
    session.refresh(db_question)
    return db_question


@router.get("/")
def read_questions(learning_set_id:int | None = None,
                   session: Session = Depends(get_session),
                   username:str = Depends(validate_jwt)) -> list[QuestionResponse]:
    """
    Reads all questions from the database
    
    Args:
        session (Session): the database session
        learning_set_id(int | None): the learning set the questions should belong to
        username (str): Username of the current user - extracted from jwt
    
    Returns:
        list[QuestionResponse]: All questions in the database
    """
    if learning_set_id:
        return session.exec(
            select(Question).where(Question.learning_set_id == learning_set_id)).all()
    return session.exec(select(Question)).all()

@router.get("/{id}")
def read_question(id: int,
                  session: Session = Depends(get_session),
                  username:str = Depends(validate_jwt)) -> QuestionResponse:
    """
    Reads a single question by its id
    
    Args:
        id (int): the id of the wanted question
        session (Session): the database session
        username (str): Username of the current user - extracted from jwt
    
    Returns:
        QuestionResponse: The question that is stored
    """

    question = session.get(Question, id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.put("/{id}")
def update_question(id: int,
                    question: QuestionBase,
                    session: Session = Depends(get_session),
                    username:str = Depends(validate_jwt)) -> QuestionResponse:
    """
    update a question, but not its answers!
    
    Args:
        id (int): the id of the question taht is going to be updated:
        question (QuestionBase): the new information of the question 
        session (Session): the database session
        username (str): Username of the current user - extracted from jwt
    
    Returns:
        QuestionResponse: the updated question
    """

    db_question = session.get(Question, id)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    question_data = question.model_dump(exclude_unset=True)
    db_question.sqlmodel_update(question_data)
    session.add(db_question)
    session.commit()
    session.refresh(db_question)
    return db_question

@router.delete("/{id}")
def delete_question(id: int,
                    session: Session = Depends(get_session),
                    username:str = Depends(validate_jwt)):
    """
    deletes a question
    
    Args:
        id (int): the id of the question that is going to be deleted
        session (Session): the database session
        username (str): Username of the current user - extracted from jwt

    Returns:
        null
    """

    question = session.get(Question, id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    session.delete(question)
    session.commit()
    return

@router.put("/answers/{id}")
def update_answer(id: int,
                  answer: AnswerBase,
                  session: Session = Depends(get_session),
                  username:str = Depends(validate_jwt)) -> AnswerResponse:
    """
    Updates an answer
    
    Args:
        id (int): the id of the answer that is going to be updated
        answer (AnswerBase): the new information of the answer
        session (Session): the database session
        username (str): Username of the current user - extracted from jwt
    
    Returns:
        AnswerResponse: the updated answer
    """

    db_answer = session.get(Answer, id)
    if not db_answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    answer_data = answer.model_dump(exclude_unset=True)
    db_answer.sqlmodel_update(answer_data)
    session.add(db_answer)
    session.commit()
    session.refresh(db_answer)
    return db_answer
