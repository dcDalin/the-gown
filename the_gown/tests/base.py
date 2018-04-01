# the_gown/tests/base.py


from flask_testing import TestCase

from the_gown.api import app


class BaseTestCase(TestCase):
    """ Base Tests """

    @classmethod
    def create_app(self):
        app.config.from_object('the_gown.api.config.TestingConfig')
        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass
