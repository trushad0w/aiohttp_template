import re
import typing


class APICoreException(Exception):
    pass


class APIResponseFormatUndefined(APICoreException):
    pass


class APIDomainException(APICoreException):
    def __init__(
        self,
        message: typing.Union[str, None],
        *,
        code: str = None,
        status: int = 400,
        meta: typing.Optional[dict] = None,
        errors: typing.Iterable[dict] = None,
    ):
        """
        :param message:
        :param code:
        :param status:
        :param errors:
        :param meta:
        """
        self.code = code
        self.status = status
        self.message = message
        self.errors = errors
        self.meta = meta


def resolve_status_code(e: Exception) -> typing.Optional[int]:
    """"""

    if hasattr(e, "status"):
        return e.status

    return None


def resolve_error_code(e: Exception):
    """"""

    if hasattr(e, "code") and e.code:
        return e.code

    # to underscore
    error_code = re.sub(
        "([a-z0-9])([A-Z])",
        r"\1_\2",
        re.sub("(.)([A-Z][a-z]+)", r"\1_\2", type(e).__name__),
    ).upper()

    if "ERROR" not in error_code:
        error_code = f"ERROR_{error_code}"

    return error_code
