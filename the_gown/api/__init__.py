# the_gown/api/__init__.py
"""This is the core module

This module does imports flask framework, initializes it and passes the
initialized flask object to various modules and extensions.
"""

# the os module provides a portable way of using operating system dependent
# functionality
import os

# python microframework
from flask import Flask

# provides bcrypt hashing utilities for our application
from flask_bcrypt import Bcrypt

# making cross-origin AJAX possible
from flask_cors import CORS

# instanciate Flask
app = Flask(__name__)

# initialize the Flask-Cors extension with default arguments in order
# to allow CORS for all domains on all routes
CORS(app)

# os.getenv -> return the value of the environment variable
app_settings = os.getenv(
    'APP_SETTINGS',
    'the_gown.api.config.DevelopmentConfig'
)
# retreiving config stored in separate files (config.py)
app.config.from_object(app_settings)

# pass flask app object to Bcrypt
bcrypt = Bcrypt(app)
