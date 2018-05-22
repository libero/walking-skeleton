from contextlib import contextmanager
from functools import partial, wraps
import json
from time import gmtime, strftime
from typing import (
    Any,
    Callable,
    ContextManager,
    Dict
)
import uuid

import pika
from pika.exceptions import ConnectionClosed
from pika.adapters.blocking_connection import BlockingChannel

from .conf import (
    ARTICLES_EXCHANGE,
    BROKER_PARAMS,
    DEFAULT_QUEUES
)


DELIVERY_MODE_PERSISTENT = 2


def create_message(msg_type: str, identifier: str, data: Dict) -> Dict:
    """Create a message `dict` based on a standard schema.

    :return: Dict
    """
    return {
        "eventId": str(uuid.uuid1()),
        "happenedAt": strftime("%Y-%m-%dT%H:%M:%S+00:00", gmtime()),
        "aggregate": {
            "service": "article-store",
            "name": "article-version",
            "identifier": identifier,
        },
        "type": msg_type,
        "data": data or {}
    }


@contextmanager
def get_channel() -> ContextManager[BlockingChannel]:
    """Handles the creation and clean up of a connection,
    giving the caller a connection channel to use.
    :return: class: `BlockingChannel`
    """
    try:
        connection = pika.BlockingConnection(parameters=BROKER_PARAMS)
        yield connection.channel()
        connection.close()
    except ConnectionClosed as err:
        print(err)
        raise


def setup_exchanges_and_queues(func) -> Callable[..., None]:
    """Setup required queues and exchanges on target broker.

    If they exist already they will be skipped.

    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        with get_channel() as channel:
            for queue_name in DEFAULT_QUEUES:
                channel.queue_declare(queue=queue_name, durable=True)

                for exchange in DEFAULT_QUEUES[queue_name]:
                    channel.exchange_declare(exchange=exchange, exchange_type='fanout', durable=True)
                    channel.queue_bind(exchange=exchange, queue=queue_name)

        return func(*args, **kwargs)

    return wrapper


@setup_exchanges_and_queues
def send_article_message(msg_type: str, article_id: str, article_version: int = None) -> None:
    """Create and send article event message.

    :param msg_type: str
    :param article_id: str
    :param article_version: int
    :return:
    """
    with get_channel() as channel:
        message = create_message(msg_type=msg_type, identifier=article_id,
                                 data={'article_version': article_version})

        channel.basic_publish(exchange=ARTICLES_EXCHANGE,
                              routing_key="",
                              body=json.dumps(message),
                              properties=pika.BasicProperties(delivery_mode=DELIVERY_MODE_PERSISTENT))


@contextmanager
def message_publisher(msg_type: str, article_id: str, article_version: int = None) -> ContextManager[None]:
    """Wrapper to send started/completed/failed messages for a given article `msg_type`.

    :param msg_type: str
    :param article_id: str
    :param article_version: int
    :return:
    """

    send_message = partial(send_article_message, article_id=article_id, article_version=article_version)

    try:
        send_message(f'{msg_type}.started')
        yield
        send_message(f'{msg_type}.completed')
    except Exception:
        send_message(f'{msg_type}.failed')


if __name__ == '__main__':
    pass
