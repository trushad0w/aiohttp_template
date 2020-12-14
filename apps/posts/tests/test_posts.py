from asynctest import CoroutineMock
from pytest_mock import MockFixture, pytest

from apps.posts.models.features import FeatureDto
from apps.posts.models.posts import PostsDto
from apps.posts.services.posts import PostsService
from apps.posts.tests.fixtures.posts_and_features import create_posts_and_features
from common.db.mongo_db import mongo_connection
from common.services.app_pages.client import AppPagesClient
from common.services.app_pages.models import BlogPostDto


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


async def test_get_all_posts_service():
    await create_posts_and_features()
    posts = [PostsDto.make(post) async for post in mongo_connection().posts.find({})]
    _, service_data = await PostsService.get_all_posts(offset=0, limit=len(posts))
    assert posts == service_data, "Data from DB do not match with data from service"


async def test_posts_and_features_service():
    await create_posts_and_features()
    post = PostsDto.make(await mongo_connection().posts.find_one({}))
    features = [FeatureDto.make(feature) async for feature in mongo_connection().features.find({})]
    post_from_service, features_from_service = await PostsService.get_post_and_features(
        post_id=post.id, fetch_non_active=True
    )

    assert post == post_from_service, "Post from service didn't match post from DB"
    assert features == features_from_service, "Features from service didn't match features from DB"


@pytest.mark.parametrize(
    "posts",
    [
        [
            BlogPostDto(
                title="test",
                subtitle="test",
                url="test",
                preview_image="test",
            )
        ],
        [],
    ],
)
async def test_external_service_example(mocker: MockFixture, posts):

    mocker.patch.object(AppPagesClient, "get_featured_posts", CoroutineMock(return_value=posts))

    data = await PostsService.external_service_example()
    assert posts == data
