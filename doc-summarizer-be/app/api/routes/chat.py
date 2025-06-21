import logging
from fastapi import APIRouter
from app.core.models.chat import ChatRequestBody, ChatResponse
from app.core.utils.qdrant import get_chat_response


router = APIRouter(prefix="", tags=["Chat"])


@router.post("/chat")
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
