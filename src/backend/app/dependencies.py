"""
Diese Datei liefert die session mit der Datenbank.
Diese wird von den Endpoint zur Datenbankinteraktion benutzt.
"""

from sqlmodel import Session
from app.database import engine

def get_session():
    with Session(engine) as session:
        yield session