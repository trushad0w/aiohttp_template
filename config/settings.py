from envparse import env


env.read_envfile()

DEBUG = env.bool("DEBUG", default=False)

# ---------------- DB example settings ------------------ #
DB_USER = env.str("DB_USER", default="user")
DB_PASSWORD = env.str("DB_PASSWORD", default="pass")
DB_HOST = env.str("DB_HOST", default="localhost")
DB_PORT = env.str("DB_PORT", default="27017")
DB_NAME = env.str("DB_NAME", default="admin")

MONGO_DSN = f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"

POSTGRESQL_DSN = env.str("POSTGRESQL_DSN")

MYSQL_DSN = env.str("MYSQL_DSN")

DATABASES = {
    "default": {
        "dsn": MONGO_DSN,
        "db": "mongodb",
        "max_pool_size": env.int("MAX_POOL_SIZE", default=1),
        "min_pool_size": env.int("MIN_POOL_SIZE", default=1),
        "db_name": DB_NAME,
    },
    "postgres": {
        "dsn": POSTGRESQL_DSN,
        "db": "postgresql",
        "max_pool_size": env.int("MAX_POOL_SIZE", default=1),
        "min_pool_size": env.int("MIN_POOL_SIZE", default=1),
    },
    "mysql": {
        "dsn": MYSQL_DSN,
        "db": "mysql",
        "max_pool_size": env.int("MAX_POOL_SIZE", default=1),
        "min_pool_size": env.int("MIN_POOL_SIZE", default=1),
    },
}

# ---------------- DB settings ------------------ #

LOG_LEVEL = env.str("LOG_LEVEL", default="INFO")
