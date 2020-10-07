from marshmallow import Schema

from common.api import definition, response, response_error


@definition(
    path="/health_check",
    responses={"200": response(Schema), "4xx": response_error(), "5xx": response_error()},
    methods=["GET"],
    tags=["srv"],
    description="Service route for health check",
)
async def health_check(request):
    return 200, None
