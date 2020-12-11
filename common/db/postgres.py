from typing import Dict, Union

from asyncpg.pool import Pool

from common.db.base import DbOptions
from common.exceptions import InitException
from config import settings

PG_POOL_REGISTRY: Dict[str, Pool] = {}


class PostgresDbRegister:
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
            PG_POOL_REGISTRY[db_name] = await cls._get_pool(options=options)

    @classmethod
    async def _get_pool(cls, options: Dict[str, Union[str, int]]):
        options = DbOptions.make(options)

        try:
            import asyncpg
        except Exception:
            raise InitException("asyncpg package not installed")

        return await asyncpg.create_pool(
            dsn=options.dsn,
            min_size=options.min_pool_size,
            max_size=options.max_pool_size,
        )


def pg_connection(dbname: str = settings.POOL_DEFAULT_NAME) -> Pool:
    return PG_POOL_REGISTRY[dbname]


async def shutdown_postgres_db_pool(app):
    for _, pool in PG_POOL_REGISTRY.items():

        if pool is None:
            continue

        await pool.close()

    PG_POOL_REGISTRY.clear()
