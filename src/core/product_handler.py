import json

from app import db
from orm.models import Product, ProductDetail, ProductType, Order, OrderDetail
from utils.const import Const
from utils.db_tool import DBTool
from utils.error_code import ErrorCode
from utils.errors import ValidationError
from utils.image_tool import ImageHandler
from utils.response_handler import ResponseHandler


class ProductHandler:
    @classmethod
    def post_product(cls, user_id, name, describe, product_type_id, on_shelf, images, product_details):
        if not images:
            raise ValidationError(error_code=ErrorCode.PAYLOAD_ERROR)
        product = Product(
            user_id=user_id,
            name=name,
            describe=describe,
            product_type_id=product_type_id,
            on_shelf=on_shelf,
        )

        db.session.add(product)
        db.session.flush()
        for product_detail in product_details:
            detail = ProductDetail(
                product_id=product.id,
                specifications=product_detail['specifications'],
                price=product_detail['price'],
                stock=product_detail['stock'],
            )
            db.session.add(detail)
        images_name = ImageHandler.upload_product_images(product_id=product.id, images=images)
        product.images_name = json.dumps(images_name)
        DBTool.commit()
        res = {
            'id': product.id,
            'user_id': user_id,
            'name': name,
            'describe': describe,
            'product_type_id': product_type_id,
            'on_shelf': on_shelf,
        }
        return res

    @staticmethod
    def _get_product_detail_map(detail_ids):
        details = ProductDetail.query.filter(
            ProductDetail.id.in_(detail_ids),
        ).all()
        res = {
            detail.id: detail for detail in details
        }
        return res

    @classmethod
    def _update_product_image(cls, product_images_name, images_name):
        for name in images_name:
            if name not in product_images_name:
                raise ValidationError(ErrorCode.UPDATE_PRODUCT_ERROR)
        return json.dumps(list(set(images_name)))

    @classmethod
    def _update_product(cls, product, name, describe, product_type_id, on_shelf, product_details, images_name=None):
        product.name = name
        product.describe = describe
        product.on_shelf = on_shelf
        product.product_type_id = product_type_id
        detail_ids = [product_detail['id'] for product_detail in product_details]
        detail_map = cls._get_product_detail_map(detail_ids=detail_ids)
        if images_name:
            product.images_name = cls._update_product_image(
                product_images_name=product.images_name,
                images_name=images_name
            )

        for product_detail in product_details:
            if product_detail['id'] not in detail_map:
                raise ValidationError(error_code=ErrorCode.PAYLOAD_ERROR)
            detail = detail_map[product_detail['id']]
            if product.id != detail.product_id:
                raise ValidationError(error_code=ErrorCode.PAYLOAD_ERROR)
            detail.price = product_detail['price']
            detail.specifications = product_detail['specifications']
            detail.stock = product_detail['stock']
        ProductDetail.query.filter(
            ProductDetail.product_id == product.id,
            ProductDetail.id.not_in(detail_ids)
        ).delete()
        DBTool.commit()

    @classmethod
    def update_my_product(
            cls, user_id, product_id, name, images_name, describe, product_type_id, on_shelf, product_details):
        product = Product.query.filter(
            Product.id == product_id,
            Product.user_id == user_id
        ).first()
        if not product:
            raise ValidationError(error_code=ErrorCode.PRODUCT_NOT_EXIST)
        cls._update_product(
            product=product,
            name=name,
            describe=describe,
            images_name=images_name,
            product_type_id=product_type_id,
            on_shelf=on_shelf,
            product_details=product_details
        )
        return True

    @classmethod
    def admin_update_product(cls, product_id, name, describe, product_type_id, on_shelf, product_details):
        if not product_details:
            raise
        product = Product.query.filter(
            Product.id == product_id,
        ).first()
        if not product:
            raise ValidationError(error_code=ErrorCode.PRODUCT_NOT_EXIST)
        cls._update_product(
            product=product,
            name=name,
            describe=describe,
            product_type_id=product_type_id,
            on_shelf=on_shelf,
            product_details=product_details
        )
        return True

    @classmethod
    def upload_product_image(cls, user_id, product_id, images):
        product = Product.query.filter(
            Product.id == product_id,
            Product.user_id == user_id
        ).first()
        if not product:
            raise ValidationError(error_code=ErrorCode.PRODUCT_NOT_EXIST)
        images_name = ImageHandler.upload_product_images(product_id=product_id, images=images)
        if product.images_name is None:
            product.images_name = json.dumps(images_name)
        else:
            images_name.extend(json.loads(product.images_name))
            product.images_name = json.dumps(images_name)
        DBTool.commit()
        return True

    @staticmethod
    def _get_products(page, per_page, conditions):
        products = Product.query.filter(
            *conditions
        ).paginate(
            page=page,
            per_page=per_page,
            max_per_page=Const.Page.MAX_PAGE,
        )
        res = []
        for product in products.items:
            detail = ProductDetail.query.filter_by(product_id=product.id).first()
            data = {
                'id': product.id,
                'name': product.name,
                'price': detail.price,
                'describe': product.describe,
                'product_type': product.product_type_id,
                'images_name': json.loads(product.images_name),
                'on_shelf': product.on_shelf
            }
            res.append(data)
        pager = ResponseHandler.make_pager(page=page, per_page=per_page, obj=products)
        return res, pager

    @classmethod
    def get_all_products(cls, page, per_page, keyword, product_type_id):
        conditions = []
        if product_type_id:
            conditions.append(Product.product_type_id == product_type_id)
        if keyword:
            conditions.append(Product.name.like(f'%{keyword}%'))
        res, pager = cls._get_products(page=page, per_page=per_page, conditions=conditions)
        return res, pager

    @classmethod
    def get_on_shelf_products(cls, page, per_page, keyword, product_type_id):
        conditions = [
            Product.on_shelf
        ]
        if product_type_id:
            conditions.append(Product.product_type_id == product_type_id)
        if keyword:
            conditions.append(Product.name.like(f'%{keyword}%'))
        res, pager = cls._get_products(page=page, per_page=per_page, conditions=conditions)
        return res, pager

    @classmethod
    def get_my_products(cls, page, per_page, keyword, user_id):
        conditions = [
            Product.user_id == user_id
        ]
        if keyword:
            conditions.append(Product.name.like(f'%{keyword}%'))
        res, pager = cls._get_products(page=page, per_page=per_page, conditions=conditions)
        return res, pager

    @classmethod
    def get_product_detail(cls, product_id):
        products = db.session.query(
            ProductDetail.id,
            ProductDetail.product_id,
            ProductDetail.specifications,
            ProductDetail.price,
            ProductDetail.stock,
            Product.describe,
            Product.name,
            Product.images_name,
            ProductType.name.label('product_type'),
        ).filter(
            Product.id == product_id,
            Product.on_shelf
        ).join(
            Product, ProductDetail.product_id == Product.id
        ).join(
            ProductType, Product.product_type_id == ProductType.id
        ).all()
        if not products:
            raise ValidationError(error_code=ErrorCode.PRODUCT_NOT_EXIST)
        res = {
            'id': products[0].id,
            'name': products[0].name,
            'describe': products[0].describe,
            'product_type': products[0].product_type,
            'price': products[0].price,
            'images_name': json.loads(products[0].images_name),
        }
        details = []
        for product in products:
            data = {
                'id': product.id,
                'product_id': product.product_id,
                'specifications': product.specifications,
                'stock': product.stock,
                'price': product.price,
            }
            details.append(data)
        res['details'] = details
        return res

    @classmethod
    def buy_product(cls, user_id, address, name, phone, delivery, payment, product_details):
        order = Order(
            user_id=user_id,
            address=address,
            name=name,
            phone=phone,
            delivery=delivery,
            payment=payment
        )
        db.session.add(order)
        db.session.flush()
        detail_ids = [product_detail['id'] for product_detail in product_details]
        product_detail_map = cls._get_product_detail_map(detail_ids=detail_ids)
        product_ids = set()
        for detail in product_details:
            if detail['id'] not in product_detail_map:
                raise ValidationError(error_code=ErrorCode.PRODUCT_DETAIL_NOT_EXIST)
            detail_obj = product_detail_map[detail['id']]
            detail_obj.stock = detail_obj.stock - detail['quantity']
            if detail_obj.stock < 0:
                raise ValidationError(error_code=ErrorCode.OUT_OF_STOCK)
            product_ids.add(detail_obj.product_id)
            order_detail = OrderDetail(
                order_id=order.id,
                product_detail_id=detail_obj.id,
                product_price=detail_obj.price,
                product_name=detail_obj.specifications,
                quantity=detail['quantity'],
            )
            db.session.add(order_detail)
        product = Product.query.filter(Product.user_id == user_id, Product.id.in_(product_ids)).first()
        if product:
            raise ValidationError(error_code=ErrorCode.BUY_SELF_PRODUCT)
        DBTool.commit()
        res = {
            'id': order.id,
            'user_id': user_id,
            'address': address,
            'name': name,
            'phone': phone,
            'delivery': delivery,
            'payment': payment
        }
        return res

    @classmethod
    def add_product_type(cls, name):
        product_type = ProductType.query.filter(ProductType.name == name).first()
        if product_type:
            raise ValidationError(error_code=ErrorCode.PRODUCT_TYPE_IS_EXIST)
        product_type = ProductType(
            name=name,
        )
        db.session.add(product_type)
        DBTool.commit()
        res = {
            'id': product_type.id,
            'name': name,
        }
        return res
