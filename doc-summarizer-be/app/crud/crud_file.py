import logging
from typing import List

from bson import ObjectId
from fastapi import HTTPException, status

from app.core.config import Settings
from app.core.models.file_model import FileModel
from app.core.models.file_response import ExtractedFile
from motor.core import AgnosticDatabase
from app.core.models.session_model import Session
from app.core.utils.qdrant import delete_indexed_record
from app.crud.base import CRUDBase
from fastapi.encoders import jsonable_encoder


class CRUDFile(CRUDBase[FileModel, None, None]):
    async def create_multi(self, db: AgnosticDatabase, *, obj_in: List[ExtractedFile], session_obj: Session) -> List[FileModel]:  # noqa
        obj_in = [FileModel(id=file["id"], file_name=file["file_name"], file_size=file["file_size"],
                            file_type=file["file_type"], session_id=session_obj) for file in obj_in]
        # Extend the session's files with the new file IDs
        session_obj.files.extend(file.id for file in obj_in)
        obj_in_data = jsonable_encoder(obj_in)
        db_objs = [self.model(**data) for data in obj_in_data]  # type: ignore
        return await self.engine.save_all(db_objs)

    async def get_multi(self, session: Session, db: AgnosticDatabase, *, page: int = 0, page_break: bool = False):
        offset = [{"$limit": Settings.MULTI_MAX},
                  {"$skip": page * Settings.MULTI_MAX}] if page_break else []

        files = await self.engine.get_collection(FileModel).aggregate([
            {"$match": {"session_id": session.id}},
            *offset,
            {
                "$project":
                    {
                        "_id": 0,
                        "id": {
                            "$toString": "$_id"
                        },
                        "file_name": 1,
                        "file_type": 1,
                        "file_size": 1,
                        "created": {
                            "$toString": "$created"
                        },
                        "session_id": {
                            "$toString": "$session_id"
                        },
                    }
            },
        ]).to_list()
        return files

    async def remove(self, db: AgnosticDatabase, *, id: str) -> FileModel:
        await delete_indexed_record(file_id=id)
        id = ObjectId(id)
        db_obj = await self.get(db, id)
        if (not db_obj):
            logging.error(f"File with ID {id} not found for deletion.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found."
            )
        session = await self.engine.find_one(Session, Session.files.in_([db_obj.id]))
        session.files.remove(db_obj.id)
        await self.engine.save(session)
        await self.engine.delete(db_obj)
        return db_obj


file = CRUDFile(FileModel)
