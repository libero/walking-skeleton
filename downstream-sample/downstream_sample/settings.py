from contextlib import contextmanager
from typing import ContextManager

import pika
from pika.adapters.blocking_connection import BlockingChannel


DELIVERY_MODE_PERSISTENT = 2

# TODO: extract as environment variables
HOST = 'event-bus'
PORT = 5672
PASSWORD = 'guest'
USER = 'guest'
ARTICLE_EXCHANGE_NAME = 'articles'
DOWNSTREAM_EXCHANGE_NAME = 'downstream-sample'
DOWNSTREAM_QUEUE_NAME = 'downstream-sample'

CREDENTIALS = pika.PlainCredentials(USER, PASSWORD)
PARAMS = pika.ConnectionParameters(host=HOST, credentials=CREDENTIALS)


@contextmanager
def get_channel() -> ContextManager[BlockingChannel]:
    """Handles the creation and clean up of a connection,
    giving the caller a connection channel to use.
    :return: class: `BlockingChannel`
    """
    connection = pika.BlockingConnection(parameters=PARAMS)
    yield connection.channel()
    connection.close()

# TODO: rename to ensure_queue()
# TODO: pass queue name as argument?
def get_queue():
    with get_channel() as channel:
        # create queue, will skip if exists
        channel.queue_declare(queue=DOWNSTREAM_QUEUE_NAME, durable=True)
        # bind queue to exchange, will skip if already bound
        channel.queue_bind(exchange=ARTICLE_EXCHANGE_NAME, queue=DOWNSTREAM_QUEUE_NAME)

def ensure_exchange(exchange_name):
    with get_channel() as channel:
        # create an exchange of type `fanout`, will skip if already exists
        channel.exchange_declare(exchange=exchange_name,
                                 exchange_type='fanout',
                                 durable=True)
