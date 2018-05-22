import os

import pika


RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')  # event-bus
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT', 5672)
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD')
RABBITMQ_USER = os.environ.get('RABBITMQ_USER')

BROKER_CREDENTIALS = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
BROKER_PARAMS = pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=BROKER_CREDENTIALS)

ARTICLES_QUEUE = os.environ.get('ARTICLES_QUEUE', 'articles')
ARTICLES_EXCHANGE = os.environ.get('ARTICLES_EXCHANGE', 'articles')

DEFAULT_QUEUES = {
    ARTICLES_QUEUE: [
        ARTICLES_EXCHANGE
    ],
}
