import asyncio
from typing import List, Tuple, Optional

from asyncpg import Connection
from asyncpg.pool import Pool

from common import db
from src.models.posts import PostsDto


class PostsRepo:
    @staticmethod
    async def get_post_by_id(id: int) -> Optional[PostsDto]:
        query = """
            select * from posts where id = $1
        """

        data = await db.connection("postgres").fetchrow(query, id)

        return PostsDto.make(data) if data else None

    @staticmethod
    async def get_all_posts(limit: int, offset: int) -> Tuple[int, List[PostsDto]]:
        query = "select * from posts limit $1 offset $2"
        count_query = "select count(*) from posts"

        count, posts = await asyncio.gather(
            db.connection("postgres").fetchval(count_query),
            db.connection("postgres").fetch(query, limit, offset),
        )
        return count, [PostsDto.make(post) for post in posts]
