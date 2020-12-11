from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Dict

from common.base_dto import BaseDto


class AppPagesStoreEnum(str, Enum):
    GOOGLE_PLAY = "android"
    AMAZON = "amazon"
    APP_STORE = "ios"

    def __str__(self):
        return self.value


@dataclass()
class ReviewsData(BaseDto):
    avg_rating_by_featured_reviews: float
    reply_rate: str
    reply_rate_negative_reviews_current_period: str
    reviews_number_30_days: int


@dataclass()
class AppDataDto(BaseDto):
    country: str
    icon: str
    title: str
    subtitle: str
    description: str
    tags: List[Dict[str, str]]
    categories: List[str]
    reviews_rating: float
    reviews_total: int
    price: str
    size: str
    last_update: datetime
    version: str
    screenshots: Dict[str, List[Dict[str, str]]]
    rating_list: List[int]
    reviews: List[Dict[str, str]]
    developer: str
    downloads: str
    developer_url: str
    developer_slug: str
    related_apps: List[str]
    reviews_data: ReviewsData

    def __post_init__(self):
        if isinstance(self.reviews_data, dict):
            self.reviews_data = ReviewsData.make(self.reviews_data)


@dataclass()
class DevContextAppDto(BaseDto):
    url: str
    icon: str
    title: str
    categories: List[str]


@dataclass()
class BlogPostDto(BaseDto):
    title: str
    subtitle: str
    url: str
    preview_image: str


@dataclass()
class DevNameDto(BaseDto):
    dev_slug: str
    developer: str


@dataclass()
class DevAppsDto(BaseDto):
    title: str
    icon: str
    categories: List[str]
    url: str
    developer_url: str
    developer: str


@dataclass
class AppTripletDto(BaseDto):
    store: AppPagesStoreEnum
    ext_id: str
    country: str
