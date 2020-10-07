from dataclasses import dataclass

from common.base_dto import BaseDto


@dataclass
class FeatureDto(BaseDto):
    id: int
    is_active: bool
    feature_name: str
