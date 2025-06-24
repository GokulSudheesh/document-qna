import logging
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import StreamingResponse
from app.core.models.chat import ChatRequestBody, ChatResponse
from app.core.models.chat_response import ChatHistoryResponse
from app.core.utils.chat import get_chat_response, get_stream_chat_response
from motor.core import AgnosticDatabase
from app import crud
from app.api import deps

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("")
async def chat(body: ChatRequestBody, db: AgnosticDatabase = Depends(deps.get_db)) -> ChatResponse:
    session_id = body.session_id
    query = body.query
    session = await crud.session.get(db, id=ObjectId(session_id))
    if (not session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found."
        )
    past_chat_history = await crud.chat.get_transformed_chat_history(db, session=session)
    response = await get_chat_response(
        db=db,
        session=session,
        query=query,
        chat_history=past_chat_history
    )
    logging.info(f"Response: {response.model_dump_json()}")
    return ChatResponse(data=response.model_dump())


@router.post("/sse")
async def chat_stream(body: ChatRequestBody,
                      db: AgnosticDatabase = Depends(deps.get_db)) -> StreamingResponse:
    session_id = body.session_id
    query = body.query
    session = await crud.session.get(db, id=ObjectId(session_id))
    if (not session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found."
        )
    logging.info(
        f"Streaming chat response for session_id: {session_id}, query: {query}")
    past_chat_history = await crud.chat.get_transformed_chat_history(db, session=session)
    return StreamingResponse(get_stream_chat_response(
        db=db,
        session=session,
        query=query,
        chat_history=past_chat_history
    ), media_type="text/event-stream")


@router.get("/history/{session_id}")
async def chat_history(session_id: str, db: AgnosticDatabase = Depends(deps.get_db)) -> ChatHistoryResponse:
    session = await crud.session.get(db, id=ObjectId(session_id))
    if (not session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found."
        )
    chat_history = await crud.chat.get_multi(db, session=session)
    return ChatHistoryResponse(data=chat_history)
