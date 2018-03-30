# the_gown/api/auth/views.py


from flask import Blueprint, jsonify

# allows execution of a different function for each HTTP method
from flask.views import MethodView

# create a blueprint for /auth route
auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def post(self):
        pass


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
        pass


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
