from typing import List

from apps.posts.models.features import FeatureDto
from common.db.mongo_db import mongo_connection


class FeaturesRepo:
    @staticmethod
    async def get_features(fetch_non_active: bool) -> List[FeatureDto]:
        condition = {}
        if not fetch_non_active:
            condition = {"is_active": True}

        return [FeatureDto.make(feature) async for feature in mongo_connection().features.find(condition)]
