import jwt
from datetime import datetime, timedelta

SECRET_KEY = b'7[\x7f\rl\xe7\xa4\xfbc\xe2\xc1MxKg\x08\xf9w/P\x17X\xf6L'


def encode_auth_token(user):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=0, seconds=2400),
        'iat': datetime.utcnow(),
        'sub': str(user['_id'])
    }
    return jwt.encode(
        payload,
        key=SECRET_KEY,
        algorithm='HS256'
    )


def decode_auth_token(auth_token):
    # except jwt.ExpiredSignatureError:
    #     return 'Signature expired. Please log in again.'
    # except jwt.InvalidTokenError:
    #     return 'Invalid token. Please log in again.'
    payload = jwt.decode(auth_token, key=SECRET_KEY)
    return payload['sub']


auth_token = encode_auth_token({'_id': '21232134'})
print(decode_auth_token(auth_token))
