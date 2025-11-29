from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select

from app.models import QuestionBase, Question, QuestionResponse, AnswerBase, Answer, AnswerResponse
from app.dependencies import get_session

router = APIRouter(
    prefix="/api/questions",
    tags=["questions"]
)

@router.post("/", response_model=QuestionResponse)
def create_question(question: QuestionBase, answers: list[AnswerBase],learningset_id, session: Session = Depends(get_session)) -> QuestionResponse:
    db_question = Question.model_validate(question)
    db_question.learning_set_id = learningset_id
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
def read_questions(session: Session = Depends(get_session)) -> list[QuestionResponse]:
    return session.exec(select(Question)).all()

@router.get("/{id}")
def read_question(id: int, session: Session = Depends(get_session)) -> QuestionResponse:
    question = session.get(Question, id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.put("/{id}")
def update_question(id: int, question: QuestionBase, session: Session = Depends(get_session)) -> QuestionResponse:
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
def delete_question(id: int, session: Session = Depends(get_session)):
    question = session.get(Question, id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    session.delete(question)
    session.commit()
    return

@router.put("/answers/{id}")
def update_answer(id: int, answer: AnswerBase ,session: Session = Depends(get_session)) -> AnswerResponse:
    db_answer = session.get(Answer, id)
    if not db_answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    answer_data = answer.model_dump(exclude_unset=True)
    db_answer.sqlmodel_update(answer_data)
    session.add(db_answer)
    session.commit()
    session.refresh(db_answer)
    return db_answer
