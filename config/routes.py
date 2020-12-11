from aiohttp import web

from common.api import setup_routes
import common
from apps.posts import views


def init_routing_table(app: web.Application):
    setup_routes(app=app, modules=(common, views), base_path="/template_api")
