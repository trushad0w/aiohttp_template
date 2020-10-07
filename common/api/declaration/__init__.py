import inspect
import typing

from common.api.declaration.handler import OperationHandler
from common.api.declaration.metadata import (
    METADATA_ATTRIBUTE_NAME,
    OperationMetadata,
    RequestBodyDefinition,
    RequestQueryDefinition,
)


def get(handler: typing.Callable) -> typing.Optional[OperationMetadata]:
    return getattr(handler, METADATA_ATTRIBUTE_NAME, None)


def fetch_all(
    modules: typing.Iterable[object],
) -> typing.Iterable[typing.Tuple[OperationMetadata, typing.Callable]]:
    """
    Searching for all OperationalMetadata objects in the list of modules
    """
    for module in modules:
        for _, func in inspect.getmembers(module, predicate=lambda x: inspect.isfunction(x)):

            if not hasattr(func, METADATA_ATTRIBUTE_NAME):
                continue

            yield (getattr(func, METADATA_ATTRIBUTE_NAME), func)
