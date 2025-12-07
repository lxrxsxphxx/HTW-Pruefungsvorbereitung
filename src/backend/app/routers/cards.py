"""
Diese Datei beschreibt den Endpoint für Karteikarten.
"""

from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select

from app.models import CardBase, Card, LearningSet
from app.dependencies import get_session

router = APIRouter(
    prefix="/api/cards",
    tags=["cards"]
)

@router.post("/")
def create_card(cards: list[CardBase],learning_set_id: int ,session: Session = Depends(get_session)) -> list[Card]:

    learning_set = session.get(LearningSet,learning_set_id)
    if not learning_set:
        raise HTTPException(status_code=404, detail="Learning Set not found")

    db_cards = []
    for card in cards:
        db_card = Card.model_validate(card)
        db_card.learning_set_id = learning_set.id
        session.add(db_card)
        session.commit()
        session.refresh(db_card)
        db_cards.append(db_card.model_copy())

    return db_cards

@router.get("/")
def read_cards(session: Session = Depends(get_session)) -> list[Card]:
    return session.exec(select(Card)).all()

@router.get("/{id}")
def read_card(id: int, session: Session = Depends(get_session)) -> Card:
    card = session.get(Card, id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

@router.put("/{id}")
def update_card(id: int, card: CardBase, session: Session = Depends(get_session)) -> Card:
    db_card = session.get(Card, id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    card_data = card.model_dump(exclude_unset=True)
    db_card.sqlmodel_update(card_data)
    session.add(db_card)
    session.commit()
    session.refresh(db_card)
    return db_card

@router.delete("/{id}")
def delete_card(id: int, session: Session = Depends(get_session)):
    card = session.get(Card, id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    session.delete(card)
    session.commit()
    return
