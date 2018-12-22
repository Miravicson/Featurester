import unittest
from flask import current_app
from app import create_app, db
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        config = os.getenv('TESTING_CONFIG')
        self.app = create_app(config_class=config)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
