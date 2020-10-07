import dataclasses
import itertools
import typing

import ujson
from marshmallow import (
    Schema,
    ValidationError,
)

from common.api.exceptions import APIDomainException
from common.api.response.representation import (
    make_validation_errors,
    make_representation_error,
    make_representation_success,
)

METADATA_ATTRIBUTE_NAME = "__api_metadata__"


class ResponseDefinition:
    def __init__(self, schema: Schema, description: str = None):
        self.schema = schema
        self.description = description

    def dump(self, result) -> dict:
        """"""

        if result is not None:
            result = self.schema.dump(result) if self.schema else None

        return make_representation_success(result)


class ResponsePaginationDefinition(ResponseDefinition):
    def dump(self, result) -> dict:
        return make_representation_success(
            self.schema.dump(result["items"]),
            pagination=result["pagination"],
        )


class ResponseErrorDefinition(ResponseDefinition):
    def dump(self, result) -> dict:
        return make_representation_error(
            self.schema.dump(result["errors"]),
            code=result.get("code"),
            message=result.get("message"),
            meta=result.get("pagination"),
        )


class RequestQueryDefinition:
    def __init__(self, schema: Schema):
        self.schema = schema

    def load(self, data: typing.Union[dict, str]) -> dict:
        """"""

        if isinstance(data, str):
            data = ujson.loads(data) if data else dict()

        if isinstance(data, dict) and "sort" in data:
            data["sort"] = dict(
                itertools.zip_longest(
                    str(data["sort"] or "").split(","),
                    str(data.pop("sort_dir") or "").split(","),
                )
            )

        try:
            return self.schema.load(data)
        except ValidationError as e:
            self.raise_error(e)

    def raise_error(self, e: ValidationError):
        raise APIDomainException(
            code="INCORRECT_QUERY_PARAMS",
            message="Incorrect query params",
            errors=make_validation_errors(e.messages),
            status=400,
        ) from e


class RequestBodyDefinition(RequestQueryDefinition):
    def __init__(
        self,
        schema: Schema,
        required: bool = True,
        description: typing.Optional[str] = None,
        examples: typing.Dict[str, dict] = None,
    ):
        """"""
        super().__init__(schema)
        self.required = required
        self.description = description
        self.examples = examples

    def raise_error(self, e: ValidationError):
        raise APIDomainException(
            code="INCORRECT_BODY",
            message="Incorrect body params",
            errors=make_validation_errors(e.messages),
            status=400,
        ) from e


@dataclasses.dataclass()
class OperationMetadata:
    path: str
    methods: typing.Iterable[str]
    request_query: typing.Optional[RequestQueryDefinition] = None
    request_body: typing.Optional[RequestBodyDefinition] = None
    responses: typing.Dict[str, ResponseDefinition] = dataclasses.field(default_factory=dict)
    summary: typing.Optional[str] = None
    description: typing.Optional[str] = None
    deprecated: bool = False
    tags: typing.Iterable[str] = dataclasses.field(default_factory=set)

    def get_response(self, status: int) -> typing.Optional[ResponseDefinition]:

        status_nnn = str(status)
        status_nnx = f"{status_nnn[:2]}x"
        status_nxx = f"{status_nnn[0]}xx"

        if status_nnn in self.responses:
            return self.responses[status_nnn]

        if status_nnx in self.responses:
            return self.responses[status_nnx]

        if status_nxx in self.responses:
            return self.responses[status_nxx]

        return None

    def __hash__(self):
        return hash(self.path) + sum(hash(x) for x in self.methods)
