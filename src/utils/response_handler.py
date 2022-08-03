from flask import jsonify, make_response

from utils.error_code import ErrorCode
from utils.errors import ValidationError


class ResponseHandler:
    @staticmethod
    def _validate_results(res):
        if res is False:
            raise ValidationError(error_code=ErrorCode.INVALID_OPERATION)
        if res is None:
            raise ValidationError(error_code=ErrorCode.DATA_MISSING)
        if not (isinstance(res, dict) or isinstance(res, list)):
            raise ValidationError(error_code=ErrorCode.DATA_ERROR)

    @staticmethod
    def _validate_pager(pager):
        if pager is None:
            return

        if not isinstance(pager, dict):
            raise ValidationError(error_code=ErrorCode.DATA_ERROR)

    @classmethod
    def to_json(cls, data, pager=None, code=200):
        if data is True:
            return jsonify({'success': True}), code
        cls._validate_results(res=data)
        cls._validate_pager(pager=pager)
        res = {
            'success': True,
            'response': {
                'data': data,
                'pager': pager,
            }
        }
        return jsonify(res), code

    @staticmethod
    def make_pager(page, per_page, obj):
        pager = {
            'page': page,
            'per_page': per_page,
            'total': obj.total,
            'pages': obj.pages,
        }
        return pager

    @staticmethod
    def make_csv_response(csv, filename):
        response = make_response(csv)
        response.minetype = 'text/csv'
        response.headers['Content-disposition'] = f'attachment; filename={filename}.csv'
        return response
