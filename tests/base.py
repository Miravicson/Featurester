import os
import unittest
from datetime import datetime

from dotenv import find_dotenv, load_dotenv
from flask import current_app
from flask_testing import TestCase

from app import create_app, db
from app.models import Client, Feature

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

    def create_dummy_client(self):
        ''' Test that a given feature is created '''
        client = Client('Client A', 'clienta@company.com')
        assert isinstance(client, Client)
        db.session.add(client)
        db.session.commit()
        return Client.query.filter_by(name='Client A').first()

    def create_dummy_feature(self, client, priority=1):

        date = datetime.date(datetime.today())
        feature = Feature(
            'Add footer', 'We need nice footer', priority, date, client)
        assert isinstance(feature, Feature)
        db.session.add(feature)
        db.session.commit()
        return Feature.query.filter_by(title='Add footer').first()
