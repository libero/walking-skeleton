import os

import pika


RABBITMQ_URL = os.environ.get('RABBITMQ_URL')

BROKER_PARAMS = pika.connection.URLParameters(RABBITMQ_URL, '')

ARTICLES_QUEUE = os.environ.get('ARTICLES_QUEUE', 'articles')
ARTICLES_EXCHANGE = os.environ.get('ARTICLES_EXCHANGE', 'articles')

DEFAULT_QUEUES = {
    ARTICLES_QUEUE: [
        ARTICLES_EXCHANGE
    ],
}
