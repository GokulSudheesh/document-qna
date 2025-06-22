from fastapi import APIRouter
from app.api.routes import chat, file

api_router = APIRouter()
api_router.include_router(chat.router)
api_router.include_router(file.router)
