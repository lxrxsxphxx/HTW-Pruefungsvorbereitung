"""
This file describes the models used by the ORM.
These are used for communication between backend and frontend.
"""

from sqlmodel import Field, Relationship, SQLModel, LargeBinary, Column, UniqueConstraint

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

class LearningSet(LearningSetBase, table = True):
    """
    Class for how learning sets are stored in database.
    """

    id: int | None = Field(default=None, primary_key=True)
    cards: list[Card] = Relationship(back_populates="learning_set", cascade_delete=True)
    questions: list[Question] = Relationship(back_populates="learning_set", cascade_delete=True)
    module_id: int | None = Field(default=None, foreign_key="module.id")
    module: "Module" = Relationship(back_populates="learning_sets", cascade_delete=False)

class LearningSetResponse(LearningSetBase):
    """
    Class representing a learning set. Only used as response to GET-requests.
    """

    id: int
    cards: list[CardResponse]
    questions: list[QuestionResponse]

class CourseBase(SQLModel):
    """
    Base class for courses of study.
    Holds necessary information to describe a single course of study.
    """

    name: str
    faculty: str

class UserBase(SQLModel):
    """
    Base class for users. 
    Holds minimum necessary information to describe a single user.
    """
    name: str
    faculty: str
    curr_semester: int

class ModuleBase(SQLModel):
    """
    Base class for modules.
    Holds minimum necessary information to describe a single module.
    """

    name: str
    lecturer: str
    semester: int

class Course(CourseBase,table=True):
    """
    Class for how courses of study are stored in database.
    """

    id: int | None = Field(default=None, primary_key=True)
    modules:"CourseModule" = Relationship(back_populates="courses", cascade_delete=False)
    users: "User" = Relationship(back_populates="course")

class CourseResponse(CourseBase):
    """
    Class representing a course of study. Only used as response to GET-requests.
    """

    id: int

class CourseModule(SQLModel,table=True):
    """
    Class mapping Courses to modules and reverse.
    """

    course_id: int = Field(default=None, foreign_key="course.id", primary_key=True)
    courses:"Course" = Relationship(back_populates="modules", cascade_delete=False)
    module_id: int = Field(default=None, foreign_key="module.id", primary_key=True)
    modules:"Module" = Relationship(back_populates="courses", cascade_delete=False)

class User(UserBase,table=True):
    """
    Class for how users are stored in database.
    """
    __table_args__ = (UniqueConstraint("name"),)
    id: int | None = Field(default=None, primary_key=True)
    course_id: int | None = Field(default = None, foreign_key = "course.id")
    course:Course = Relationship(back_populates="users")
    modules:list["ModuleUser"] = Relationship(back_populates="user")
    username:str
    passwd:bytes = Field(sa_column=Column(LargeBinary))


class UserResponse(UserBase):
    """
    Class representing a user. Only used as response to GET-requests.
    """

    id:int
    course_id: int = Field(default=None, foreign_key="course.id")


class Module(ModuleBase,table=True):
    """
    Class for how modules are stored in database.
    """

    id: int | None = Field(default=None, primary_key=True)
    courses: list[CourseModule] = Relationship(back_populates="modules", cascade_delete=False)
    learning_sets: list[LearningSet] = Relationship(back_populates="module", cascade_delete=False)

class ModuleResponse(ModuleBase):
    """
    Class representing a card. Only used as response to GET-requests.
    """

    id:int
    learning_sets: list[LearningSetResponse]

class ModuleUser(SQLModel, table=True):
    """
    Class mapping modules to users and reverse.
    """

    module_id: int = Field(default=None, foreign_key="module.id", primary_key=True)
    module: Module  = Relationship(cascade_delete=False)
    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
    user: User = Relationship(back_populates="modules", cascade_delete=False)

class LoginData(SQLModel):
    """
    Class bundling the data for a user login into a single object
    """
    username: str
    passwd: str
