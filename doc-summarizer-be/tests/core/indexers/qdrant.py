from uuid import uuid4
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import AsyncQdrantClient, models
from core.config import Settings
from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from qdrant_client.http.models import Distance, VectorParams
from core.models.docs import DocMetaData


class DocumentIndexer:
    def __init__(self):
        self.client = AsyncQdrantClient(
            url=Settings.QDRANT_CONNECTION_URL, prefer_grpc=True)
        self.embeddings = NVIDIAEmbeddings(
            model=Settings.NVIDIA_EMBEDDINGS_MODEL, api_key=Settings.NVIDIA_EMBEDDINGS_API_KEY)
        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', ','],
            chunk_size=Settings.CHUNK_SIZE, chunk_overlap=200, add_start_index=True
        )

    async def index_documents(self, extracted_text: str, meta_data: DocMetaData) -> bool:
        try:
            collections = await self.client.get_collections()
            if Settings.QDRANT_COLLECTION_NAME not in [collection.name for collection in collections.collections]:
                print(
                    f"Creating collection: {Settings.QDRANT_COLLECTION_NAME}")
                await self.client.create_collection(
                    collection_name=Settings.QDRANT_COLLECTION_NAME,
                    vectors_config=VectorParams(
                        size=Settings.VECTOR_SIZE, distance=Distance.COSINE),
                )
            self.vector_store = QdrantVectorStore.from_existing_collection(
                collection_name=Settings.QDRANT_COLLECTION_NAME, embedding=self.embeddings)

            document = Document(
                page_content=extracted_text, metadata=meta_data)

            doc_splits = self.text_splitter.split_documents([document])
            # Generate UUIDs for all splits
            uuids = [f"{str(uuid4())}" for _ in range(len(doc_splits))]
            await self.vector_store.aadd_documents(documents=doc_splits, ids=uuids)
            print(
                f"Indexed {len(doc_splits)} document splits with UUIDs: {uuids}")
            return True
        except Exception as e:
            print(f"Error indexing document: {e}")
            raise

    async def get_retriever(self, filter: models.Filter | None, top_k: int) -> VectorStoreRetriever:
        try:
            if self.vector_store is None:
                self.vector_store = QdrantVectorStore.from_existing_collection(
                    collection_name=Settings.QDRANT_COLLECTION_NAME, embedding=self.embeddings)

            return self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": top_k, 'filter': filter})
        except Exception as e:
            print(f"Error creating retriever: {e}")
            raise


doc_indexer = DocumentIndexer()
