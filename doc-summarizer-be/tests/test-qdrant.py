import asyncio
from uuid import uuid4
from core.indexers.qdrant import doc_indexer
from utils.qdrant import get_chat_response
import os


docs_dir = "tests/docs"


def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


async def index_docs():
    session_id = uuid4()
    for filename in os.listdir(docs_dir):
        file_path = os.path.join(docs_dir, filename)
        if os.path.isfile(file_path):
            extracted_text = read_txt_file(file_path)
            await doc_indexer.index_documents(
                extracted_text=extracted_text,
                meta_data={
                    "file_id": uuid4(),
                    "session_id": session_id,
                    "file_name": filename,
                    "file_type": "text/plain"
                }
            )


async def main():
    # await index_docs()
    response = await get_chat_response(
        session_id="92e3b302-36d6-44c0-83a1-6ce89adae2b7",
        query="What is Amazon river often referred to as?",
        chat_history=[]
    )
    print(f"Response: {response.model_dump_json()}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred: {e}")
