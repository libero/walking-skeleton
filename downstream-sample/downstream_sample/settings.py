from contextlib import contextmanager
from typing import ContextManager
import os

import pika
from pika.adapters.blocking_connection import BlockingChannel


DELIVERY_MODE_PERSISTENT = 2

BUS_PARAMS = pika.connection.URLParameters(os.environ['RABBITMQ_URL'])

ARTICLE_EXCHANGE_NAME = 'articles'
DOWNSTREAM_EXCHANGE_NAME = 'downstream-sample'
DOWNSTREAM_QUEUE_NAME = 'downstream-sample'



@contextmanager
def get_channel() -> ContextManager[BlockingChannel]:
    """Handles the creation and clean up of a connection,
    giving the caller a connection channel to use.
    :return: class: `BlockingChannel`
    """
    connection = pika.BlockingConnection(parameters=BUS_PARAMS)
    yield connection.channel()
    connection.close()

def ensure_queue(queue_name):
    with get_channel() as channel:
        # create queue, will skip if exists
        channel.queue_declare(queue=queue_name, durable=True)
        # bind queue to exchange, will skip if already bound
        channel.queue_bind(exchange=ARTICLE_EXCHANGE_NAME, queue=queue_name)

# TODO: wait for exchange to be present
def ensure_exchange(exchange_name):
    with get_channel() as channel:
        # create an exchange of type `fanout`, will skip if already exists
        channel.exchange_declare(exchange=exchange_name,
                                 exchange_type='fanout',
                                 durable=True)
