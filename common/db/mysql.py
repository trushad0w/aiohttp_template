from typing import Dict, Union

from common.db.base import DbOptions
from common.exceptions import InitException
from config import settings

MYSQL_POOL_REGISTRY: Dict[str, object] = {}


class DbRegister:
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
            MYSQL_POOL_REGISTRY[db_name] = await cls._get_pool(options=options)

    @classmethod
    async def _get_pool(cls, options: Dict[str, Union[str, int]]):
        options = DbOptions.make(options)

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


def connection(dbname: str = settings.POOL_DEFAULT_NAME) -> object:
    return MYSQL_POOL_REGISTRY[dbname]


async def shutdown_db_pool(app):
    for _, pool in MYSQL_POOL_REGISTRY.items():

        if pool is None:
            continue

        pool.close()
        await pool.wait_closed()

    MYSQL_POOL_REGISTRY.clear()
