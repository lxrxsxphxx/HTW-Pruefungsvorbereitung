from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import Session, select

from app.models import CardBase, Card
from app.dependencies import get_session

router = APIRouter(
    prefix="/cards",
    tags=["cards"]
)

@router.post("/api/cards")
def create_card(cards: list[CardBase], session: Session = Depends(get_session)) -> list[Card]:
    db_cards = []
    for card in cards:
        db_card = Card.model_validate(card)
        session.add(db_card)
        session.commit()
        session.refresh(db_card)
        db_cards.append(db_card.copy())
    return db_cards

@router.get("/api/cards")
def read_cards(session: Session = Depends(get_session), modul: str | None = None) -> list[Card]:
    if modul:
        return session.exec(select(Card).where(Card.modul == modul)).all()
    return session.exec(select(Card)).all()

@router.get("/api/cards/{id}")
def read_card(id: int, session: Session = Depends(get_session)) -> Card:
    card = session.get(Card, id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

@router.put("/api/cards/{id}")
def read_card(id: int, card: CardBase, session: Session = Depends(get_session)) -> Card:
    db_card = session.get(Card, id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    card_data = card.model_dump(exclude_unset=True)
    db_card.sqlmodel_update(card_data)
    session.add(db_card)
    session.commit()
    session.refresh(db_card)
    return db_card

@router.delete("/api/cards/{id}")
def delete_card(id: int, session: Session = Depends(get_session)):
    card = session.get(Card, id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    session.delete(card)
    session.commit()
    return
