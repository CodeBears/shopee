from functools import wraps

import bcrypt
from flask import request

from config import Config
from orm.models import User
from utils.error_code import ErrorCode
from utils.errors import ValidationError
from utils.jwt_tool import JWTTool


class AuthTool:
    @staticmethod
    def _unicode_to_bytes(unicode_string):
        return bytes(unicode_string, 'utf-8')

    @staticmethod
    def _get_token_content():
        prefix = 'Bearer'
        header = request.headers.get('Authorization')
        bearer, _, token = header.partition(' ')
        if bearer != prefix:
            raise ValidationError(error_code=ErrorCode.HEADER_FORMAT_ERROR)
        return JWTTool.decode_jwt(Config.JWT_SECRET_KEY, token=token)

    @classmethod
    def hash_password(cls, password):
        password = cls._unicode_to_bytes(password)
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password, salt).decode('utf-8')

    @classmethod
    def check_password(cls, password, hashed):
        password = cls._unicode_to_bytes(password)
        hashed = cls._unicode_to_bytes(hashed)
        return bcrypt.checkpw(password, hashed)

    @classmethod
    def get_access_token(cls, **kwargs):
        res = JWTTool.encode_jwt(
            secret_key=Config.JWT_SECRET_KEY,
            exp=Config.ACCESS_TOKEN_EXPIRE_TIME,
            **kwargs
        )
        return res

    @classmethod
    def get_user(cls, roles):
        def real_decorator(method, **kwargs):
            @wraps(method)
            def wrapper(*args, **kwargs):
                token_content = cls._get_token_content()
                email = token_content.get('email')
                if not email:
                    raise ValidationError(error_code=ErrorCode.INVALID_TOKEN)
                user = User.query.filter_by(email=email).first()
                if not user:
                    raise ValidationError(error_code=ErrorCode.MEMBER_IS_NOT_EXIST)
                if roles:
                    if user.role not in roles:
                        raise ValidationError(error_code=ErrorCode.PERMISSION_DENIED)
                return method(*args, **kwargs, user=user)

            return wrapper

        return real_decorator
