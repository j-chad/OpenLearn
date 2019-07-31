# -*- coding: utf-8 -*-
import configparser
import pathlib
import unittest

import OpenLearn


class TestApp(unittest.TestCase):
    def test_version_number(self):
        """Ensure the version is the same everywhere"""
        config_path = pathlib.Path(OpenLearn.__file__).parent.parent / "pyproject.toml"
        parser = configparser.ConfigParser()
        parser.read(config_path)
        version_number_config_file = parser["tool.poetry"]["version"].strip('"')
        self.assertEqual(version_number_config_file, OpenLearn.__version__)
