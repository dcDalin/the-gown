import json
import unittest

from the_gown.tests.base import BaseTestCase

from the_gown.api.auth.business import Business


def register_user(self, first_name, last_name, email, password):
    return self.client.post(
        '/auth/register',
        data=json.dumps(dict(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )),
        content_type='application/json',
    )


class TestAuthBusiness(unittest.TestCase):

    def setUp(self):
        '''initialization'''
        self.initAuth = Business()

    def test_check_email_exists(self):
        '''Test email exists'''
        response = self.initAuth.check_email_exists('random@mail.com')
        self.assertFalse(response)

    def test_check_email_exists_true(self):
        data = {
            'first_name': 'test',
            'last_name': 'last',
            'email': 'the@email.co',
            'password': 'aaaAAA111'
        }
        reg = self.initAuth.register_user(data)
        self.assertTrue(reg)
        response = self.initAuth.check_email_exists('the@email.co')
        self.assertTrue(response)

    def test_retreive_by_email(self):
        '''Test email retreival failed'''
        response = self.initAuth.retreive_by_email('random@rand.com')
        self.assertFalse(response)


if __name__ == '__main__':
    unittest.main()
