from common import db
from src.models.features import FeatureDto


class FeaturesRepo:
    @staticmethod
    async def get_features(fetch_non_active: bool):
        condition = ""
        if not fetch_non_active:
            condition = "where is_active = true"
        query = f"select * from features {condition}"

        return [FeatureDto.make(feature) for feature in await db.connection("postgres").fetch(query)]
