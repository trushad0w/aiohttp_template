from os import environ
from typing import Dict

from consul import Consul
from envparse import env

from common.logger import app_logger

env.read_envfile()

CONSUL_HOST = env.str("CONSUL_HOST", default="")
CONSUL_TOKEN = env.str("CONSUL_TOKEN", default="")
CONSUL_SCHEME = env.str("CONSUL_SCHEME", default="")
CONSUL_PORT = env.int("CONSUL_PORT", default=8500)
CONSUL_DC = env.str("CONSUL_DC", default="")
CONSUL_PREFIX = env.str("CONSUL_PREFIX", default="")


def get_config():
    try:
        client = Consul(
            host=CONSUL_HOST,
            token=CONSUL_TOKEN,
            dc=CONSUL_DC,
            port=CONSUL_PORT,
            scheme=CONSUL_SCHEME,
        )

        _, values = client.kv.get(key=f"{CONSUL_PREFIX}", recurse=True)

        _config = {
            value["Key"].replace(f"{CONSUL_PREFIX}/", ""): value["Value"].decode()
            for value in values
            if value["Key"] != f"{CONSUL_PREFIX}/"
        }

        return _config
    except Exception as e:
        app_logger.error(f"Error parsing config from consul: {e.args}")

        return {}


def _put_values(values: Dict[str, str]):
    client = Consul(
        host=CONSUL_HOST,
        token=CONSUL_TOKEN,
        dc=CONSUL_DC,
        port=CONSUL_PORT,
        scheme=CONSUL_SCHEME,
    )
    for key, value in values.items():
        client.kv.put(f"{CONSUL_PREFIX}/{key}", value, dc=CONSUL_DC, token=CONSUL_TOKEN)


def set_env_vars():
    try:
        client = Consul(
            host=CONSUL_HOST,
            token=CONSUL_TOKEN,
            dc=CONSUL_DC,
            port=CONSUL_PORT,
            scheme=CONSUL_SCHEME,
        )

        _, values = client.kv.get(key=f"{CONSUL_PREFIX}", recurse=True)

        if isinstance(values, list):
            _config = {
                value["Key"].replace(f"{CONSUL_PREFIX}/", ""): value["Value"].decode()
                for value in values
                if value["Key"] != f"{CONSUL_PREFIX}/"
            }

            for key, value in _config.items():
                environ[key] = value
    except Exception as e:
        app_logger.error(f"Error parsing config from consul: {e.args}")
