# the_gown/tests/test_config.py
"""This is the test_config module

This module does utilizes unittest and flask testing so as to test our
various app configurations
"""

# testing framework
import unittest

# current app proxy which is bound to the current request’s application
# reference
from flask import current_app

# provide unit testing utilities for Flask
from flask_testing import TestCase

# import out app object
from the_gown.api import app


class TestDevelopmentConfig(TestCase):
    """Test the Development Config Option"""
    @classmethod
    def create_app(self):
        """Create app with Dev config and return it"""
        app.config.from_object('the_gown.api.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        """assert various test cases"""
        self.assertTrue(app.config['SECRET_KEY'] is 'TheSecretKey')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)


class TestTestingConfig(TestCase):
    """Test the Testing Config Option"""

    def create_app(self):
        """Create app with Testing config and return it"""
        app.config.from_object('the_gown.api.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        """assert various test cases"""
        self.assertTrue(app.config['SECRET_KEY'] is 'TheSecretKey')
        self.assertTrue(app.config['DEBUG'])


class TestProductionConfig(TestCase):
    """Test the Production Config Option"""

    def create_app(self):
        """Create app with Production config and return it"""
        app.config.from_object('the_gown.api.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        """assert various test cases"""
        self.assertTrue(app.config['DEBUG'] is False)


# Run script
if __name__ == '__main__':
    unittest.main()
