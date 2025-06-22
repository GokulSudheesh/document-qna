import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings():
    NVIDIA_API_KEY: str = os.getenv("NVIDIA_API_KEY")
    NVIDIA_EMBEDDINGS_API_KEY: str = os.getenv("NVIDIA_EMBEDDINGS_API_KEY")
    NVIDIA_EMBEDDINGS_MODEL: str = os.getenv(
        "NVIDIA_EMBEDDINGS_MODEL", "NV-Embed-QA")
    NVIDIA_COMPLETIONS_MODEL_NAME: str = os.getenv(
        "NVIDIA_COMPLETIONS_MODEL_NAME", "mistralai/mistral-7b-instruct-v0.2")
    QDRANT_CONNECTION_URL: str = os.getenv("QDRANT_CONNECTION_URL")
    QDRANT_COLLECTION_NAME: str = "docs_collection"
    VECTOR_SIZE: int = 1024
    CHUNK_SIZE: int = 2000
    NO_OF_CHUNKS: int = 3

    NVIDIA_MODEL_CONFIG: dict = {
        "model": NVIDIA_COMPLETIONS_MODEL_NAME,
        "api_key": NVIDIA_API_KEY,
        "temperature": 0.3,
        "max_tokens": 4096
    }
