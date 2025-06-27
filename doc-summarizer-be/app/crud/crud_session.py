import logging
from bson import ObjectId
from app.core.models.chat_model import ChatModel
from app.core.models.file_model import FileModel
from app.core.models.session_model import Session, UpdateSession
from motor.core import AgnosticDatabase
from app.core.utils.qdrant import delete_indexed_record
from app.crud.base import CRUDBase
from app.core.config import Settings
from odmantic.engine import AIOCursor


class CRUDSession(CRUDBase[Session, None, UpdateSession]):
    async def create(self, db: AgnosticDatabase) -> Session:  # noqa
        return await self.engine.save(Session())

    async def get_multi(self, db: AgnosticDatabase, *, page: int = 0, page_break: bool = False) -> list[Session]:  # noqa
        offset = [{"$limit": Settings.MULTI_MAX},
                  {"$skip": page * Settings.MULTI_MAX}] if page_break else []
        collection = self.engine.get_collection(Session)
        motor_cursor = collection.aggregate([
            *offset,
            {
                "$project":
                    {
                        "created": {
                            "$toString": "$created"
                        },
                        "session_name": 1,
                        "files": 1,
                    }
            },
        ])
        return await AIOCursor(self.model, motor_cursor)

    async def get_by_id(self, db: AgnosticDatabase, id: str):
        logging.info(f"Retrieving session with ID: {ObjectId(id)}")
        sessions = await self.engine.get_collection(Session).aggregate([
            {
                "$match": {
                    "_id": ObjectId(id)
                }
            },
            {
                "$lookup": {
                    "from": "file",
                    "let": {
                        "file_ids": "$files"
                    },
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$in": [
                                        "$_id",
                                        "$$file_ids"
                                    ]
                                }
                            }
                        },
                        {
                            "$project": {
                                "_id": 0,
                                "id": {
                                    "$toString": "$_id"
                                },
                                "created": {
                                    "$toString": "$created"
                                },
                                "file_name": 1,
                                "file_type": 1,
                                "file_size": 1
                            }
                        }
                    ],
                    "as": "files"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "id": {
                        "$toString": "$_id"
                    },
                    "created": {
                        "$toString": "$created"
                    },
                    "files": 1,
                    "session_name": 1
                }
            }
        ]).to_list()
        return sessions[0] if sessions else None

    async def remove(self, db: AgnosticDatabase, *, db_obj: Session) -> Session:
        id = db_obj.id
        await delete_indexed_record(session_id=str(id))
        # Deleting associated files and chats
        await self.engine.remove(FileModel, FileModel.session_id == id)
        await self.engine.remove(ChatModel, ChatModel.session_id == id)
        await self.engine.delete(db_obj)
        return db_obj


session = CRUDSession(Session)
