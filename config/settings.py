from config.remote_config import set_env_vars

set_env_vars()

from envparse import env


env.read_envfile()

DEBUG = env.bool("DEBUG", default=False)

# ---------------- DB example settings ------------------ #
DB_USER = env.str("DB_USER", default="user")
DB_PASSWORD = env.str("DB_PASSWORD", default="pass")
DB_HOST = env.str("DB_HOST", default="localhost")
DB_PORT = env.str("DB_PORT", default="27017")
DB_NAME = env.str("DB_NAME", default="test")

MONGO_DSN = f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"

POSTGRESQL_DSN = env.str("POSTGRESQL_DSN")

MYSQL_DSN = env.str("MYSQL_DSN")

POOL_DEFAULT_NAME = "default"

MONGO_DATABASES = {
    POOL_DEFAULT_NAME: {
        "dsn": MONGO_DSN,
        "max_pool_size": env.int("MAX_POOL_SIZE", default=1),
        "min_pool_size": env.int("MIN_POOL_SIZE", default=0),
        "db_name": DB_NAME,
    },
    "secondary": {
        "dsn": MONGO_DSN,
        "max_pool_size": env.int("MAX_POOL_SIZE", default=1),
        "min_pool_size": env.int("MIN_POOL_SIZE", default=0),
        "db_name": f"{DB_NAME}_helper",
    },
}

MYSQL_DATABASES = {
    POOL_DEFAULT_NAME: {
        "dsn": MYSQL_DSN,
        "max_pool_size": env.int("MAX_POOL_SIZE", default=1),
        "min_pool_size": env.int("MIN_POOL_SIZE", default=0),
    },
}

POSTGRESQL_DATABASES = {
    POOL_DEFAULT_NAME: {
        "dsn": POSTGRESQL_DSN,
        "max_pool_size": env.int("MAX_POOL_SIZE", default=1),
        "min_pool_size": env.int("MIN_POOL_SIZE", default=0),
    },
}

# ---------------- DB settings ------------------ #

LOG_LEVEL = env.str("LOG_LEVEL", default="INFO")


# ------------- External services ------------ #

APP_PAGES_API_URL = env.str("APP_PAGES_API_URL", default="http://localhost:8000")

# ------------- External services ------------ #
