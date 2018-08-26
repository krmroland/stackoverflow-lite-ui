import sys
from os import getenv, path
from dotenv import load_dotenv


# load environment variables
env_path = path.abspath(".env")

if not path.exists(env_path):  # pragma: no cover
    print("A .env configuration file was not found in your root project")
    sys.exit(0)

load_dotenv(verbose=True, dotenv_path=env_path)


class Configuration:
    """Common configuration for all environments """
    DB_NAME = getenv("DB_NAME")
    SECRET = getenv("APP_KEY")


class TestConfiguration(Configuration):
    """Configuration for the test environment"""
    TESTING = True
    DB_NAME = getenv("TEST_DB_NAME")


class DevelopmentConfiguration(Configuration):
    """Configuration for Development Environment"""
    pass


class ProductionConfiguration(Configuration):
    """Configuration for Development Environment"""
    pass


config = {
    "development": DevelopmentConfiguration,
    "testing": TestConfiguration,
    "production": ProductionConfiguration
}
