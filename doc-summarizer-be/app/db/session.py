from app.core.config import Settings
from motor import motor_asyncio, core
from odmantic import AIOEngine
from pymongo.driver_info import DriverInfo

DRIVER_INFO = DriverInfo(name=Settings.PROJECT_NAME,
                         version=Settings.PROJECT_VERSION)


class _MongoClientSingleton:
    mongo_client: motor_asyncio.AsyncIOMotorClient | None
    engine: AIOEngine

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(_MongoClientSingleton, cls).__new__(cls)
            cls.instance.mongo_client = motor_asyncio.AsyncIOMotorClient(
                Settings.MONGO_CONNECTION_STRING, driver=DRIVER_INFO
            )
            cls.instance.engine = AIOEngine(
                client=cls.instance.mongo_client, database=Settings.MONGO_DB_NAME)
        return cls.instance


def MongoDatabase() -> core.AgnosticDatabase:
    return _MongoClientSingleton().mongo_client[Settings.MONGO_DB_NAME]


def get_engine() -> AIOEngine:
    return _MongoClientSingleton().engine


async def ping():
    await MongoDatabase().command("ping")


__all__ = ["MongoDatabase", "ping"]
