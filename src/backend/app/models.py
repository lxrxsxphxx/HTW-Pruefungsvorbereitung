from sqlmodel import Field, Relationship, SQLModel

#Base: minimal content to create object
#table = True: this is a table in db

class CardBase(SQLModel):
    front: str = Field()
    back: str = Field()


class Card(CardBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    learning_set_id:int = Field(default = None, foreign_key = "learning_set.id")
    learning_set: "LearningSet" = Relationship(back_populates="cards")

class QuestionBase(SQLModel):
    question: str = Field()

class CardResponse(CardBase):
    id: int

class AnswerBase(SQLModel):
    answer: str = Field()
    correct: bool = Field()

class Question(QuestionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    answers: list["Answer"] = Relationship(back_populates="question", cascade_delete=True)
    learning_set_id:int = Field(default = None, foreign_key = "learning_set.id")
    learning_set: "LearningSet" = Relationship(back_populates="questions")

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

class LearningSetBase(SQLModel):
    name: str
    module: str

class LearningSet(LearningSetBase, table = True):
    id: int | None = Field(default=None, primary_key=True)
    cards: list[Card] = Relationship(back_populates="learning_set", cascade_delete=True)
    questions: list[Question] = Relationship(back_populates="learning_set", cascade_delete=True)

class LearningSetResponse(LearningSetBase):
    id: int
    cards: list[CardResponse]
    questions: list[QuestionResponse]
