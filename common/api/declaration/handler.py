import functools
import logging
import typing

from aiohttp import web
from common.api.declaration.metadata import (
    METADATA_ATTRIBUTE_NAME,
    OperationMetadata,
)
from common.api.exceptions import (
    APIDomainException,
    APIResponseFormatUndefined,
    resolve_status_code,
)
from common.api.response import make_response
from common.api.response.representation import make_representation_error_from_exception


class DummyOperationHandler:
    def __call__(self, func: typing.Callable):
        return func


class OperationHandler:
    def __init__(self, metadata: OperationMetadata):
        self.metadata = metadata

    def __call__(self, func: typing.Callable):
        return self.decorate(func)

    def decorate(self, handler: typing.Callable):

        setattr(handler, METADATA_ATTRIBUTE_NAME, self.metadata)

        if self.metadata.description is None:
            self.metadata.description = handler.__doc__

        @functools.wraps(handler)
        async def wrapper_handler(request: web.Request, *args, **kwargs):

            try:
                request = await self.extract_params_into_request(request)
                result = await handler(request, *args, **kwargs)
            except APIDomainException as e:
                result = make_representation_error_from_exception(e)
                result = result, resolve_status_code(e)

            return self.response_process(result)

        return wrapper_handler

    async def extract_params_into_request(self, req: web.Request) -> web.Request:
        if self.metadata.request_query:
            req["query"] = self.metadata.request_query.load(dict(req.query))

        if self.metadata.request_body:
            req["body"] = self.metadata.request_body.load(await req.text())

        return req

    def response_process(self, result) -> web.Response:
        if isinstance(result, web.Response):
            return result

        return self.make_response(result)

    def make_response(self, result) -> web.Response:
        status = 200
        headers = None

        if isinstance(result, tuple):

            result_len = len(result)

            if 3 == result_len:
                result, status, headers = result
            elif 2 == result_len:
                if isinstance(result[1], int):
                    result, status = result
                else:
                    result, headers = result
            else:
                raise TypeError(
                    "The API handler function did not return a valid response tuple. "
                    "The tuple must have the form (body, status, headers), "
                    "(body, status), or (body, headers)."
                )

        response = self.metadata.get_response(status)

        if not response:
            raise APIResponseFormatUndefined

        return make_response(response.dump(result), status=status, headers=headers)
