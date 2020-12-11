import pytest
from aiohttp import web
from pymongo import MongoClient

from common.api import ErrorHandlerMiddleware
from common.db.mongo_db import MongoDbRegister, shutdown_mongo_db_pool
from common.logger import init_logger
from config import settings
from config.external import init_clients
from config.routes import init_routing_table

TEST_DB_PREFIX = "testdb"


@pytest.fixture(scope="session", autouse=True)
def drop_test_db():
    test_db_name = f"{settings.DB_NAME}_{TEST_DB_PREFIX}"
    from config.settings import MONGO_DSN

    client = MongoClient(MONGO_DSN)
    client.drop_database(test_db_name)

    yield

    client.drop_database(test_db_name)
    client.close()


def __init_test_app():
    init_logger(log_level=settings.LOG_LEVEL)
    from common.logger import app_logger

    app = web.Application(middlewares=[ErrorHandlerMiddleware(logger=app_logger)])
    init_routing_table(app)
    init_clients()
    test_db_name = f"{settings.DB_NAME}_{TEST_DB_PREFIX}"
    databases = {
        "default": {
            "dsn": settings.MONGO_DSN,
            "max_pool_size": 1,
            "min_pool_size": 0,
            "db_name": test_db_name,
        }
    }

    MongoDbRegister.setup_db(settings=databases)
    app.on_cleanup.append(shutdown_mongo_db_pool)

    return app


@pytest.fixture(autouse=True)
def client(loop, test_client):
    return loop.run_until_complete(test_client(__init_test_app()))
