from marshmallow import Schema, fields, EXCLUDE


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
