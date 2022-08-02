from app import create_app, config
from core.spider_handler import SpiderHandler

app = create_app()

env = config['ENVIRONMENT']

if __name__ == '__main__':
    SpiderHandler.start_spider()
