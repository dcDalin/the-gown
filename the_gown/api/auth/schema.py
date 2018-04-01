# pasword regex
# https://gist.github.com/ravibharathii/3975295


def register_user_schema():
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
