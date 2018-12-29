import os
import unittest
from datetime import datetime

from dotenv import find_dotenv, load_dotenv
from flask import Flask, url_for
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from app import db, create_app
from app.models import Client, Feature, ProductArea
from tests.base import BasicsTestCase

load_dotenv(find_dotenv())


class FlaskClientTestCase(BasicsTestCase):
    def test_home_page(self):
        """
        Test that the homepage returns a 200 response status code
        :return:
        """
        with self.client:
            response = self.client.get(url_for('main.index'))
            self.assert200(response)
            self.assertTrue('Featurester' in response.get_data(as_text=True))

    def test_page_not_found(self):
        """ Test that a given route does not exists in the application"""

        with self.client:
            response = self.client.get('/home')
            data = response.get_data(as_text=True)
            self.assert404(response)
            self.assertTrue('404' in data)

    def test_method_not_found(self):
        """ Test that a given method is not found"""

        with self.client:
            response = self.client.put(url_for('main.index'))
            data = response.get_data(as_text=True)
            self.assert405(response)
            self.assertTrue('405' in data)

    # def test_factory_function(self):

    #     app = create_app(config_class=os.getenv('APP_SETTINGS'))
    #     assert isinstance(app, Flask)

    def test_delete_feature(self):

        with self.client:
            # create client
            client = self.create_dummy_client()
            # create feature
            feature = self.create_dummy_feature(client)
            response = self.client.post(
                url_for('main.delete_features', client_id=client.id, feature_id=feature.id))
            self.assertEqual(response.status, '302 FOUND')
            self.assertTrue('Redirecting' in response.get_data(as_text=True))

    def test_delete_client(self):
        with self.client:
            # create client
            client = self.create_dummy_client()
            response = self.client.post(
                url_for('main.delete_client', client_id=client.id))
            self.assertEqual(response.status, '302 FOUND')
            self.assertTrue('Redirecting' in response.get_data(as_text=True))

    def test_client_details(self):
        with self.client:
            # create client
            client = self.create_dummy_client()
            response = self.client.get(
                url_for('main.client_details', client_id=client.id))
            self.assert200(response)
            self.assertTrue(
                'Client Details' in response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
