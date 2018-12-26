import unittest
from flask_testing import TestCase
from flask import current_app
from app import create_app, db
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


class BasicsTestCase(TestCase):
    def create_app(self):
        config = os.getenv('TESTING_CONFIG')
        app = create_app(config_class=config)
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
