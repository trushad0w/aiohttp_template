from common.health_check import health_check


def setup_routes(app):
    app.router.add_get("/", health_check, name="health_check")
