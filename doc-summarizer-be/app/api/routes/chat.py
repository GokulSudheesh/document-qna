import json
import logging
from fastapi import APIRouter


router = APIRouter(prefix="", tags=["Chat"])


@router.get("/chat")
async def get_chat_response():
    # Simulating a chat response
    response = {
        "message": "This is a static chat response.",
        "status": "success"
    }
    return response
