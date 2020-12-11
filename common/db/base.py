from dataclasses import dataclass
from typing import Optional

from common.base_dto import BaseDto
from common.exceptions import InitException


@dataclass
class DbOptions(BaseDto):
    dsn: str
    max_pool_size: int
    min_pool_size: int
    db_name: Optional[str] = None

    def __post_init__(self):
        if not self.dsn:
            raise InitException(
                f"Error on db init - dsn should be provided, your params are : {self.asdict()}"
            )
        if not self.max_pool_size or self.min_pool_size < 0:
            self.max_pool_size = 1
        if not self.min_pool_size or self.min_pool_size <= 0:
            self.min_pool_size = 0
