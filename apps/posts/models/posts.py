from dataclasses import dataclass

import ujson

from common.base_dto import BaseDto


@dataclass
class PostsDto(BaseDto):
    id: int
    title: str
    content: str
    additional_data: dict

    def __post_init__(self):
        if isinstance(self.additional_data, str):
            self.additional_data = ujson.loads(self.additional_data)
