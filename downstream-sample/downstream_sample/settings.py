from contextlib import contextmanager
from functools import wraps
import os
import time
from typing import ContextManager

import pika
import pika.exceptions
from pika.adapters.blocking_connection import BlockingChannel


DELIVERY_MODE_PERSISTENT = 2

BUS_PARAMS = pika.connection.URLParameters(os.environ['RABBITMQ_URL'])

ARTICLE_EXCHANGE_NAME = 'articles'
ARTICLE_EXCHANGE_ROUTING_KEY = 'article.version.*.completed'
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


def wait_exchange(func):
    EXCHANGE_NOT_FOUND = 404

    @wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except pika.exceptions.ChannelClosed as e:
                # pika.exceptions.ChannelClosed: 404, "NOT_FOUND - no exchange 'articles' in vhost '/'"
                if e.args[0] == EXCHANGE_NOT_FOUND:
                    print("Exchange not ready: %s" % e.args[1])
                    time.sleep(1)
                    continue
                else:
                    raise

    return wrapper

@wait_exchange
def ensure_queue(queue_name):
    with get_channel() as channel:
        # create queue, will skip if exists
        channel.queue_declare(queue=queue_name, durable=True)
        # bind queue to exchange, will skip if already bound
        channel.queue_bind(exchange=ARTICLE_EXCHANGE_NAME, queue=queue_name, routing_key=ARTICLE_EXCHANGE_ROUTING_KEY)

def ensure_exchange(exchange_name):
    with get_channel() as channel:
        # create an exchange of type `topic`, will skip if already exists
        channel.exchange_declare(exchange=exchange_name,
                                 exchange_type='topic',
                                 durable=True)
