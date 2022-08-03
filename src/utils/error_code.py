class ErrorCode:
    # system error
    SYSTEM_ERROR = 100
    SIZE_ERROR = 101
    INVALID_TOKEN = 102
    EXPIRED_TOKEN = 103
    HEADER_FORMAT_ERROR = 104
    METHOD_NOT_ALLOWED = 105
    ENDPOINT_NOT_FOUND = 106

    # user error
    DATA_ERROR = 200
    DATA_MISSING = 201
    PERMISSION_DENIED = 203
    INVALID_OPERATION = 204
    SCHEMA_ERROR = 205
    EMAIL_OR_PASSWORD_WRONG = 206
    MEMBER_IS_EXIST = 207
    MEMBER_IS_NOT_EXIST = 208
    PAYLOAD_ERROR = 209
    UPLOAD_IMAGE_ERROR = 210
    PRODUCT_NOT_EXIST = 211
    PRODUCT_TYPE_NOT_EXIST = 212
    PRODUCT_TYPE_IS_EXIST = 213
    UPDATE_PRODUCT_ERROR = 214
    PRODUCT_DETAIL_NOT_EXIST = 215
    OUT_OF_STOCK = 216
    BUY_SELF_PRODUCT = 217

    @staticmethod
    def get_error_key(error_code):
        for key, value in ErrorCode.__dict__.items():
            if key.startswith('_'):
                continue
            if value == error_code:
                return key
        return None

    @staticmethod
    def get_error_msg(error_code):
        for key, value in ErrorCode.__dict__.items():
            if key.startswith('_'):
                continue
            if value == error_code:
                msg = ' '.join(key.split('_')).lower()
                return msg
        return None
