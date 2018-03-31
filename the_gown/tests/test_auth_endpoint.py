# the_gown/tests/test_auth_endpoint.py

import time
import json
import unittest


from the_gown.tests.base import BaseTestCase


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


class TestAuthBlueprint(BaseTestCase):

    def test_registration(self):
        """ Test for user registration """
        with self.client:
            response = register_user(
                self, 'dalin', 'oluoch', 'joe@gmail.com', 'aaaAAA111')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_email_exists(self):
        register_user(self, 'some', 'name', 'another@gmail.com', 'aaaAAA111')
        with self.client:
            response = register_user(
                self, 'dalin', 'oluoch', 'another@gmail.com', 'aaaAAA111')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Email exists, login instead.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)

    def test_invalid_password(self):
        with self.client:
            response = register_user(
                self, 'dalin', 'oluoch', 'invalid@gmail.com', 'password')
            data = json.loads(response.data.decode())
            self.assertTrue(
                data['password'][0] == "value does not match regex '(?=^.{8,}$)((?=.*\\d)|(?=.*\\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$'")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

    def test_show_all_users(self):
        response = self.client.get('/auth/status')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(response.data['email'] == 'another@gmail.com')


if __name__ == '__main__':
    unittest.main()
