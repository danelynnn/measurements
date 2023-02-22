from datetime import datetime, timedelta
import jwt
from core import SECRET_KEY


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
    payload = jwt.decode(auth_token, key=SECRET_KEY, algorithms='HS256')
    return payload['sub']
