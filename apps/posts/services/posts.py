import asyncio
from typing import Tuple, List

from apps.posts.models.features import FeatureDto
from apps.posts.models.posts import PostsDto
from apps.posts.repositories.features import FeaturesRepo
from apps.posts.repositories.posts import PostsRepo
from common import services
from common.services.app_pages.client import AppPagesClient
from common.services.app_pages.models import AppPagesStoreEnum


class PostsService:
    @classmethod
    async def get_all_posts(cls, limit: int, offset: int) -> Tuple[int, List[PostsDto]]:
        return await PostsRepo.get_all_posts(limit=limit, offset=offset)

    @classmethod
    async def get_post_and_features(
        cls, post_id: int, fetch_non_active: bool
    ) -> Tuple[PostsDto, List[FeatureDto]]:
        posts, features = await asyncio.gather(
            PostsRepo.get_post_by_id(id=post_id), FeaturesRepo.get_features(fetch_non_active=fetch_non_active)
        )
        # Here might be some app business logic
        return posts, features

    @classmethod
    async def external_service_example(cls):
        app_pages_client: AppPagesClient = services.get_client(AppPagesClient)
        data = await app_pages_client.get_featured_posts(store=AppPagesStoreEnum.GOOGLE_PLAY, country="us")
        return data
