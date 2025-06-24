from __future__ import annotations
from datetime import datetime
from odmantic import Field, ObjectId
from app.db.base_class import Base


def datetime_now_sec():
    return datetime.now().replace(microsecond=0)


class Session(Base):
    created: datetime = Field(default_factory=datetime_now_sec)
    session_name: str = Field(default="")
    files: list[ObjectId] = Field(default_factory=list)
