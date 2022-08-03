from datetime import datetime, timedelta

import pandas as pd

from app import db, app
from config import Config
from orm.models import OrderDetail


class ReportHandler:
    @classmethod
    def get_transaction_report(cls, start_date, end_date):
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m')
        else:
            start_date = datetime.now() - timedelta(days=180)

        if end_date:
            end_date = datetime.strptime(start_date, '%Y-%m')
        else:
            end_date = datetime.now()
        conditions = [
            OrderDetail.create_datetime >= start_date,
            OrderDetail.create_datetime <= end_date
        ]
        query = OrderDetail.query.filter(*conditions)
        df = pd.read_sql(query.statement, db.get_engine(app, Config.DB_NAME))

        df['total'] = df['product_price'] * df['quantity']
        drop_column = [
            'id',
            'order_id',
            'product_detail_id',
            'product_price',
            'product_name',
            'product_name',
            'quantity',
            'update_datetime'
        ]
        df.drop(drop_column, axis=1, inplace=True)
        if df.empty:
            return df.to_csv()
        per = df.create_datetime.dt.to_period("M")
        df = df.groupby(per).sum()
        return df.to_csv()
