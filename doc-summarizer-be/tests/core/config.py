import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class Settings():
    NVIDIA_API_KEY: str = os.getenv("NVIDIA_API_KEY")
    NVIDIA_EMBEDDINGS_API_KEY: str = os.getenv("NVIDIA_EMBEDDINGS_API_KEY")
    NVIDIA_EMBEDDINGS_MODEL: str = os.getenv(
        "NVIDIA_EMBEDDINGS_MODEL", "NV-Embed-QA")
    QDRANT_CONNECTION_URL: str = os.getenv("QDRANT_CONNECTION_URL")
    QDRANT_COLLECTION_NAME: str = "demo_collection"
