from marshmallow import Schema, fields, post_load, EXCLUDE

from common.services.app_pages.models import AppDataDto, BlogPostDto, DevNameDto, DevAppsDto


class DeveloperReviewResponseSchema(Schema):
    text = fields.Str()
    date = fields.Str()

    class Meta:
        unknown = EXCLUDE


class ReviewsSchema(Schema):
    text = fields.Str()
    name = fields.Str()
    date = fields.Str()
    rating = fields.Int()
    developer_response = fields.Nested(DeveloperReviewResponseSchema)

    class Meta:
        unknown = EXCLUDE


class ScreenShotListElementSchema(Schema):
    view = fields.Str()
    full = fields.Str()

    class Meta:
        unknown = EXCLUDE


class ScreenShotSchema(Schema):
    id = fields.Str()
    list = fields.Nested(ScreenShotListElementSchema, many=True)
    name = fields.Str()

    class Meta:
        unknown = EXCLUDE


class TagsSchema(Schema):
    label = fields.Str()

    class Meta:
        unknown = EXCLUDE


class ReviewsDataSchema(Schema):
    reviews_number_30_days = fields.Str()
    avg_rating_by_featured_reviews = fields.Str()
    reply_rate = fields.Str()
    reply_rate_negative_reviews_current_period = fields.Str()

    class Meta:
        unknown = EXCLUDE


class AppDataSchema(Schema):
    reviews = fields.Nested(ReviewsSchema, many=True)
    last_update = fields.Str()
    subtitle = fields.Str()
    url = fields.Str()
    reviews_rating = fields.Float()
    rating_list = fields.List(fields.Int(), missing=[])
    icon = fields.Str()
    screenshots = fields.Nested(ScreenShotSchema, many=True, missing=[])
    reviews_total = fields.Method()
    downloads = fields.Str()
    categories = fields.List(fields.Str(), missing=[])
    related_apps = fields.List(fields.Str(), missing=[])
    description = fields.Str()
    developer = fields.Str()
    developer_slug = fields.Str()
    version = fields.Str()
    size = fields.Method()
    permalink = fields.Method()
    developer_url = fields.Str()
    tags = fields.Nested(TagsSchema, many=True)
    price = fields.Str()
    reviews_data = fields.Nested(ReviewsDataSchema)
    title = fields.Str()
    score = fields.Int()
    default_country = fields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load()
    def make_model(self, data, **kwargs) -> AppDataDto:
        return AppDataDto.make(data)


class BlogPostSchema(Schema):
    title = fields.Str()
    subtitle = fields.Str()
    url = fields.Str()
    preview_image = fields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load()
    def make_model(self, data, **kwargs) -> BlogPostDto:
        return BlogPostDto.make(data)


class DevNameSchema(Schema):
    dev_slug = fields.Str()
    developer = fields.Str()

    class Meta:
        unknown = EXCLUDE

    @post_load()
    def make_model(self, data, **kwargs) -> DevNameDto:
        return DevNameDto.make(data)


class DevAppsSchema(Schema):
    title = fields.Str()
    icon = fields.Str()
    categories = fields.List(fields.Str(), missing=[])
    url = fields.Str()
    developer_url = fields.Str()
    developer = fields.Str()

    @post_load()
    def make_model(self, data, **kwargs) -> DevAppsDto:
        return DevAppsDto.make(data)
