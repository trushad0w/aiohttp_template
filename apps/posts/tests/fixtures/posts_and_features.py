import asyncio

from apps.posts.models.features import FeatureDto
from apps.posts.models.posts import PostsDto
from common.db.mongo_db import mongo_connection


async def create_posts_and_features():
    feature, post = await asyncio.gather(
        mongo_connection().features.find_one({}), mongo_connection().posts.find_one({})
    )

    if feature or post:
        raise Exception("DB is not empty")

    posts = [
        PostsDto(id=i, title=f"title{i}", content=f"content{i}", additional_data={"data": f"test{i}"})
        for i in range(10)
    ]
    features = [
        FeatureDto(
            id=i,
            is_active=True,
            feature_name=f"feature{i}",
        )
        for i in range(5)
    ]

    await asyncio.gather(
        mongo_connection().posts.insert_many([record.asdict() for record in posts]),
        mongo_connection().features.insert_many([record.asdict() for record in features]),
    )
