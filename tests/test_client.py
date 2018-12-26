import unittest
from flask import url_for, Flask
from tests.base import BasicsTestCase
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


class FlaskClientTestCase(BasicsTestCase):
    def test_home_page(self):
        """
        Test that the homepage returns a 200 response status code
        :return:
        """
        with self.client:
            # response = self.client.get('/')
            # # self.assert200(response)
            response = self.client.get(url_for('main.index'))
            self.assert200(response)
            self.assertTrue('' in response.get_data(as_text=True))

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

    def test_create_app(self):
        from app import create_app

        config = os.getenv('APP_SETTINGS')

        app = Flask(__name__)
        app.config.from_object(config)
        self.assertTrue(app == create_app(config_class=config))


if __name__ == "__main__":
    unittest.main()
