import typing

import marshmallow

from common.api.declaration.handler import (
    DummyOperationHandler,
    OperationHandler,
)
from common.api.declaration.metadata import (
    OperationMetadata,
    RequestBodyDefinition,
    RequestQueryDefinition,
    ResponseDefinition,
    ResponseErrorDefinition,
    ResponsePaginationDefinition,
)
from common.api.response.schemas import ErrorSchema


def _assert_type(name: str, value: typing.Any, types: typing.Tuple[typing.Type, ...]):

    if not value or isinstance(value, types):
        return

    raise ValueError(
        f'Parameter "{name}" must be type {" or ".join(map(lambda x: x.__name__, types))}, '
        f"but got {value.__name__}"
    )


def definition(
    path: str,
    responses: typing.Dict[str, ResponseDefinition],
    methods: typing.Union[str, typing.Iterable[str]] = "GET",
    request_query: typing.Optional[RequestQueryDefinition] = None,
    request_body: typing.Optional[RequestBodyDefinition] = None,
    summary: typing.Optional[str] = None,
    description: typing.Optional[str] = None,
    deprecated: bool = False,
    tags: typing.Iterable[str] = None,
    disabled: bool = False,
):
    """
    :param path: Routing path
    :param responses: Response code and schema dict
    :param methods: Route methods
    :param request_query: Request query validation schema
    :param request_body: Request body validation schema
    :param summary: swagger summary
    :param description: swagger description
    :param deprecated: optional bool param to determine route deprecation
    :param tags: swagger tags
    :param disabled: If this parameter is True then it won't appear in the routing table
    """

    _assert_type(
        "request_query",
        request_query,
        (
            RequestQueryDefinition,
            RequestBodyDefinition,
        ),
    )
    _assert_type("request_body", request_body, (RequestBodyDefinition,))

    if disabled:
        return DummyOperationHandler()

    responses["4xx"] = response_error(description="Request Error")
    responses["5xx"] = response_error(description="Internal Server Error")

    return OperationHandler(
        OperationMetadata(
            path=path,
            methods=list(map(str.upper, (methods,) if isinstance(methods, str) else methods)),
            request_query=request_query,
            request_body=request_body,
            responses=responses,
            summary=summary,
            description=description,
            deprecated=deprecated,
            tags=tags or [],
        )
    )


def request_query(schema: typing.Type[marshmallow.Schema], **schema_kwargs) -> RequestQueryDefinition:
    return RequestQueryDefinition(
        schema=schema(
            unknown=schema_kwargs.pop("unknown", marshmallow.EXCLUDE),
            **schema_kwargs,
        )
    )


def request_body(
    schema: typing.Type[marshmallow.Schema],
    required: bool = True,
    description: typing.Optional[str] = None,
    examples: typing.Dict[str, dict] = None,
    **schema_kwargs,
) -> RequestBodyDefinition:
    return RequestBodyDefinition(
        schema=schema(unknown=schema_kwargs.pop("unknown", marshmallow.EXCLUDE), **schema_kwargs),
        required=required,
        description=description or schema.__doc__,
        examples=examples,
    )


def response(
    schema: typing.Type[marshmallow.Schema],
    description: str = None,
    many: bool = False,
    **schema_kwargs,
) -> ResponseDefinition:
    return ResponseDefinition(
        schema=schema(
            many=many,
            unknown=schema_kwargs.pop("unknown", marshmallow.EXCLUDE),
            **schema_kwargs,
        ),
        description=description,
    )


def response_pagination(
    schema: typing.Type[marshmallow.Schema], description: str = None, **schema_kwargs
) -> ResponsePaginationDefinition:
    return ResponsePaginationDefinition(
        schema=schema(
            many=True,
            unknown=schema_kwargs.pop("unknown", marshmallow.EXCLUDE),
            **schema_kwargs,
        ),
        description=description,
    )


def response_error(description: str = None) -> ResponseErrorDefinition:
    return ResponseErrorDefinition(schema=ErrorSchema(many=True), description=description)
