import os
import sys
from dotenv import load_dotenv
from app.core.models.enum import Environment, FileType, Platform
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    stream=sys.stdout,
)

# Load environment variables from .env file
load_dotenv()


class Settings():
    ENVIRONMENT: Environment = os.getenv("ENVIRONMENT")
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "doc-summarizer"
    PROJECT_VERSION: str = "0.1.0"

    NVIDIA_API_KEY: str = os.getenv("NVIDIA_API_KEY")
    NVIDIA_EMBEDDINGS_API_KEY: str = os.getenv("NVIDIA_EMBEDDINGS_API_KEY")
    NVIDIA_EMBEDDINGS_MODEL: str = os.getenv(
        "NVIDIA_EMBEDDINGS_MODEL", "NV-Embed-QA")
    NVIDIA_VECTOR_SIZE: int = 1024
    NVIDIA_COMPLETIONS_MODEL_NAME: str = os.getenv(
        "NVIDIA_COMPLETIONS_MODEL_NAME", "speakleash/bielik-11b-v2.3-instruct")

    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL")
    OLLAMA_MODEL_NAME: str = os.getenv("OLLAMA_MODEL_NAME")
    OLLAMA_VECTOR_SIZE: int = 4096
    # Should be either "ollama" or "nvidia"
    PLATFORM_TO_USE: Platform = os.getenv("PLATFORM_TO_USE")

    QDRANT_CONNECTION_URL: str = os.getenv("QDRANT_CONNECTION_URL")
    QDRANT_COLLECTION_NAME: str = "docs_collection"
    CHUNK_SIZE: int = 2000
    NO_OF_CHUNKS: int = 3

    NVIDIA_MODEL_CONFIG: dict = {
        "model": NVIDIA_COMPLETIONS_MODEL_NAME,
        "api_key": NVIDIA_API_KEY,
        "temperature": 0.3,
        "max_tokens": 4096
    }

    OLLAMA_MODEL_CONFIG: dict = {
        "base_url": OLLAMA_BASE_URL,
        "model": OLLAMA_MODEL_NAME,
        "temperature": 0.3,
        "max_tokens": 4096
    }

    CHAT_STREAM_MESSAGE_EVENT: str = "message"
    CHAT_STREAM_REFERENCES_EVENT: str = "references"

    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    MAX_FILE_SIZE_STR: str = "5MB"
    ACCEPTED_FILE_TYPES: list[str] = [FileType.TEXT_TYPE, FileType.PDF_TYPE,
                                      FileType.DOC_TYPE, FileType.DOCX_TYPE, "txt", "pdf", "doc", "docx"]

    # MongoDB configuration
    MONGO_CONNECTION_STRING: str = os.getenv("MONGO_CONNECTION_STRING")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME")
    MULTI_MAX: int = 100
    SESSION_NAME_UPDATE_THRESHOLD: int = 10
