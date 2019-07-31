# -*- coding: utf-8 -*-
import enum
import os
from typing import Optional

import OpenLearn

config = {
    "development": "OpenLearn.settings.DevelopmentConfig",
    "testing": "OpenLearn.settings.TestingConfig",
    "production": "OpenLearn.settings.ProductionConfig",
    "default": "OpenLearn.settings.DevelopmentConfig"
}


class ConfigType(enum.Enum):
    Auto = 0
    Development = "development"
    Testing = "testing"
    Production = "production"

    @property
    def config(self):
        return {
            ConfigType.Development: lambda: DevelopmentConfig,
            ConfigType.Testing: lambda: TestingConfig,
            ConfigType.Production: lambda: ProductionConfig,
            ConfigType.Auto: lambda: ConfigType(os.getenv("FLASK_ENV", "development")).config
        }[self]()


class BaseConfig(object):
    CONFIG_FILE = "config.cfg"

    DEBUG = False
    TESTING = False
    VERSION = OpenLearn.__version__

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    VERSION = f"{OpenLearn.__version__} dev"


class TestingConfig(BaseConfig):
    CONFIG_FILE = "testing.cfg"

    DEBUG = False
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False
    BCRYPT_LOG_ROUNDS = 4


class ProductionConfig(BaseConfig):
    pass


def configure_app(app, config_type: ConfigType):
    app.config.from_object(config_type.config)
    app.config.from_pyfile(app.config["CONFIG_FILE"], silent=False)
