import typing

from common.api.exceptions import (
    APIDomainException,
    resolve_error_code,
)


def make_representation_success(
    result: typing.Union[dict, list], *, pagination: typing.Optional[dict] = None
) -> dict:
    payload = {
        "success": True,
        "result": result,
    }

    if pagination:
        payload["pagination"] = pagination

    return payload


def make_representation_error(
    errors: typing.Iterable[dict],
    *,
    message: typing.Optional[str] = None,
    code: typing.Optional[str] = None,
    meta: typing.Optional[dict] = None,
) -> dict:
    """"""

    payload = {
        "success": False,
        "code": code,
        "message": message,
        "errors": errors,
        "meta": meta,
    }

    if not code:
        del payload["code"]

    if not message:
        del payload["message"]

    if not meta:
        del payload["meta"]

    return payload


def make_representation_error_from_exception(e: Exception) -> dict:
    """"""

    if isinstance(e, APIDomainException):
        return make_representation_error(code=e.code, message=e.message, errors=e.errors, meta=e.meta)

    return make_representation_error(errors=[make_error_from_exception(e)])


def make_representation_internal_server_error(
    meta: typing.Optional[dict] = None,
) -> dict:
    return make_representation_error(
        errors=[
            make_error(
                code="INTERNAL_SERVER_ERROR",
                message="Something went wrong, try again later.",
                meta=meta,
            )
        ]
    )


def make_error(
    code: str,
    message: str,
    *,
    field_name: str = None,
    meta: typing.Optional[dict] = None,
) -> dict:
    """"""

    error = {"code": code, "message": message}

    if field_name:
        error["field_name"] = field_name

    if meta:
        error["meta"] = meta

    return error


def make_error_from_exception(e: Exception) -> dict:
    return make_error(
        code=resolve_error_code(e),
        message=str(e),
    )


def make_validation_errors(errors: typing.Union[list, dict], field_name: str = None):
    """"""

    results = []

    for key in errors:

        if isinstance(errors[key], dict):
            results += make_validation_errors(errors[key], field_name=f"{field_name or ''}{key}.")
        else:
            results += (
                make_error(
                    code="VALIDATION_ERROR",
                    field_name=f"{field_name or ''}{key}",
                    message=message,
                )
                for message in errors[key]
            )

    return results
