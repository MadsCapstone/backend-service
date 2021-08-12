"""Config settings for for development, testing and production environments."""
import os
from pathlib import Path


HERE = Path(__file__).parent
FLASK_APP_DIR = HERE.parent.parent
SQLITE_DEV = "sqlite:///" + str(FLASK_APP_DIR / "backend_api_dev.db")
SQLITE_TEST = "sqlite:///" + str(FLASK_APP_DIR / "backend_api_test.db")
SQLITE_PROD = "sqlite:///" + str(FLASK_APP_DIR / "backend_api_prod.db")
CLOUDSQL_LOCAL = f"postgresql://{os.getenv('DB_USER', None)}:{os.getenv('DB_PASS', None)}@0.0.0.0:5432/{os.getenv('DB_NAME', None)}"
CLOUDSQL_PROD = f"postgresql://{os.getenv('DB_USER', None)}:{os.getenv('DB_PASS', None)}@localhost:5432/{os.getenv('DB_NAME',None)}"
MIGRATIONS = os.path.join(FLASK_APP_DIR, 'migrations')


class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "open sesame")
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRE_HOURS = 0
    TOKEN_EXPIRE_MINUTES = 0
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SWAGGER_UI_DOC_EXPANSION = "list"
    RESTX_MASK_SWAGGER = False
    JSON_SORT_KEYS = False
    MIGRATIONS_FOLDER = os.getenv("MIGRATIONS_DIR", MIGRATIONS)


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = SQLITE_TEST


class DevelopmentConfig(Config):
    """Development configuration."""
    TOKEN_EXPIRE_MINUTES = 15
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", SQLITE_DEV)

class CloudNonProduction(Config):
    TOKEN_EXPIRE_HOURS = 20
    SQLALCHEMY_DATABASE_URI = os.getenv("CLOUD_NP_DATABASE_URL")

class LocalProductionConfig(Config):
    """Local Connection Details For """
    TOKEN_EXPIRE_HOURS = 1
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = CLOUDSQL_LOCAL
    PRESERVE_CONTEXT_ON_EXCEPTION = True

class ProductionConfig(Config):
    """Production configuration."""
    TOKEN_EXPIRE_HOURS = 1
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = CLOUDSQL_PROD
    PRESERVE_CONTEXT_ON_EXCEPTION = True


ENV_CONFIG_DICT = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig, localprod=LocalProductionConfig
)


def get_config(config_name):
    """Retrieve environment configuration settings."""
    return ENV_CONFIG_DICT.get(config_name, ProductionConfig)
