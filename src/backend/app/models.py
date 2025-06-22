from sqlmodel import Field, Relationship, SQLModel

class CardBase(SQLModel):
    front: str = Field()
    back: str = Field()
    modul: str = Field(index=True)

class Card(CardBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class QuestionBase(SQLModel):
    question: str = Field()

class AnswerBase(SQLModel):
    answer: str = Field()
    correct: bool = Field()

class Question(QuestionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    answers: list["Answer"] = Relationship(back_populates="question", cascade_delete=True)

class Answer(AnswerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    question_id: int = Field(default=None, foreign_key="question.id")
    question: Question = Relationship(back_populates="answers")

class AnswerResponse(AnswerBase):
    id: int
    question_id: int

class QuestionResponse(QuestionBase):
    id: int
    answers: list[AnswerResponse] = []
