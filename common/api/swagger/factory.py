import re
import typing

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from common.api import (
    OperationMetadata,
    RequestBodyDefinition,
    ResponseDefinition,
)


class SwaggerFactory:
    def __init__(self, title: str, *, servers: typing.List[dict] = None, version: str = "1.0.0"):
        self.spec = APISpec(
            title=title,
            version=version,
            openapi_version="3.0.2",
            servers=servers,
            plugins=[MarshmallowPlugin()],
        )

    def make(self, operations: typing.Iterable[OperationMetadata]) -> dict:

        for operation in operations:
            self.spec.path(
                path=self.normalize_path(operation.path),
                operations={
                    str(method).lower(): self.create_operation(operation) for method in operation.methods
                },
            )

        return self.spec.to_dict()

    def create_operation(self, definition: OperationMetadata) -> dict:
        operation = {}
        operation_parameters = self.get_path_parameters(definition.path)

        if definition.request_query:
            operation_parameters.append(
                {
                    "in": "query",
                    "schema": definition.request_query.schema,
                }
            )

        if definition.deprecated:
            operation["deprecated"] = definition.deprecated

        if definition.tags:
            operation["tags"] = definition.tags

        if definition.summary:
            operation["summary"] = definition.summary

        if definition.description:
            operation["description"] = definition.description

        if definition.request_body:
            operation["requestBody"] = self.create_request_body(definition.request_body)

        if definition.responses:
            operation["responses"] = {
                str(status).upper(): self.create_response(resp_definition)
                for status, resp_definition in definition.responses.items()
            }

        if operation_parameters:
            operation["parameters"] = operation_parameters

        return operation

    def create_request_body(self, definition: RequestBodyDefinition):
        return {
            "description": definition.description,
            "required": definition.required,
            "content": {
                "application/json": {
                    "schema": definition.schema,
                    "examples": definition.examples,
                }
            },
        }

    def create_response(self, definition: ResponseDefinition) -> dict:
        return {
            "description": definition.description,
            "content": {"application/json": {"schema": definition.schema}},
        }

    @staticmethod
    def normalize_path(path: str) -> str:
        return re.sub(r"{(.+?):.+?}", "{\\1}", path.rstrip("/"))

    @staticmethod
    def get_path_parameters(path: str) -> list:
        return [
            {"in": "path", "name": m.group("name"), "required": True, "schema": {}}
            for m in re.finditer(r"{(?P<name>.+?)(:.+?)?}", path)
        ]
