"""
Initial migration
"""
from apps.posts.models.features import FeatureDto
from apps.posts.models.posts import PostsDto

name = "20201112_init"
dependencies = []


def upgrade(db):
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
    db.posts.insert_many([record.asdict() for record in posts])
    db.features.insert_many([record.asdict() for record in features])
