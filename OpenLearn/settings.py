# -*- coding: utf-8 -*-
import os
import OpenLearn

config = {
    "development": "OpenLearn.settings.DevelopmentConfig",
    "testing": "OpenLearn.settings.TestingConfig",
    "production": "OpenLearn.settings.ProductionConfig",
    "default": "OpenLearn.settings.DevelopmentConfig"
}


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    VERSION = OpenLearn.__version__


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    VERSION = f"{OpenLearn.__version__} dev"


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True


class ProductionConfig(BaseConfig):
    pass


def configure_app(app):
    config_name = os.getenv("FLASK_ENV", "default")
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)
