from app import app
from core.product_handler import ProductHandler
from utils.auth_tool import AuthTool
from utils.const import Const
from utils.data_validator import DataValidator, DataSchema
from utils.response_handler import ResponseHandler


@app.route('/member/product/<int:product_id>', methods=['PUT'])
@AuthTool.get_user([Const.Role.MEMBER])
@DataValidator.validate(schema=DataSchema.UPDATE_MY_PRODUCT)
def update_my_product(product_id, user, payload):
    """
    更新商品
    """
    res = ProductHandler.update_my_product(
        user_id=user.id,
        product_id=product_id,
        name=payload['name'],
        describe=payload['describe'],
        product_type_id=payload['product_type_id'],
        images_name=payload['images_name'],
        on_shelf=payload['on_shelf'],
        product_details=payload['product_details']
    )
    return ResponseHandler.to_json(data=res)


@app.route('/member/product', methods=['POST'])
@AuthTool.get_user([Const.Role.MEMBER])
@DataValidator.validate(schema=DataSchema.POST_PRODUCT)
def post_product(user, payload):
    """
    上傳商品
    """
    res = ProductHandler.post_product(
        user_id=user.id,
        name=payload['name'],
        describe=payload['describe'],
        product_type_id=payload['product_type_id'],
        on_shelf=payload['on_shelf'],
        images=payload['images'],
        product_details=payload['product_details'],
    )
    return ResponseHandler.to_json(data=res)


@app.route('/admin/product/<int:product_id>', methods=['PUT'])
@AuthTool.get_user([Const.Role.ADMIN])
@DataValidator.validate(schema=DataSchema.ADMIN_UPDATE_PRODUCT)
def admin_update_product(product_id, user, payload):
    """
    管理員更新商品
    """
    res = ProductHandler.admin_update_product(
        product_id=product_id,
        name=payload['name'],
        describe=payload['describe'],
        product_type_id=payload['product_type_id'],
        on_shelf=payload['on_shelf'],
        product_details=payload['product_details']
    )
    return ResponseHandler.to_json(data=res)


@app.route('/member/product/image/<int:product_id>', methods=['PUT'])
@AuthTool.get_user([Const.Role.MEMBER])
@DataValidator.validate(schema=DataSchema.UPDATE_PRODUCT_IMAGE)
def upload_product_image(user, product_id, payload):
    res = ProductHandler.upload_product_image(
        user_id=user.id,
        product_id=product_id,
        images=payload['images'],
    )
    return ResponseHandler.to_json(data=res)


@app.route('/admin/product', methods=['GET'])
@AuthTool.get_user([Const.Role.ADMIN])
@DataValidator.validate()
def get_all_products(user, payload):
    """
    取得所有商品
    """
    res, pager = ProductHandler.get_all_products(
        page=int(payload.get('page', 1)),
        per_page=int(payload.get('per_page', Const.Page.PER_PAGE)),
        keyword=payload.get('keyword'),
        product_type_id=payload.get('product_type_id'),
    )
    return ResponseHandler.to_json(data=res, pager=pager)


@app.route('/product', methods=['GET'])
@DataValidator.validate()
def get_on_shelf_products(payload):
    """
    取得商品
    """
    res, pager = ProductHandler.get_on_shelf_products(
        page=int(payload.get('page', 1)),
        per_page=int(payload.get('per_page', Const.Page.PER_PAGE)),
        keyword=payload.get('keyword'),
        product_type_id=payload.get('product_type_id'),
    )
    return ResponseHandler.to_json(data=res, pager=pager)


@app.route('/member/product', methods=['GET'])
@AuthTool.get_user([Const.Role.MEMBER])
@DataValidator.validate()
def get_my_products(user, payload):
    """
    取得我的商品
    """
    res, pager = ProductHandler.get_my_products(
        page=int(payload.get('page', 1)),
        per_page=int(payload.get('per_page', Const.Page.PER_PAGE)),
        keyword=payload.get('keyword'),
        user_id=user.id
    )
    return ResponseHandler.to_json(data=res, pager=pager)


@app.route('/product/<int:product_id>', methods=['GET'])
def get_product_detail(product_id):
    """
    取得商品詳細資料
    """
    res = ProductHandler.get_product_detail(
        product_id=product_id
    )
    return ResponseHandler.to_json(data=res)


@app.route('/order', methods=['POST'])
@AuthTool.get_user([Const.Role.MEMBER])
@DataValidator.validate(schema=DataSchema.ORDER)
def buy_product(user, payload):
    """
    買商品
    """
    res = ProductHandler.buy_product(
        user_id=user.id,
        address=payload['address'],
        name=payload['name'],
        phone=payload['phone'],
        delivery=payload['delivery'],
        payment=payload['payment'],
        product_details=payload['product_details'],
    )
    return ResponseHandler.to_json(data=res)


@app.route('/order', methods=['GET'])
@AuthTool.get_user([Const.Role.MEMBER])
@DataValidator.validate()
def get_order(user, payload):
    """
    取得訂單
    """
    res, pager = ProductHandler.get_order(
        user_id=user.id,
        page=int(payload.get('page', 1)),
        per_page=int(payload.get('per_page', Const.Page.PER_PAGE)),
    )
    return ResponseHandler.to_json(data=res, pager=pager)


@app.route('/admin/product-type', methods=['POST'])
@AuthTool.get_user([Const.Role.ADMIN])
@DataValidator.validate(schema=DataSchema.ADD_PRODUCT_TYPE)
def add_product_type(user, payload):
    """
    新增產品種類
    """
    res = ProductHandler.add_product_type(
        name=payload['name'],
    )
    return ResponseHandler.to_json(data=res)
