import typing
from copy import copy

from aiohttp import web
from common.api import declaration
from common.api.swagger.factory import SwaggerFactory


def create_swagger_handler(
    app: web.Application, swagger: SwaggerFactory, *, path_normalizer: typing.Callable[[str], str] = None
):
    operations = set()

    if not path_normalizer:
        path_normalizer = lambda x: x

    for route in app.router.routes():
        operation = declaration.get(route.handler)
        if operation:
            operation = copy(operation)
            operation.path = path_normalizer(str(route.resource.canonical))
            operations.add(operation)

    async def handler(req: web.Request):
        return web.json_response(swagger.make(operations))

    return handler
