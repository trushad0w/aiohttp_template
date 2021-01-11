import os
import platform
from abc import ABC
from typing import Optional, Union, Callable

import aiohttp
import ujson
from aiohttp import BasicAuth, ClientResponseError

from common.logger import app_logger


class ClientSession(aiohttp.ClientSession):
    async def _request(self, method, url, **kwargs):

        if kwargs.get("params"):
            kwargs["params"] = self._prepare_params(kwargs["params"])

        if kwargs.get("json"):
            kwargs["json"] = self._prepare_json(kwargs["json"])

        return await super()._request(method, url, **kwargs)

    @staticmethod
    def _prepare_params(params: Union[list, dict]):

        if isinstance(params, list):
            return [(x[0], str(x[1])) for x in params if x[1] is not None]

        return {
            k: ",".join(map(str, list(v)))
            if isinstance(
                v,
                (
                    list,
                    set,
                    tuple,
                ),
            )
            else str(v)
            for k, v in params.items()
            if v is not None
        }

    @staticmethod
    def _prepare_json(data: Union[dict, list]) -> Union[dict, list]:
        if not isinstance(data, dict):
            return data

        return {
            k: list(v)
            if isinstance(
                v,
                (
                    list,
                    set,
                    tuple,
                ),
            )
            else v
            for k, v in data.items()
        }


class ServiceClient(ABC):
    DEFAULT_MAX_RETRIES = 0

    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.logger = app_logger
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.username = username
        self.password = password
        self.session = self.create_client_session()

    async def dispose(self):
        await self.session.close()

    def create_client_session(self):
        return ClientSession(
            headers=self.get_default_headers(),
            auth=self.get_http_auth(),
            json_serialize=ujson.dumps,
        )

    def get_default_headers(self) -> dict:
        return {
            "accept": "application/json",
            "cache-control": "no-cache",
            "user-agent": self.get_user_agent(),
        }

    def get_user_agent(self) -> str:
        software = aiohttp.http.SERVER_SOFTWARE.replace(" ", "; ")
        return f"{os.getenv('HOSTNAME') or platform.node()}; client/app-pages; {software}"

    def get_http_auth(self):
        if self.username is not None and self.password is not None:
            return BasicAuth(self.username, self.password)

    def make_full_url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    async def _make_request(self, request: Callable, retries=DEFAULT_MAX_RETRIES, **kwargs) -> dict:
        try:
            async with request(**kwargs) as resp:
                resp.raise_for_status()
                return resp
        except ClientResponseError as e:
            app_logger.warning(f"Error during external request: {e.args}")
            if retries > 0 and e.status >= 500:
                return await self._make_request(request=request, retries=retries - 1, **kwargs)
            else:
                raise e
