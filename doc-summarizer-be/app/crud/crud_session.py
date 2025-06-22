from app.core.models.session import Session
from motor.core import AgnosticDatabase
from app.crud.base import CRUDBase


class CRUDSession(CRUDBase[Session, None, None]):
    async def create(self, db: AgnosticDatabase) -> Session:  # noqa
        return await self.engine.save(Session())


session = CRUDSession(Session)
