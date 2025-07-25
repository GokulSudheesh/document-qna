from uuid import uuid4
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import AsyncQdrantClient, models
from app.core.config import Settings
from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from qdrant_client.http.models import Distance, VectorParams
from app.core.models.enum import Platform
from app.core.models.file_model import DocMetaData
import logging


class DocumentIndexer:
    def __init__(self):
        self.client = AsyncQdrantClient(
            url=Settings.QDRANT_CONNECTION_URL, prefer_grpc=True)
        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', ','],
            chunk_size=Settings.CHUNK_SIZE, chunk_overlap=200, add_start_index=True
        )
        match Settings.PLATFORM_TO_USE:
            case Platform.NVIDIA:
                self.embeddings = NVIDIAEmbeddings(
                    model=Settings.NVIDIA_EMBEDDINGS_MODEL,
                    api_key=Settings.NVIDIA_EMBEDDINGS_API_KEY
                )
                self.vector_size = Settings.NVIDIA_VECTOR_SIZE
            case Platform.OLLAMA:
                self.embeddings = OllamaEmbeddings(
                    base_url=Settings.OLLAMA_BASE_URL,
                    model=Settings.OLLAMA_MODEL_NAME
                )
                self.vector_size = Settings.OLLAMA_VECTOR_SIZE

    async def index_documents(self, extracted_text: str, meta_data: DocMetaData) -> bool:
        try:
            collections = await self.client.get_collections()
            if Settings.QDRANT_COLLECTION_NAME not in [collection.name for collection in collections.collections]:
                logging.info(
                    f"Creating collection: {Settings.QDRANT_COLLECTION_NAME}")
                await self.client.create_collection(
                    collection_name=Settings.QDRANT_COLLECTION_NAME,
                    vectors_config=VectorParams(
                        size=self.vector_size, distance=Distance.COSINE),
                )
            self.vector_store = QdrantVectorStore.from_existing_collection(
                collection_name=Settings.QDRANT_COLLECTION_NAME, embedding=self.embeddings)

            document = Document(
                page_content=extracted_text, metadata=meta_data)

            doc_splits = self.text_splitter.split_documents([document])
            # Generate UUIDs for all splits
            uuids = [f"{str(uuid4())}" for _ in range(len(doc_splits))]
            await self.vector_store.aadd_documents(documents=doc_splits, ids=uuids)
            logging.info(
                f"Indexed {len(doc_splits)} document splits with UUIDs: {uuids}")
            return True
        except Exception as e:
            logging.error(f"Error indexing document: {e}")
            raise

    async def get_retriever(self, filter: models.Filter | None, top_k: int) -> VectorStoreRetriever:
        try:
            if self.vector_store is None:
                self.vector_store = QdrantVectorStore.from_existing_collection(
                    collection_name=Settings.QDRANT_COLLECTION_NAME, embedding=self.embeddings)

            return self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": top_k, 'filter': filter})
        except Exception as e:
            logging.info(f"Error creating retriever: {e}")
            raise

    async def delete_record(self, filter: models.Filter | None,) -> bool:
        try:
            await self.client.delete(collection_name=Settings.QDRANT_COLLECTION_NAME, points_selector=filter)
            logging.info(f"Deleted record with filter: {filter}")
            return True
        except Exception as e:
            logging.error(f"Error deleting record: {e}")
            raise


doc_indexer = DocumentIndexer()
