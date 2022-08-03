from app import create_app, config, db
from utils.auth_tool import AuthTool
from utils.db_tool import DBTool

app = create_app()

env = config['ENVIRONMENT']
from orm.models import ProductType, User
from utils.const import Const

if __name__ == '__main__':
    db.create_all()
    product_type = ProductType(name='衣服')
    db.session.add(product_type)
    password = AuthTool.hash_password(password='a11111111'),
    user = User(
        username='member001',
        email='member001@gmail.com',
        password=password,
        role=Const.Role.MEMBER,
    )
    db.session.add(user)
    user = User(
        username='admin001',
        email='admin001@gmail.com',
        password=password,
        role=Const.Role.ADMIN,
    )
    db.session.add(user)
    DBTool.commit()
