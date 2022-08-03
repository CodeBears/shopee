from functools import wraps

from flask import request
from schema import Schema, Regex, And, Optional

from utils.const import Const


class DataValidator:
    @staticmethod
    def validate(schema=None):
        def real_decorator(method, **kwargs):
            @wraps(method)
            def wrapper(*args, **kwargs):
                if request.method in {'GET', 'DELETE'}:
                    payload = request.args
                    payload = dict(payload)
                else:
                    payload = request.get_json(force=True)
                if schema:
                    schema.validate(payload)
                return method(*args, **kwargs, payload=payload)

            return wrapper

        return real_decorator


class DataSchema:
    _EMAIL_PATTERN = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    _USERNAME_PATTERN = r"[A-Za-z\d]{8,20}$"  # 8-20
    _PASSWORD_PATTERN = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,20}$"  # 8-20 英數混合

    SIGN_IN = Schema({
        'email': Regex(_EMAIL_PATTERN),
        'password': str,
    }, ignore_extra_keys=True)

    SIGN_UP = Schema({
        'email': And(str, Regex(_EMAIL_PATTERN)),
        'username': And(str, Regex(_USERNAME_PATTERN)),
        'password': And(str, Regex(_PASSWORD_PATTERN)),
    }, ignore_extra_keys=True)

    ADD_PRODUCT_TYPE = Schema({
        'name': And(str, lambda s: len(s) >= 1),
    }, ignore_extra_keys=True)

    ORDER = Schema({
        'address': And(str, lambda s: len(s) >= 1),
        'name': And(str, lambda s: len(s) >= 1),
        'phone': And(str, lambda s: len(s) >= 1),
        'delivery': And(int, lambda s: s in Const.Delivery.get_elements()),
        'payment': And(int, lambda s: s in Const.Delivery.get_elements()),
        'product_details': [{
            'id': int,
            'quantity': And(int, lambda s: s >= 0)
        }]
    }, ignore_extra_keys=True)
    ADMIN_UPDATE_PRODUCT = Schema({
        'name': And(str, lambda s: len(s) >= 1),
        'describe': And(str, lambda s: len(s) >= 1),
        'product_type_id': int,
        'on_shelf': bool,
        'product_details': [{
            'id': int,
            'price': And(int, lambda s: s >= 0),
            'specifications': And(str, lambda s: len(s) >= 1),
            'stock': And(int, lambda s: s >= 0)
        }]
    }, ignore_extra_keys=True)

    UPDATE_MY_PRODUCT = Schema({
        'name': And(str, lambda s: len(s) >= 1),
        'describe': And(str, lambda s: len(s) >= 1),
        'product_type_id': int,
        'on_shelf': bool,
        'product_details': [{
            'id': int,
            'price': And(int, lambda s: s >= 0),
            'specifications': And(str, lambda s: len(s) >= 1),
            'stock': And(int, lambda s: s >= 0)
        }]
    }, ignore_extra_keys=True)

    UPDATE_PRODUCT_IMAGE = Schema({
        'images': [str],
    }, ignore_extra_keys=True)

    POST_PRODUCT = Schema({
        'name': And(str, lambda s: len(s) >= 1),
        'describe': And(str, lambda s: len(s) >= 1),
        'product_type_id': int,
        'on_shelf': bool,
        'images': [str],
        'product_details': [{
            'price': And(int, lambda s: s >= 0),
            'specifications': And(str, lambda s: len(s) >= 1),
            'stock': And(int, lambda s: s >= 0)
        }]
    }, ignore_extra_keys=True)

    TRANSACTION_REPORT = Schema({
        Optional('start_date'): str,
        Optional('end_date'): str,
        Optional('user_id'): int,
    }, ignore_extra_keys=True)
