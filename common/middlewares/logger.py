import traceback

from aiohttp import web
from aiohttp.web_middlewares import middleware

from common.exceptions import ApiException
from config.logger import app_logger


@middleware
async def logger_middleware(request, handler):
    try:
        response = await handler(request)
        return response
    except ApiException as e:
        app_logger.warning(e.message)
        return web.json_response(status=e.code, data={"error": e.message})
    except Exception:
        message = traceback.format_exc()
        app_logger.critical(f"path: {request.raw_path} , {message}")
        return web.json_response(status=500, data={"error": "Unhandled error occurred, try again later"})
