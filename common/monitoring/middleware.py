import asyncio
import time


def monitor_middleware(app_name):
    @asyncio.coroutine
    def factory(app, handler):
        @asyncio.coroutine
        def middleware_handler(request):
            request["start_time"] = time.perf_counter_ns()
            request.app["REQUEST_IN_PROGRESS"].labels(app_name, request.path, request.method).inc()
            response = yield from handler(request)
            resp_time = (time.perf_counter_ns() - request["start_time"]) / 10 ** 9
            request.app["REQUEST_LATENCY"].labels(app_name, request.path).observe(resp_time)
            request.app["REQUEST_IN_PROGRESS"].labels(app_name, request.path, request.method).dec()
            request.app["REQUEST_COUNT"].labels(app_name, request.method, request.path, response.status).inc()
            return response

        return middleware_handler

    return factory
