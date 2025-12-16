"""
This file gets the database session. The session ist used by the REST-endpoints
for database interactions
"""

from sqlmodel import Session
from app.database import engine

def get_session():
    with Session(engine) as session:
        yield session