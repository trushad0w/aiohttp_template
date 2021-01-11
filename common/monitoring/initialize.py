import prometheus_client

from common.monitoring.handler import metrics
from common.monitoring.middleware import monitor_middleware


def setup_metrics(app, app_name):
    app["REQUEST_COUNT"] = prometheus_client.Counter(
        "requests_total", "Total Request Count", ["app_name", "method", "endpoint", "http_status"]
    )
    app["REQUEST_LATENCY"] = prometheus_client.Histogram(
        "request_latency_seconds", "Request latency", ["app_name", "endpoint"]
    )

    app["REQUEST_IN_PROGRESS"] = prometheus_client.Gauge(
        "requests_in_progress_total", "Requests in progress", ["app_name", "endpoint", "method"]
    )

    app.middlewares.insert(0, monitor_middleware(app_name))
    app.router.add_get("/metrics", metrics)
