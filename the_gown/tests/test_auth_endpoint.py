# the_gown/tests/test_auth_endpoint.py

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


def login_user(self, email, password):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
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
        """Test wrong password formart"""
        with self.client:
            response = register_user(
                self, 'dalin', 'oluoch', 'inalid@gmail.com', 'password')
            data = json.loads(response.data.decode())
            self.assertTrue(
                data['password'][0] ==
                "value does not match regex '(?=^.{8,}$)((?=.*\\d)|(?=.*\\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$'")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

    # Login Tests

    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        register_user(self, 'some', 'name', 'another@gmail.com', 'aaaAAA111')
        with self.client:
            response = login_user(self, 'another@gmail.com', 'aaaAAA111')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_wrong_pass_login(self):
        """Test registered user logs in with correct email but incorrect
        password
        """
        register_user(self, 'some', 'name', 'another@gmail.com', 'aaaAAA111')
        with self.client:
            response = login_user(
                self, 'another@gmail.com', 'aaaAA3A111')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Wrong password.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_email_not_exists_login(self):
        """Test for non existent email during login, a user who's not
        registered
        """
        with self.client:
            response = login_user(
                self, 'themail@themail.com', 'aaaAAA111')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] ==
                            'Email does not exist, register instead.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_invalid_email_login(self):
        """Test for invalid email formart durring login"""
        with self.client:
            response = login_user(
                self, 'invaligmail.com', 'password')
            data = json.loads(response.data.decode())
            self.assertTrue(
                data['email'][0] ==
                "value does not match regex '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$'")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

    def test_empty_email_login(self):
        """Test for email being empty durring login"""
        with self.client:
            response = login_user(
                self, '', 'password')
            data = json.loads(response.data.decode())
            self.assertTrue(
                data['email'][0] ==
                "empty values not allowed")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

    def test_empty_password_login(self):
        """Test for password being empty durring login"""
        with self.client:
            response = login_user(
                self, 'joe@gmail.com', '')
            data = json.loads(response.data.decode())
            self.assertTrue(
                data['password'][0] ==
                "empty values not allowed")
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)

    def test_email_doesnot_exist(self):
        """Test unregistered user trying to login"""
        with self.client:
            response = login_user(
                self, 'doesnotexisttrying@log.com', 'aaaAAA111')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] ==
                            'Email does not exist, register instead.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_show_all_users(self):
        response = self.client.get('/auth/status')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(response.data['email'] == 'another@gmail.com')


if __name__ == '__main__':
    unittest.main()
