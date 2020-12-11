from apps.posts.models.posts import PostsDto
from apps.posts.tests.fixtures.posts_and_features import create_posts_and_features
from common.db.mongo_db import mongo_connection


async def test_all_posts(client):
    await create_posts_and_features()
    res = await client.get("/template_api/posts/all")
    assert res.status == 200, "Posts completed unsuccessfully"

    data = (await res.json()).get("result")

    assert len(data) > 0, "result is empty"


async def test_post(client):
    await create_posts_and_features()
    post_from_db = PostsDto.make(await mongo_connection().posts.find_one({}))

    res = await client.get("/template_api/post", params={"id": post_from_db.id})
    assert res.status == 200, "Posts completed unsuccessfully"

    data = (await res.json()).get("result")

    for k, v in data.get("post").items():
        assert v == post_from_db.__getattribute__(k), "result from api differs from result from db"
