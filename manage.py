import asyncio

import click
import uvloop
from aiohttp import web

from common.db import DbRegister, shutdown_db_pool
from config import settings
from config.routes import setup_routes


async def init_app():
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    app = web.Application()

    setup_routes(app)

    await DbRegister.setup_db(settings=settings.DATABASES)

    app.on_cleanup.append(shutdown_db_pool)

    return app


@click.command()
@click.option("--port", default="8080", help="server port")
@click.option("--host", default="localhost", help="host address")
def run_server(port, host):
    app = init_app()
    web.run_app(app, port=port, host=host)


if __name__ == "__main__":
    run_server()
