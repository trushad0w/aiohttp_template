import logging
from logging.config import dictConfig


def init_logger(log_level: str):
    log_conf = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "format": '{"logtime": "%(asctime)s.%(msecs)03d", '
                '"loglevel": "%(levelname)s", '
                '"logger": "%(name)s", '
                '"extra": {"filename": "%(filename)s", '
                '"funcName": "%(funcName)s", "lineno": %(lineno)d, "logmessage": %(message)s}}',
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "console": {
                "level": log_level,
                "class": "logging.StreamHandler",
                "formatter": "default",
            }
        },
        "loggers": {"main": {"handlers": ("console",), "level": "DEBUG", "propagate": True}},
    }
    dictConfig(log_conf)


app_logger = logging.getLogger("main")
