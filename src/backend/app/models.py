from sqlmodel import Field, SQLModel

class CardBase(SQLModel):
    front: str = Field()
    back: str = Field()
    modul: str = Field(index=True)

class Card(CardBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
