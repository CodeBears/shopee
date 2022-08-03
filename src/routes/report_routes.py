from app import app
from core.report_handler import ReportHandler
from utils.auth_tool import AuthTool
from utils.const import Const
from utils.data_validator import DataValidator, DataSchema
from utils.response_handler import ResponseHandler


@app.route('/admin/report/transaction', methods=['GET'])
@AuthTool.get_user([Const.Role.ADMIN])
@DataValidator.validate(DataSchema.TRANSACTION_REPORT)
def transaction_report(user, payload):
    res = ReportHandler.get_transaction_report(
        start_date=payload.get('start_date'),
        end_date=payload.get('end_date'),
    )
    return ResponseHandler.make_csv_response(csv=res, filename='transaction_report')
