class ConstTemplate:
    _INVALID_TYPE = {classmethod, staticmethod}

    @classmethod
    def get_elements(cls):
        elements = set()
        for k, v in cls.__dict__.items():
            if k.startswith('_') or type(v) in cls._INVALID_TYPE:
                continue
            elements.add(v)
        return elements


class Const:
    class Page:
        PER_PAGE = 20
        MAX_PAGE = 20

    class Role:
        ADMIN = 1  # 管理員
        MEMBER = 2  # 會員

    class OrderStatus:
        PENDING = 1  # 訂單成立
        DELIVERY = 2  # 貨物運送
        ARRIVE = 3  # 到貨
        DONE = 4  # 已取貨
        RETURN = 5  # 退貨

    class Payment:
        COD = 1  # 貨到付款
        CREDIT_CARD = 2  # 信用卡

    class Delivery(ConstTemplate):
        SEVEN_ELEVEN = 1  # 7-11
        FAMILY_MART = 2  # 全家
        OK_MART = 3
        SHOPEE = 4  # 蝦皮店到店
        HOME_DELIVERY = 5  # 宅配
