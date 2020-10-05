from dataclasses import dataclass
from enum import Enum
from typing import Dict, Union, Optional

from common.base_dto import BaseDto
from common.exceptions import InitException
from inspect import iscoroutinefunction

POOL_REGISTRY: Dict[str, object] = {}
POOL_DEFAULT_NAME = "default"


class _DbEnum(str, Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MONGODB = "mongodb"


@dataclass
class DbOptions(BaseDto):
    dsn: str
    db: _DbEnum
    max_pool_size: int
    min_pool_size: int
    db_name: Optional[str] = None

    def __post_init__(self):
        if not self.db or not self.dsn:
            raise InitException(
                f"Error on db init: db and dsn should be provided, your params are : {self.asdict()}"
            )
        if not isinstance(self.db, _DbEnum):
            self.db = _DbEnum(self.db)
        if not self.max_pool_size or self.min_pool_size < 0:
            self.max_pool_size = 1
        if not self.min_pool_size or self.min_pool_size < 0:
            self.min_pool_size = 1


class DbRegister:
    DB_OPTIONS = ("postgresql", "mysql", "mongodb")

    @classmethod
    async def setup_db(cls, settings: Dict[str, dict]):
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
            POOL_REGISTRY[db_name] = await cls._get_pool(options=options)

    @classmethod
    async def _get_pool(cls, options: Dict[str, Union[str, int]]):
        options = DbOptions.make(options)
        if options.db == _DbEnum.MONGODB:

            try:
                import motor.motor_asyncio as aiomotor
            except Exception:
                raise InitException("motor package not installed")
            client = aiomotor.AsyncIOMotorClient(
                options.dsn,
                maxPoolSize=options.max_pool_size,
                minPoolSize=options.min_pool_size,
            )
            return client[options.db_name]
        if options.db == _DbEnum.POSTGRESQL:
            try:
                import asyncpg
            except Exception:
                raise InitException("asyncpg package not installed")

            return await asyncpg.create_pool(
                dsn=options.dsn,
                min_size=options.min_pool_size,
                max_size=options.max_pool_size,
            )

        if options.db == _DbEnum.MYSQL:
            try:
                import aiomysql
                import dsnparse
            except Exception:
                raise InitException("aiomysql or dsnparse not installed")

            mysql_data = dsnparse.parse(options.dsn)

            return await aiomysql.create_pool(
                host=mysql_data.host,
                port=mysql_data.port,
                user=mysql_data.user,
                password=mysql_data.password,
                db=mysql_data.dbname,
                minsize=options.min_pool_size,
                maxsize=options.max_pool_size,
            )


def connection(dbname: str = POOL_DEFAULT_NAME) -> object:
    return POOL_REGISTRY[dbname]


async def shutdown_db_pool(app):
    for _, pool in POOL_REGISTRY.items():

        if pool is None:
            continue

        if hasattr(pool, "client"):
            pool.client.close()

        elif hasattr(pool, "close"):
            if iscoroutinefunction(pool.close):
                await pool.close()
            else:
                pool.close()
                await pool.wait_closed()

    POOL_REGISTRY.clear()
