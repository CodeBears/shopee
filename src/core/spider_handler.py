import json

from bs4 import BeautifulSoup
from tqdm import tqdm

from app import db
from const import ShopeeConst
from core.beams_api import BeamsApi
from orm.models import Product, ProductType, ProductDetail, User
from utils.db_tool import DBTool
from utils.image_tool import ImageHandler


class SpiderHandler:
    @classmethod
    def start_spider(cls):
        products = cls._get_all_products()
        cls._save_to_db(products=products)
        product_ids = cls._save_image(products=products)
        cls._save_image_to_db(product_ids=product_ids)

    @staticmethod
    def _parse_price(price):
        price = price.strip()
        return int(''.join(price[4:].split(',')))

    @staticmethod
    def _parse_img_src(img):
        return 'https:' + img

    @staticmethod
    def _parse_name(name):
        return name.strip()

    @staticmethod
    def _download_image(url, product_id):
        response = BeamsApi.get_response(url=url)
        if not response:
            return None
        ImageHandler.download_image(response=response, product_id=product_id)

    @classmethod
    def _get_products(cls, page):
        response = BeamsApi.get_products(page=page)
        if not response:
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.select('li.beams-list-image-item')
        if not products:
            return None
        res = []
        for product in tqdm(products, desc=f'get products | page: {page}'):
            name = cls._parse_name(product.select_one('div.product-name').getText())
            price = cls._parse_price(product.select_one('div.price').getText())
            img_url = cls._parse_img_src(product.select_one('img').get('src'))
            tmp = {
                'name': name,
                'price': price,
                'img_url': img_url
            }
            product = Product.query.filter(Product.name == name).first()
            if product:
                continue
            res.append(tmp)
        return res

    @classmethod
    def _get_all_products(cls):
        page = 1
        products = cls._get_products(page=page)
        res = []
        while products:
            res.extend(products)
            page = page + 1
            products = cls._get_products(page=page)
        return res

    @staticmethod
    def _save_to_db(products):
        product_type = ProductType.query.filter(ProductType.name == '衣服').first()
        user = User.query.filter(User.username == 'admin001', User.role == ShopeeConst.Role.ADMIN).first()

        for product in tqdm(products, desc='save to db'):
            p = Product(
                user_id=user.id,
                name=product['name'],
                describe=product['name'],
                product_type_id=product_type.id,
            )
            db.session.add(p)
            DBTool.flush()
            default_stock = 1000
            product_detail = ProductDetail(
                product_id=p.id,
                specifications=product['name'],
                price=product['price'],
                stock=default_stock,
            )
            db.session.add(product_detail)
            product['product_id'] = p.id
        DBTool.commit()

    @staticmethod
    def _save_image_to_db(product_ids):
        products = Product.query.filter(Product.id.in_(product_ids)).all()
        for product in tqdm(products, desc=f'save image to db'):
            images_name = [f'{product.id}_1']
            product.images_name = json.dumps(images_name)

    @classmethod
    def _save_image(cls, products):
        product_ids = []
        for product in products:
            cls._download_image(url=product['img_url'], product_id=product['product_id'])
            product_ids.append(product['product_id'])
        return product_ids
