from common.services import register_service_client
from common.services.app_pages.client import AppPagesClient
from config import settings


def init_clients():
    register_service_client(
        AppPagesClient,
        AppPagesClient(
            base_url=settings.APP_PAGES_API_URL,
        ),
    )
