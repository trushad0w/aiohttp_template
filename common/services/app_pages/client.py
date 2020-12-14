from typing import List, Optional, Callable, Dict

from aiohttp import ClientResponseError

from common.logger import app_logger
from common.services import ServiceClient
from common.services.app_pages.models import (
    AppPagesStoreEnum,
    AppDataDto,
    DevContextAppDto,
    BlogPostDto,
    DevNameDto,
    DevAppsDto,
    AppTripletDto,
)
from common.services.app_pages.schemas import AppDataSchema, BlogPostSchema, DevNameSchema, DevAppsSchema


class AppPagesClient(ServiceClient):
    APPDATA_URL = "/api/v2/appdata"
    DEV_CONTEXT_URL = "/api/v2/devcntx"
    FEATURED_POSTS_URL = "/api/v2/featured_posts/{store}"
    DEV_NAME_URL = "/api/v2/devname/{store}/{country}/{dev_slug}"
    BLOCKED_APPS_URL = "/api/v2/blocked_apps"
    DEV_APPS_URL = "/api/v2/devapps"

    MAX_RETRIES = 3

    async def get_app_data(self, triplet: AppTripletDto) -> Optional[AppDataDto]:
        url = self.make_full_url(self.APPDATA_URL)

        data = await self._make_request(request=self.session.get, url=url, params=triplet.asdict())
        return AppDataSchema().load(data)

    async def get_dev_context(self, triplet: AppTripletDto) -> Dict[str, DevContextAppDto]:
        url = self.make_full_url(self.DEV_CONTEXT_URL)

        data = await self._make_request(request=self.session.get, url=url, params=triplet.asdict())
        data = data.get("apps")
        return {ext_id: DevContextAppDto.make(app) for ext_id, app in data.items()}

    async def get_featured_posts(self, store: AppPagesStoreEnum, country: str) -> List[BlogPostDto]:
        params = {"store": store, "country": country}

        url = self.make_full_url(self.FEATURED_POSTS_URL.format(**params))

        data = await self._make_request(request=self.session.get, url=url, params=params)
        return BlogPostSchema(many=True).load(data.get("posts"))

    async def get_dev_name(self, store: AppPagesStoreEnum, country: str, dev_slug: str) -> DevNameDto:
        params = {
            "store": store,
            "dev_slug": dev_slug,
            "country": country,
        }
        url = self.make_full_url(self.DEV_NAME_URL.format(**params))

        data = await self._make_request(request=self.session.get, url=url)
        return DevNameSchema().load(data)

    async def get_blocked_apps(self) -> List[str]:
        url = self.make_full_url(self.BLOCKED_APPS_URL)
        data = await self._make_request(request=self.session.get, url=url)
        return data.get("blocked_apps", [])

    async def get_dev_apps(self, store: AppPagesStoreEnum, dev_slug: str, country: str) -> List[DevAppsDto]:
        params = {
            "store": store,
            "devslug": dev_slug,
            "country": country,
        }
        url = self.make_full_url(self.DEV_APPS_URL)
        data = await self._make_request(request=self.session.get, url=url, params=params)
        return DevAppsSchema(many=True).load(data.get("developer_apps")) if data else []

    async def _make_request(self, request: Callable, retries=MAX_RETRIES, **kwargs) -> dict:
        try:
            async with request(**kwargs) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data
        except ClientResponseError as e:
            app_logger.warning(f"Error during get_app_meta request: {e.args}")
            if retries > 0:
                return await self._make_request(request=request, retries=retries - 1, **kwargs)
