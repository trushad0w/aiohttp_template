from typing import Type, TypeVar

from common.exceptions import ServiceInitError
from common.logger import app_logger
from common.services.client import ServiceClient


T = TypeVar('T')

CLIENT_SERVICES = {}


def register_service_client(
    class_name: Type[ServiceClient], initialized_class: ServiceClient
):
    """
    Method to register external service client
    Example usage:
    register_service_client(ServiceClient, ServiceClient(base_url, ...))
    """
    CLIENT_SERVICES[class_name] = initialized_class


def get_client(class_name: T):
    client_service: T = CLIENT_SERVICES.get(class_name)
    if not client_service:
        app_logger.critical(f"Service {class_name} has not been initialized")
        raise ServiceInitError(f"Service {class_name} has not been initialized")
    return client_service
