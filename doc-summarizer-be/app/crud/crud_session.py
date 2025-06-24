import logging
from bson import ObjectId
from fastapi import HTTPException, status
from app.core.models.file_model import FileModel
from app.core.models.session_model import Session
from motor.core import AgnosticDatabase
from app.crud.base import CRUDBase


class CRUDSession(CRUDBase[Session, None, None]):
    async def create(self, db: AgnosticDatabase) -> Session:  # noqa
        return await self.engine.save(Session())

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
                                "file_type": 1
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

    async def remove(self, db: AgnosticDatabase, *, id: str) -> Session:
        id = ObjectId(id)
        db_obj = await self.get(db, id)
        if (not db_obj):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found."
            )
        async for file in self.engine.find(FileModel, FileModel.session_id == id):
            logging.info(f"Deleting file with ID: {file.id}")
            await self.engine.delete(file)
        await self.engine.delete(db_obj)
        return db_obj


session = CRUDSession(Session)
