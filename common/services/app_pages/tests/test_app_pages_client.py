import pytest
from pytest_mock import MockFixture

from common.services.app_pages.client import AppPagesClient
from common.services.app_pages.models import (
    AppTripletDto,
    AppPagesStoreEnum,
    AppDataDto,
    DevContextAppDto,
    BlogPostDto,
)
from common.services.app_pages.tests.mocks.app_data import APP_DATA_MOCK
from common.services.client import ClientSession
from common.test_utils.client_response_mock import MockClientResponse


@pytest.mark.parametrize(
    "result",
    [APP_DATA_MOCK, {}],
)
async def test_get_app_data(mocker: MockFixture, result):
    async def _request(_, method, url, **kwargs):
        response = result
        return MockClientResponse(200, response)

    mocker.patch.object(ClientSession, "_request", _request)
    app_pages = AppPagesClient("")
    response = await app_pages.get_app_data(
        triplet=AppTripletDto(
            store=AppPagesStoreEnum.GOOGLE_PLAY,
            ext_id="com.test.test",
            country="us",
        )
    )
    assert isinstance(response, AppDataDto), "response is not correct"


@pytest.mark.parametrize(
    "result",
    [
        {
            "developer_apps": [
                {
                    "url": "/ios/venmo-send-receive-money/351727428?country=us",
                    "developer_url": "https://apps.apple.com/us/developer/venmo/id351727431",
                    "categories": ["Finance", "Utilities"],
                    "developer": "Venmo",
                    "title": "Venmo",
                    "icon": "https://is5-ssl.mzstatic.com/image/400x400.png",
                }
            ]
        },
        {"developer_apps": []},
    ],
)
async def test_get_dev_apps(mocker: MockFixture, result):
    async def _request(_, method, url, **kwargs):
        response = result
        return MockClientResponse(200, response)

    mocker.patch.object(ClientSession, "_request", _request)
    app_pages = AppPagesClient("")
    response = await app_pages.get_dev_apps(
        store=AppPagesStoreEnum.GOOGLE_PLAY, dev_slug="test", country="us"
    )
    assert len(response) == len(result.get("developer_apps")), "dev apps are empty"


@pytest.mark.parametrize(
    "result",
    [
        {
            "blocked_apps": [
                "692885364",
                "1164067996",
            ]
        },
        {"blocked_apps": []},
    ],
)
async def test_get_blocked_apps(mocker: MockFixture, result):
    async def _request(_, method, url, **kwargs):
        response = result
        return MockClientResponse(200, response)

    mocker.patch.object(ClientSession, "_request", _request)
    app_pages = AppPagesClient("")
    blocked = await app_pages.get_blocked_apps()
    assert len(blocked) == len(result.get("blocked_apps")), "blocked apps are empty"


@pytest.mark.parametrize(
    "result",
    [
        {
            "apps": {
                "351727428": {
                    "url": "/ios/preloaded/351727428?country=us",
                    "icon": "https://is5-ssl.mzstatic.com/image/thumb/400x400.png",
                    "title": "Venmo",
                    "categories": ["Finance", "Utilities"],
                }
            }
        },
        {"apps": {}},
    ],
)
async def test_get_dev_context(mocker: MockFixture, result):
    async def _request(_, method, url, **kwargs):
        response = result
        return MockClientResponse(200, response)

    mocker.patch.object(ClientSession, "_request", _request)
    app_pages = AppPagesClient("")
    dev_context = await app_pages.get_dev_context(
        triplet=AppTripletDto(
            store=AppPagesStoreEnum.GOOGLE_PLAY,
            ext_id="com.test.test",
            country="us",
        )
    )
    assert len(dev_context.values()) == len(result.get("apps")), "dev context is empty"
    for ext_id, context in dev_context.items():
        assert isinstance(context, DevContextAppDto), "context object is wrong"


@pytest.mark.parametrize(
    "result",
    [
        {
            "posts": [
                {
                    "title": "Holiday Marketing Guide by AppFollow and MoEngage",
                    "url": "https://appfollow.io/blog/holiday-marketing-guide-by-appfollow-and-moengage?utm_source=apppages",
                    "subtitle": "AppFollow and MoEngage released a guide for building a comprehensive holiday marketing strategy. Examples from Amazon, Ozon, AliExpress, Jam City and others.",
                    "preview_image": "https://appfollow.io/blog/static/appfollow_53851450-ee17-491f-918c-3ce6a22ddc25.jpg",
                },
            ]
        },
        {"posts": []},
    ],
)
async def test_get_featured_posts(mocker: MockFixture, result):
    async def _request(_, method, url, **kwargs):
        response = result

        return MockClientResponse(200, response)

    mocker.patch.object(ClientSession, "_request", _request)
    app_pages = AppPagesClient("")
    posts = await app_pages.get_featured_posts(store=AppPagesStoreEnum.GOOGLE_PLAY, country="us")
    assert len(posts) == len(result.get("posts"))
    for item in posts:
        assert isinstance(item, BlogPostDto)
