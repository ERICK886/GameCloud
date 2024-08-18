import datetime

import jwt
from django.conf import settings

from backend.models import User


def check_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload, True
    except jwt.ExpiredSignatureError:
        return 'token已过期', False
    except jwt.DecodeError:
        return 'token认证失败', False
    except jwt.InvalidTokenError:
        return '非法的token', False


def create_token(user):
    payload = {
        'id': user.id,
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
    }
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm='HS256'
    )
    return token


def check_admin(token):
    payload, flag = check_token(token)
    if User.objects.get(id=payload['id']).is_admin:
        return True
    else:
        return False
