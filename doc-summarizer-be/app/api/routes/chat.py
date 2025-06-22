import logging
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.core.models.chat import ChatRequestBody, ChatResponse
from app.core.utils.qdrant import get_chat_response, get_stream_chat_response


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("")
async def chat(body: ChatRequestBody) -> ChatResponse:
    session_id = body.session_id
    query = body.query
    response = await get_chat_response(
        session_id=session_id,
        query=query,
        chat_history=[]
    )
    logging.info(f"Response: {response.model_dump_json()}")

    return ChatResponse(data=response.model_dump())


@router.post("/sse")
async def chat_stream(body: ChatRequestBody) -> ChatResponse:
    session_id = body.session_id
    query = body.query
    logging.info(
        f"Streaming chat response for session_id: {session_id}, query: {query}")
    return StreamingResponse(get_stream_chat_response(
        session_id=session_id,
        query=query,
        chat_history=[]
    ), media_type="text/event-stream")
