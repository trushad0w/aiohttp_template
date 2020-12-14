from aiohttp import ClientError
from typing import Dict


class MockClientResponse:
    def __init__(self, status: int, data: Dict):
        self.status = status
        self._data = data

    async def json(self):
        return self._data

    def raise_for_status(self):
        if self.status >= 400:
            raise ClientError()

    def release(self):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
