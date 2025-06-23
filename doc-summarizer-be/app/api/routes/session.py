import logging
from fastapi import APIRouter, status, HTTPException, Depends
from app.core.models.session import CreateSessionResponse, GetSessionsResponse
from motor.core import AgnosticDatabase
from app import crud
from app.api import deps


router = APIRouter(prefix="/session", tags=["Session"])


@router.post("/create")
async def create_session(*, db: AgnosticDatabase = Depends(deps.get_db),) -> CreateSessionResponse:
    """
    Endpoint to create a new session.
    """
    logging.info("Creating a new session")
    session = await crud.session.create(db=db)
    return CreateSessionResponse(data=session)


@router.get("/list")
async def list_sessions(*, db: AgnosticDatabase = Depends(deps.get_db)) -> GetSessionsResponse:
    """
    Endpoint to list all active sessions.
    """
    logging.info("Listing all active sessions")
    sessions = await crud.session.get_multi(db=db)
    return GetSessionsResponse(data=sessions)


@router.get("/{session_id}")
async def get_session(
    session_id: str,
    db: AgnosticDatabase = Depends(deps.get_db)
):
    """
    Endpoint to get a specific session by its ID.
    """
    # logging.info(f"Retrieving session with ID: {session_id}")
    session = await crud.session.get_by_id(db=db, id=session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return {"data": session}
