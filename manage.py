import asyncio

import click
import uvloop
from aiohttp import web

from common.api import ErrorHandlerMiddleware, setup_swagger
from common.db import DbRegister, shutdown_db_pool
from config import settings
from config.logger import init_logger
from config.routes import init_routing_table


async def init_app():
    init_logger(log_level=settings.LOG_LEVEL)
    from config.logger import app_logger

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    app = web.Application(middlewares=[ErrorHandlerMiddleware(logger=app_logger)])

    init_routing_table(app)
    setup_swagger(app)

    await DbRegister.setup_db(settings=settings.DATABASES)
    init_logger(log_level=settings.LOG_LEVEL)

    app.on_cleanup.append(shutdown_db_pool)

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
def migrate():
    """
    Migrations command for SQL databases
    python manage.py migrate
    """
    from yoyo import read_migrations, get_backend

    backend = get_backend(settings.POSTGRESQL_DSN)
    migrations = read_migrations("./migrations")
    backend.apply_migrations(backend.to_apply(migrations))


cli.add_command(migrate)
cli.add_command(runserver)

if __name__ == "__main__":
    cli()
