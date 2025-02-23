import os
from pathlib import Path

base_dir = Path(__name__).parent.parent

class Config:



    SECRET_KEY = os.environ.get("SECRET_KEY", 'default-secret-key')

    @staticmethod
    def init_app(app):

        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = True


config = {
    "development": DevelopmentConfig,
    "testing": TestConfig,
    "production": ProductionConfig,
}
