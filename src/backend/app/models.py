"""
This file describes the models used by the ORM.
These are used for communication between backend and frontend.
"""

from sqlmodel import Field, Relationship, SQLModel

#Base: minimal content to create object
#table = True: this is a table in db


#see design.adoc for verbose documentation

class CardBase(SQLModel):
    """
    Base class for cards. Holds necessary information to describe a single card.
    """

    front: str = Field()
    back: str = Field()


class Card(CardBase, table=True):
    """
    Class for how cards are stored in database.
    """

    id: int | None = Field(default=None, primary_key=True)
    learning_set_id:int = Field(default = None, foreign_key = "learningset.id")
    learning_set: "LearningSet" = Relationship(back_populates="cards")

class QuestionBase(SQLModel):
    """
    Base class for cultiple choice questions. 
    Holds necessary information to describe a single multiple choice question.
    """

    question: str = Field()

class CardResponse(CardBase):
    """
    Class representing a card. Only used as response to GET-requests.
    """

    id: int

class AnswerBase(SQLModel):
    """
    Base class for answers of a multiple choice question.
    Holds necessary information to describe a single answer.
    """

    answer: str = Field()
    correct: bool = Field()

class Question(QuestionBase, table=True):
    """
    Class for how multiple choice questions are stored in database.
    """

    id: int | None = Field(default=None, primary_key=True)
    answers: list["Answer"] = Relationship(back_populates="question", cascade_delete=True)
    learning_set_id:int = Field(default = None, foreign_key = "learningset.id")
    learning_set: "LearningSet" = Relationship(back_populates="questions")

class Answer(AnswerBase, table=True):
    """
    Class for how answers to multiple choice questions are stored in database.
    """

    id: int | None = Field(default=None, primary_key=True)
    question_id: int = Field(default=None, foreign_key="question.id")
    question: Question = Relationship(back_populates="answers")

class AnswerResponse(AnswerBase):
    """
    Class representing an answer. Only used as response to GET-requests.
    """

    id: int
    question_id: int

class QuestionResponse(QuestionBase):
    """
    Class representing a question. Only used as response to GET-requests.
    """

    id: int
    answers: list[AnswerResponse] = []

class LearningSetBase(SQLModel):
    """
    Base class for learning sets. Holds necessary information to describe a single learning sets.
    """

    name: str
    module: str

class LearningSet(LearningSetBase, table = True):
    """
    Class for how answers to learning sets are stored in database.
    """

    id: int | None = Field(default=None, primary_key=True)
    cards: list[Card] = Relationship(back_populates="learning_set", cascade_delete=True)
    questions: list[Question] = Relationship(back_populates="learning_set", cascade_delete=True)

class LearningSetResponse(LearningSetBase):
    """
    Class representing a learning set. Only used as response to GET-requests.
    """

    id: int
    cards: list[CardResponse]
    questions: list[QuestionResponse]
