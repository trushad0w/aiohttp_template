import asyncio

import click
import uvloop
from aiohttp import web

from common.api import ErrorHandlerMiddleware, setup_swagger
from common.db.mongo_db import MongoDbRegister, shutdown_mongo_db_pool
from config import settings
from common.logger import init_logger
from config.external import init_clients
from config.routes import init_routing_table


async def init_app():
    init_logger(log_level=settings.LOG_LEVEL)
    from common.logger import app_logger

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    app = web.Application(middlewares=[ErrorHandlerMiddleware(logger=app_logger)])

    init_routing_table(app)
    setup_swagger(app)
    init_clients()

    MongoDbRegister.setup_db(settings=settings.MONGO_DATABASES)

    app.on_cleanup.append(shutdown_mongo_db_pool)

    return app


@click.group()
def cli():
    pass


@click.command()
@click.option("--port", default="8000", help="server port")
@click.option("--host", default="0.0.0.0", help="host address")
def runserver(port: int, host: str):
    """
    Command to run server
    python manage.py run-server [optional params --port <port: int> --host <host: str>]
    :param port: port to run server on <optional>
    :param host: host to run server on <optional>
    :return:
    """
    app = init_app()
    web.run_app(app, port=port, host=host)


@click.command()
def pgmigrate():
    """
    # TODO: Remove this if your main db is not PG or MYSQL
    Migrations command for SQL databases
    python manage.py migrate
    """
    from yoyo import read_migrations, get_backend

    backend = get_backend(settings.POSTGRESQL_DSN)
    migrations = read_migrations("./pg_migrations")
    backend.apply_migrations(backend.to_apply(migrations))


@click.command()
def mongo_migrate():
    """
    # TODO: Remove this if your main db is not Mongo DB
    Method to apply migrations for mongo db
    :return:
    """
    from pymongo_migrate.mongo_migrate import MongoMigrate
    from pymongo import MongoClient

    migrations = "./mongo_migrations"

    MongoMigrate(
        client=MongoClient(f"{settings.MONGO_DSN}/{settings.DB_NAME}?authSource=admin"),
        migrations_dir=migrations,
    ).migrate()


cli.add_command(pgmigrate)
cli.add_command(mongo_migrate)
cli.add_command(runserver)

if __name__ == "__main__":
    cli()
