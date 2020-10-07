from marshmallow import Schema, fields, EXCLUDE

from common.api import definition, response_error, request_query, response_pagination, response
from src.services.posts import PostsService


class AllPostsRequestSchema(Schema):
    limit = fields.Int(required=False, missing=10)
    offset = fields.Int(required=False, missing=0)

    class Meta:
        unknown = EXCLUDE


class PostResponseSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    content = fields.Str()

    class Meta:
        unknown = EXCLUDE


class AllPostsResponseSchema(Schema):
    items = fields.Nested(PostResponseSchema, many=True)

    class Meta:
        unknown = EXCLUDE


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


class SinglePostRequestSchema(Schema):
    id = fields.Int(required=True)
    fetch_non_active = fields.Bool(required=False, missing=False)

    class Meta:
        unknown = EXCLUDE


class FeatureSchema(Schema):
    id = fields.Int()
    is_active = fields.Bool()
    feature_name = fields.Str()

    class Meta:
        unknown = EXCLUDE


class PostFeaturesResponseSchema(Schema):
    post = fields.Nested(PostResponseSchema)
    features = fields.Nested(FeatureSchema, many=True)

    class Meta:
        unknown = EXCLUDE


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
