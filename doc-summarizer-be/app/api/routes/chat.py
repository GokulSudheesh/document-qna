import logging
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.core.models.chat import ChatRequestBody, ChatResponse
from app.core.models.chat_response import ChatHistoryResponse
from app.core.models.session_model import Session
from app.core.utils.chat import get_chat_response, get_stream_chat_response
from motor.core import AgnosticDatabase
from app import crud
from app.api import deps

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/{session_id}")
async def chat(
    body: ChatRequestBody,
    db: AgnosticDatabase = Depends(deps.get_db),
    session: Session = Depends(deps.get_session)
) -> ChatResponse:
    await crud.session.update_session_updated_at(db, db_obj=session)
    past_chat_history = await crud.chat.get_transformed_chat_history(db, session=session)
    response = await get_chat_response(
        db=db,
        session=session,
        query=body.query,
        chat_history=past_chat_history
    )
    logging.info(f"Response: {response.model_dump_json()}")
    return ChatResponse(data=response.model_dump())


@router.post("/sse/{session_id}")
async def chat_stream(
    body: ChatRequestBody,
    db: AgnosticDatabase = Depends(deps.get_db),
    session: Session = Depends(deps.get_session)
) -> StreamingResponse:
    logging.info(
        f"Streaming chat response for session_id: {session.id}, query: {body.query}")
    await crud.session.update_session_updated_at(db, db_obj=session)
    past_chat_history = await crud.chat.get_transformed_chat_history(db, session=session)
    return StreamingResponse(get_stream_chat_response(
        db=db,
        session=session,
        query=body.query,
        chat_history=past_chat_history
    ), media_type="text/event-stream")


@router.get("/history/{session_id}")
async def chat_history(
    db: AgnosticDatabase = Depends(deps.get_db),
    session: Session = Depends(deps.get_session)
) -> ChatHistoryResponse:
    chat_history = await crud.chat.get_multi(db, session=session)
    return ChatHistoryResponse(data=chat_history)
