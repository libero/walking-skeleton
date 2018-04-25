from contextlib import contextmanager
from functools import wraps
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


BROKER_HOST = 'rabbitmq'
BROKER_PORT = 5672
BROKER_PASSWORD = 'guest'
BROKER_USER = 'guest'

BROKER_CREDENTIALS = pika.PlainCredentials(BROKER_USER, BROKER_PASSWORD)
BROKER_PARAMS = pika.ConnectionParameters(host=BROKER_HOST, credentials=BROKER_CREDENTIALS)

TASK_EVENT_EXCHANGE = 'task_event'
TASK_EVENT_QUEUE = 'task_events'

DEFAULT_QUEUES = {
    TASK_EVENT_QUEUE: [
        TASK_EVENT_EXCHANGE
    ]
}


DELIVERY_MODE_PERSISTENT = 2


def get_base_message() -> Dict:
    """

    :return:
    """
    return {
        "eventId": str(uuid.uuid1()),
        "happenedAt": strftime("%Y-%m-%dT%H:%M:%S+00:00", gmtime()),
        "aggregate": {
            "service": "",
            "name": "",
            "identifier": "",
        },
        "type": "",
        "data": {}
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


def message_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    """Message handler wrapper that handles passing the parsed message body
    to wrapped `func` and ack'ing the message after completion.

    :param func:
    :return:
    """
    def handler(channel: pika.channel.Channel = None,
                method: pika.spec.Basic.Deliver = None,
                properties: pika.spec.BasicProperties = None,
                body: str = '') -> Any:
        try:
            data = json.loads(body)
            func(data)
            channel.basic_ack(method.delivery_tag)
        except json.decoder.JSONDecodeError as err:
            # logger.exception(exception)
            pass

    return handler


def setup_exchanges_and_queues(func) -> Callable[..., None]:
    """Setup required queues and exchanges on target broker.

    If they exist already they will be skipped.

    :return:
    """
    @wraps(func)
    def wrapper():
        with get_channel() as channel:
            for queue_name in DEFAULT_QUEUES:
                channel.queue_declare(queue=queue_name, durable=True)

                for exchange in DEFAULT_QUEUES[queue_name]:
                    channel.exchange_declare(exchange=exchange, exchange_type='fanout', durable=True)
                    channel.queue_bind(exchange=exchange, queue=queue_name)

        return func()

    return wrapper


if __name__ == '__main__':
    pass
