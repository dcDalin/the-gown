# the_gown/api/business.py
"""This is the business module

This module does contains the business logic for the auth endpoint
"""
import uuid  # unique random uuid
import datetime  # manipulate date and time
import jwt  # token PyJWT

from the_gown.api import app, bcrypt  # app object and bcrypt
from the_gown.api.models import TheGown  # import the gown class (our database)


class Business(TheGown):
    """The class containing our logic, inherits from TheGown class"""

    def check_email_exists(self, search_email):
        """Search and find if email exists"""
        for find_email in self.users:
            if find_email['email'] == search_email:
                return True
            return False

    def retreive_by_email(self, search_email):
        """Search and retreive all info regarding that email
        as some sort of P.K
        """
        for find_email in self.users:
            if find_email['email'] == search_email:
                return find_email
            return False

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token (encode token)
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() +
                datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def register_user(self, data):
        """Register a new user method
        In addition to user provided data, below are done automatically and
        finally appended to the users list
        """
        data['first_name'] = data['first_name'].title()
        data['last_name'] = data['last_name'].title()
        data['email'] = data['email'].lower()
        data['password'] = bcrypt.generate_password_hash(
            data['password'], app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        data['is_admin'] = False
        data['user_id'] = str(uuid.uuid4())
        data['registered_on'] = datetime.datetime.now()
        self.users.append(data)
        return True

    def show_users(self):
        """Show all users in the users list"""
        return self.users
