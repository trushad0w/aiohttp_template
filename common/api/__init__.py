from aiohttp import web

from common.api import declaration
from common.api.declaration.factory import *
from common.api.middlewares.error_handler import ErrorHandlerMiddleware


def setup_routes(app: web.Application, modules: typing.Iterable, *, base_path: str = ""):
    resources = {}

    for m, handler in declaration.fetch_all(modules):

        path = f"{base_path.rstrip('/')}{m.path.rstrip('/')}"
        resource = resources.get(path)

        if not resource:
            resource = app.router.add_resource(path)
            resources[path] = resource

        for method in m.methods:
            resource.add_route(method, handler)


def setup_swagger(
    app: web.Application,
    *,
    path_normalizer: typing.Callable[[str], str] = None,
    swagger_path: str = "/swagger.json",
    swagger_title: str = None,
    swagger_servers: typing.List[dict] = None,
):
    from common.api.swagger import (
        create_swagger_handler,
        SwaggerFactory,
    )

    app.router.add_get(
        path=swagger_path,
        handler=create_swagger_handler(
            app=app,
            path_normalizer=path_normalizer,
            swagger=SwaggerFactory(title=swagger_title, servers=swagger_servers),
        ),
    )
