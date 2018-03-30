# the_gown/api/auth/views.py

import json

from flask import Blueprint, request, make_response, jsonify

# allows execution of a different function for each HTTP method
from flask.views import MethodView

# import the main logic class
from the_gown.api.auth.business import Business

# create a blueprint for /auth route
auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

# initialize the business class
init_business = Business()


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json(force=True)
        data = {
            'first_name': post_data['first_name'],
            'last_name': post_data['last_name'],
            'email': post_data['email'],
            'password': post_data['password']
        }
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

    def post(self):
        pass


class UserAPI(MethodView):
    """
    User Resource
    """

    def get(self):
        return make_response(jsonify({
            'data': init_business.show_users()
        })), 200


class LogoutAPI(MethodView):
    """
    Logout Resource
    """

    def post(self):
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
