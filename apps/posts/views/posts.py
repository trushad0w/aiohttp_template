from apps.posts.schemas.posts import (
    PostResponseSchema,
    AllPostsRequestSchema,
    PostFeaturesResponseSchema,
    SinglePostRequestSchema,
)
from common.api import definition, response_error, request_query, response_pagination, response
from apps.posts.services.posts import PostsService


@definition(
    path="/posts/all",
    responses={
        "200": response_pagination(PostResponseSchema),
        "4xx": response_error(),
        "5xx": response_error(),
    },
    request_query=request_query(AllPostsRequestSchema),
    methods=["GET"],
    tags=["posts"],
    description="Get all posts",
)
async def get_all_posts(request):
    offset = request["query"].get("offset")
    limit = request["query"].get("limit")
    count, posts = await PostsService.get_all_posts(limit=limit, offset=offset)
    return {"pagination": {"limit": limit, "offset": offset, "total": count}, "items": posts}


@definition(
    path="/post",
    responses={
        "200": response(PostFeaturesResponseSchema),
        "4xx": response_error(),
        "5xx": response_error(),
    },
    request_query=request_query(SinglePostRequestSchema),
    methods=["GET"],
    tags=["posts"],
    description="Get all posts",
)
async def get_post_and_features(request):
    post_id = request["query"].get("id")
    fetch_non_active = request["query"].get("fetch_non_active")
    post, features = await PostsService.get_post_and_features(
        post_id=post_id, fetch_non_active=fetch_non_active
    )
    return {"post": post, "features": features}
