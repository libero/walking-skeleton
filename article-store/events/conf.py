import os

import pika


RABBITMQ_URL = os.environ.get('RABBITMQ_URL', '')

BROKER_PARAMS = pika.connection.URLParameters(RABBITMQ_URL)

ARTICLES_DUMMY_QUEUE = os.environ.get('ARTICLES_DUMMY_QUEUE', 'articles-dummy')
ARTICLES_EXCHANGE = os.environ.get('ARTICLES_EXCHANGE', 'articles')


DEFAULT_EXCHANGES = (ARTICLES_EXCHANGE, )
