import os
import unittest
from datetime import datetime

from dotenv import find_dotenv, load_dotenv
from flask import Flask, url_for
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from app import db
from app.models import Client, Feature, ProductArea
from tests.base import BasicsTestCase


class ModelTestCase(BasicsTestCase):
    def test_feature_creation(self):
        ''' Test that a given feature is created '''
        client = Client('Client A', 'clienta@company.com')
        assert isinstance(client, Client)
        date = datetime.date(datetime.today())
        db.session.add(client)
        db.session.commit()
        client = Client.query.filter_by(name='Client A').first()
        feature = Feature(
            'Add footer', 'We neeed nice footer', 1, date, client)
        assert isinstance(feature, Feature)
        db.session.add(feature)
        db.session.commit()


if __name__ == "__main__":
    unittest.main()
