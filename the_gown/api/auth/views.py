# the_gown/api/auth/views.py


from flask import Blueprint, request, make_response, jsonify

# allows execution of a different function for each HTTP method
from flask.views import MethodView

from cerberus import Validator  # JSON validation

from the_gown.api import bcrypt  # bcrypt

# import the main logic class
from the_gown.api.auth.business import Business

# import our custom schema validation
from the_gown.api.auth.schema import register_user_schema, login_user_schema

# create a blueprint for /auth route
auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

# initialize the business class
init_business = Business()

v = Validator()


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """
    @classmethod
    def post(self):
        # get our custom schema
        schema = register_user_schema()
        # get the post data
        post_data = request.get_json(force=True)
        data = {
            'first_name': post_data['first_name'],
            'last_name': post_data['last_name'],
            'email': post_data['email'],
            'password': post_data['password']
        }
        # check validation against our schema
        if not v.validate(data, schema):
            return jsonify(v.errors), 400
        # check if email exists
        if init_business.check_email_exists(data['email']):
            responseObject = {
                'status': 'fail',
                'message': 'Email exists, login instead.'
            }
            return make_response(jsonify(responseObject)), 202

        if init_business.register_user(data):
            responseObject = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return make_response(jsonify(responseObject)), 201


class LoginAPI(MethodView):
    """
    User Login Resource
    """
    @classmethod
    def post(self):
        # get our custom schema
        login_schema = login_user_schema()
        # get the post data
        post_data = request.get_json()
        data = {
            'email': post_data['email'],
            'password': post_data['password']
        }
        # check validation against our schema
        if not v.validate(data, login_schema):
            return jsonify(v.errors), 400

        if init_business.check_email_exists(data['email']):
            """If email exists"""

            # get all records relating to the passed email
            user_info = init_business.retreive_by_email(data['email'])

            # decrypt password
            if bcrypt.check_password_hash(user_info['password'],
                                          data['password']):
                auth_token = init_business.encode_auth_token(
                    user_info['user_id'])
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 200
            else:
                # Wrong password
                responseObject = {
                    'status': 'fail',
                    'message': 'Wrong password.'
                }
                return make_response(jsonify(responseObject)), 404
        # if user email doesn't exist
        responseObject = {
            'status': 'fail',
            'message': 'Email does not exist, register instead.'
        }
        return make_response(jsonify(responseObject)), 404


class UserAPI(MethodView):
    """
    User Resource
    """
    @classmethod
    def get(self):
        return make_response(jsonify({
            'data': init_business.show_users()
        })), 200


class LogoutAPI(MethodView):
    """
    Logout Resource
    """
    pass


# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
user_view = UserAPI.as_view('user_api')
logout_view = LogoutAPI.as_view('logout_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/register',
    view_func=registration_view,
    methods=['POST']


)
auth_blueprint.add_url_rule(
    '/login',
    view_func=login_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/status',
    view_func=user_view,
    methods=['GET']
)
auth_blueprint.add_url_rule(
    '/logout',
    view_func=logout_view,
    methods=['POST']
)
