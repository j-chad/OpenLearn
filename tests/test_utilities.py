import os
import unittest
from unittest import mock

from OpenLearn import settings


class TestSettingsUtilities(unittest.TestCase):
    @mock.patch.dict(os.environ, {'FLASK_ENV': 'development'})
    def test_config_type_auto_resolution_development(self):
        self.assertIs(settings.ConfigType.Auto.config, settings.DevelopmentConfig)

    @mock.patch.dict(os.environ, {'FLASK_ENV': 'production'})
    def test_config_type_auto_resolution_production(self):
        self.assertIs(settings.ConfigType.Auto.config, settings.ProductionConfig)

    @mock.patch.dict(os.environ, {'FLASK_ENV': 'testing'})
    def test_config_type_auto_resolution_testing(self):
        self.assertIs(settings.ConfigType.Auto.config, settings.TestingConfig)
