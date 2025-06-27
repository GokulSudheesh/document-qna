from fastapi import APIRouter
from app.api.routes import chat, file, session

api_router = APIRouter()
api_router.include_router(chat.router)
api_router.include_router(file.router)
api_router.include_router(session.router)
