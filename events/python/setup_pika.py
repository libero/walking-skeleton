from contextlib import contextmanager
from typing import ContextManager

import pika
from pika.adapters.blocking_connection import BlockingChannel


ARTICLE_EXCHANGE_NAME = 'articles'
DASHBOARD_QUEUE_NAME = 'dashboard'
DELIVERY_MODE_PERSISTENT = 2

HOST = 'localhost'
PORT = 5672

CREDENTIALS = pika.PlainCredentials('guest', 'guest')
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
