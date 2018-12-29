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

    def test_client_model(self):
        c = Client('Client A', 'clienta@company.com')
        db.session.add(c)
        db.session.commit()
        assert c.id > 0
        assert 'Client' in repr(c)

    def test_product_area_model(self):
        p = ProductArea(name='Billings')
        db.session.add(p)
        db.session.commit()
        assert p.id > 0
        assert 'ProductArea' in repr(p)

    def test_save_sort_algo(self):
        client = self.create_dummy_client()

        dummy_form_data = {
            'title': 'Add Navbar',
            'description': 'We need to add a navbar',
            'target_date': datetime.date(datetime.today()),
            'client_priority': 1,
            'client': client,
            'product_areas': []

        }
        

        # create a feature with priority 1
        feature_1 = self.create_dummy_feature(client, priority=1)

        # create another feature with priority 1 using the algorithm

        Feature.save_sort_algo(dummy_form_data, db)

        # retrieve the feature created
        feature_2 = Feature.query.filter_by(title='Add Navbar').first()
        # confirm that the priority of the first feature is different from the the priority of the second feature
        assert (feature_1.client_priority != feature_2.client_priority)
        # confirm that the new feature takes the topmost priority
        assert (feature_2.client_priority == 1)
        # confirm that the old feature has it's priority increased by one
        assert (feature_1.client_priority == 2)


if __name__ == "__main__":
    unittest.main()
