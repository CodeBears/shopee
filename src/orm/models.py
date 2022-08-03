from sqlalchemy import func
from sqlalchemy.dialects.mysql import MEDIUMTEXT

from app import db
from config import Config

BIND_KEY = Config.DB_NAME


class User(db.Model):
    """
    使用者
    """
    __bind_key__ = BIND_KEY
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Integer, nullable=False, comment='1:member 2:admin')
    email = db.Column(db.String(100), unique=True, nullable=False, comment='信箱')
    username = db.Column(db.String(100), unique=True, nullable=False, comment='用戶名')
    is_valid = db.Column(db.Boolean, nullable=False, server_default='0', comment='信箱')
    password = db.Column(db.String(100), nullable=False, comment='密碼')
    update_datetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                                comment='更新時間')
    create_datetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), comment='建立時間')


class Order(db.Model):
    """
    訂單
    """
    __bind_key__ = BIND_KEY
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    address = db.Column(db.String(300), nullable=False, comment='地址')
    name = db.Column(db.String(100), nullable=False, comment='名字')
    phone = db.Column(db.String(100), nullable=False, comment='電話')
    status = db.Column(db.Integer, server_default='1', nullable=False, comment='狀態')
    payment = db.Column(db.Integer, nullable=False, comment='付款方式')
    delivery = db.Column(db.Integer, nullable=False, comment='運送方式')
    update_datetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                                comment='更新時間')
    create_datetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), comment='建立時間')


class OrderDetail(db.Model):
    """
    訂單明細
    """
    __bind_key__ = BIND_KEY
    __tablename__ = 'order_detail'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_detail_id = db.Column(db.Integer, db.ForeignKey('product_detail.id'), nullable=False)
    product_price = db.Column(db.Integer, nullable=False, comment='商品單價')
    product_name = db.Column(db.Integer, nullable=False, comment='商品名稱')
    quantity = db.Column(db.Integer, nullable=False, comment='數量')
    update_datetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                                comment='更新時間')
    create_datetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), comment='建立時間')


class ProductType(db.Model):
    """
    商品種類
    """
    __bind_key__ = BIND_KEY
    __tablename__ = 'product_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment='種類名')
    update_datetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                                comment='更新時間')
    create_datetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), comment='建立時間')


class Product(db.Model):
    """
    商品
    """
    __bind_key__ = BIND_KEY
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False, comment='名字')
    describe = db.Column(db.Text, nullable=False, comment='內文')
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_type.id'), nullable=False)
    images_name = db.Column(MEDIUMTEXT, nullable=True, comment='圖片編號')
    on_shelf = db.Column(db.Boolean, nullable=False, server_default='1', comment='上架')
    update_datetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                                comment='更新時間')
    create_datetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), comment='建立時間')


class ProductDetail(db.Model):
    """
    商品細節
    """
    __bind_key__ = BIND_KEY
    __tablename__ = 'product_detail'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    specifications = db.Column(db.String(100), nullable=False, comment='規格')
    price = db.Column(db.Integer, nullable=False, comment='價錢')
    stock = db.Column(db.Integer, nullable=False, server_default='0', comment='庫存')
    create_datetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), comment='建立時間')
    update_datetime = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                                comment='更新時間')
