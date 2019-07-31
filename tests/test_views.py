# -*- coding: utf-8 -*-
import unittest

import flask_login
from flask import url_for
from flask_testing import TestCase

from OpenLearn import settings, database
from OpenLearn.app import create_app
from OpenLearn.extensions import db


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app(config=settings.ConfigType.Testing)
        app.testing = True
        return app

    def setUp(self):
        db.create_all()
        self.user = database.User(username="testUser", password="password@123")

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestPublicView(BaseTestCase):
    def test_index_page(self):
        response = self.client.get(url_for('public.index'))
        self.assert200(response)
        self.assertTrue(flask_login.current_user.is_anonymous)
        self.assertTemplateUsed('index.html')

    def test_register_page(self):
        response = self.client.get(url_for('public.register'))
        self.assert200(response)
        self.assertTrue(flask_login.current_user.is_anonymous)
        self.assertTemplateUsed('register.html')

    def test_login_page(self):
        response = self.client.get(url_for('public.login'))
        self.assert200(response)
        self.assertTrue(flask_login.current_user.is_anonymous)
        self.assertTemplateUsed('login.html')
