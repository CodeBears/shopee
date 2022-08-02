import logging
import requests
from time import sleep


class BeamsApi:
    API_DOMAIN = 'https://www.beams.tw'

    @staticmethod
    def get_response(url, params=None):
        for _ in range(5):
            try:
                response = requests.get(url=url, params=params)
                if response:
                    return response
            except Exception as e:
                logging.exception(e)
                sleep(10)
        return None

    @classmethod
    def get_products(cls, page):
        url = f'{cls.API_DOMAIN}/category/tops'
        params = {
            'p': page
        }
        response = cls.get_response(url=url, params=params)
        return response
