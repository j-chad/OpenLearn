# -*- coding: utf-8 -*-
import enum
import os
from typing import Optional

import OpenLearn


class ConfigType(enum.Enum):
    Auto = 0
    Development = "development"
    Testing = "testing"
    Production = "production"

    @property
    def config(self):
        return {
            ConfigType.Development: lambda: "OpenLearn.settings.DevelopmentConfig",
            ConfigType.Testing: lambda: "OpenLearn.settings.TestingConfig",
            ConfigType.Production: lambda: "OpenLearn.settings.ProductionConfig",
            ConfigType.Auto: lambda: ConfigType(os.getenv("FLASK_ENV", "development")).config
        }[self]()


class BaseConfig(object):
    CONFIG_FILE = "config.cfg"

    DEBUG = False
    TESTING = False
    VERSION = OpenLearn.__version__

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = True
    VERSION = f"{OpenLearn.__version__} dev"


class TestingConfig(BaseConfig):
    CONFIG_FILE = "testing.cfg"

    ENV = "testing"
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False
    BCRYPT_LOG_ROUNDS = 4


class ProductionConfig(BaseConfig):
    pass


def configure_app(app, config_type: ConfigType):
    app.config.from_object(config_type.config)
    app.config.from_pyfile(app.config["CONFIG_FILE"], silent=False)
