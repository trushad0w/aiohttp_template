from typing import Dict, Union

import motor.motor_asyncio as aiomotor

from common.db.base import DbOptions
from config import settings

MONGO_POOL_REGISTRY: Dict[str, aiomotor.AsyncIOMotorDatabase] = {}


class MongoDbRegister:
    @classmethod
    def setup_db(cls, settings: Dict[str, dict]):
        """
        Method to init connection pools

        Settings parameter should be this format

        {
            <pool_name>(example "default") : {
                "dsn": <str> (example "postgresql://postgres:pass@localhost:5432/postgres"),
                "db": <str: postgresql/mysql/mongodb> (parameter do determine pool connector),
                "max_pool_size": <int:optional> (Maximum number of pool connections) default 1,
                "min_pool_size": <int:optional> (Minimum size of pool connections) default 1,
                "db_name": <str: optional> (DB name for mongodb)
            }
        }
        "default" pool alias is required
        :param settings: dict object
        :return:
        """

        for db_name, options in settings.items():
            MONGO_POOL_REGISTRY[db_name] = cls._get_pool(options=options)

    @classmethod
    def _get_pool(cls, options: Dict[str, Union[str, int]]):
        options = DbOptions.make(options)

        client = aiomotor.AsyncIOMotorClient(
            options.dsn,
            maxPoolSize=options.max_pool_size,
            minPoolSize=options.min_pool_size,
        )
        return client[options.db_name]


def mongo_connection(dbname: str = settings.POOL_DEFAULT_NAME) -> aiomotor.AsyncIOMotorDatabase:
    return MONGO_POOL_REGISTRY[dbname]


async def shutdown_mongo_db_pool(app):
    for _, pool in MONGO_POOL_REGISTRY.items():

        if pool is None:
            continue

        pool.client.close()

    MONGO_POOL_REGISTRY.clear()
