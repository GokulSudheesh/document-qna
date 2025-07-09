from fastapi import FastAPI, Request
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import api_router
from app.core.config import Settings
from contextlib import asynccontextmanager
from app.core.models.enum import Environment
import logging


@asynccontextmanager
async def app_init(app: FastAPI):
    app.include_router(api_router, prefix=Settings.API_V1_STR)
    yield

app = FastAPI(title=Settings.PROJECT_NAME, lifespan=app_init,)

app.add_middleware(
    CORSMiddleware,
    allow_origins=Settings.ALLOWED_ORIGINS,
    allow_methods=["*"]
)


@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception):
    """
    Handles all unhandled exceptions and returns a 500 status code.
    """
    logging.error(f"{exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc) if Settings.ENVIRONMENT == Environment.LOCAL else "Something went wrong please try again."})
