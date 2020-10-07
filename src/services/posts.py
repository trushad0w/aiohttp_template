import asyncio
from typing import Tuple, List

from src.models.features import FeatureDto
from src.models.posts import PostsDto
from src.repositories.features import FeaturesRepo
from src.repositories.posts import PostsRepo


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
