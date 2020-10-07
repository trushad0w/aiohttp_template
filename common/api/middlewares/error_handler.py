import logging
import traceback
import typing

from aiohttp import web
from common.api.exceptions import (
    APIDomainException,
    resolve_status_code,
)
from common.api.response import make_response
from common.api.response.representation import (
    make_representation_error_from_exception,
    make_representation_internal_server_error,
)


@web.middleware
class ErrorHandlerMiddleware:
    def __init__(
        self,
        *,
        domain_exceptions: typing.Iterable[typing.Type[Exception]] = (),
        logger: logging.Logger = None
    ):

        self.domain_exceptions = domain_exceptions
        self.logger = logger or logging.getLogger("main")

    async def __call__(self, request: web.Request, handler: typing.Callable, *args, **kwargs):
        try:
            return await handler(request, *args, **kwargs)
        except APIDomainException as e:
            return self.create_response_from_exception(e, e.status)
        except (web.HTTPError, *self.domain_exceptions) as e:
            return self.create_response_from_exception(e)
        except Exception as e:
            self.logger.debug(traceback.format_exc())
            self.logger.critical(e)
            return self.create_response_internal_server_error(e)

    @staticmethod
    def create_response_from_exception(e: Exception, status: int = None):
        return make_response(
            make_representation_error_from_exception(e),
            status=(status or resolve_status_code(e)),
        )

    @staticmethod
    def create_response_internal_server_error(e: Exception):
        return make_response(make_representation_internal_server_error(), status=500)
