from typing import Generator
from app.core.models.session_model import Session
from app.db.session import MongoDatabase
from bson import ObjectId
from fastapi import HTTPException, status, Depends
from motor.core import AgnosticDatabase
from app import crud
from app.api import deps


def get_db() -> Generator:
    try:
        db = MongoDatabase()
        yield db
    finally:
        pass


async def get_session(
        session_id: str | None,
        db: AgnosticDatabase = Depends(deps.get_db)) -> Session:
    session = await crud.session.get(db, id=ObjectId(session_id))
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found."
        )
    return session
