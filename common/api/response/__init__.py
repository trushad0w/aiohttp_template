import ujson
from aiohttp import web


def make_response(payload, *, status: int, headers: dict = None) -> web.Response:
    payload = ujson.dumps(payload, ensure_ascii=False)
    return web.Response(
        text=payload,
        status=status,
        headers=headers,
        content_type="application/json",
        charset="utf-8",
    )
