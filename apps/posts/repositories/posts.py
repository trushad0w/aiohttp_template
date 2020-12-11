from typing import List, Tuple, Optional

from apps.posts.models.posts import PostsDto
from common.db.mongo_db import mongo_connection


class PostsRepo:
    @staticmethod
    async def get_post_by_id(id: int) -> Optional[PostsDto]:
        data = await mongo_connection().posts.find_one({"id": id})

        return PostsDto.make(data) if data else None

    @staticmethod
    async def get_all_posts(limit: int, offset: int) -> Tuple[int, List[PostsDto]]:
        count = await mongo_connection().posts.count_documents({})
        posts = mongo_connection().posts.find({}).sort("_id").skip(offset).limit(limit)

        return count, [PostsDto.make(post) async for post in posts]
