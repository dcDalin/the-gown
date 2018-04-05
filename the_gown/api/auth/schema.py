# pasword regex
# https://gist.github.com/ravibharathii/3975295
"""Contains methods that handle input validation schema for the auth endpoint"""


def register_user_schema():
    '''Input validation schema for new user registration'''
    return {
        'first_name': {
            'empty': False,
            'minlength': 3,
            'maxlength': 10,
            'type': 'string',
            'regex': "^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$"
        },
        'last_name': {
            'empty': False,
            'minlength': 3,
            'maxlength': 10,
            'type': 'string',
            'regex': "^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$"
        },
        'email': {
            'empty': False,
            'type': 'string',
            'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        },
        'password': {
            'empty': False,
            'maxlength': 30,
            'type': 'string',
            'regex':
            '(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$'
        }
    }


def login_user_schema():
    '''Input validation schema for user login'''
    return {
        'email': {
            'empty': False,
            'type': 'string',
            'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        },
        'password': {
            'empty': False,
            'minlength': 8,
            'maxlength': 30,
            'type': 'string'
        }
    }
