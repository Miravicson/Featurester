import unittest
import os
from flask import url_for
from app import create_app, db
from app.models import Feature, Client, ProductArea
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        config = os.getenv('TESTING_CONFIG')
        self.app = create_app(config_class=config)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue('' in response.get_data(as_text=True))
