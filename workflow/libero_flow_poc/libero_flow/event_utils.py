from contextlib import contextmanager
from functools import wraps
from time import gmtime, strftime
from typing import Callable, ContextManager, Dict
import uuid

import pika
from pika.adapters.blocking_connection import BlockingChannel


DELIVERY_MODE_PERSISTENT = 2

HOST = 'localhost'
PORT = 5672
PASSWORD = 'guest'
USER = 'guest'

CREDENTIALS = pika.PlainCredentials(USER, PASSWORD)
PARAMS = pika.ConnectionParameters(host=HOST, credentials=CREDENTIALS)


ACTIVITY_RESULT_QUEUE = 'activity_results'
DECISION_RESULT_QUEUE = 'decision_results'
SCHEDULED_DECISION_QUEUE = 'scheduled_decisions'
SCHEDULED_ACTIVITY_QUEUE = 'scheduled_activities'
WORKFLOW_STARTER_QUEUE = 'workflow_starter'

ACTIVITY_RESULT_EXCHANGE = 'activity_result'
DECISION_RESULT_EXCHANGE = 'decision_result'
SCHEDULED_ACTIVITY_EXCHANGE = 'schedule_activity'
SCHEDULED_DECISION_EXCHANGE = 'schedule_decision'
WORKFLOW_STARTER_EXCHANGE = 'start_workflow'


DEFAULT_QUEUES = {
    ACTIVITY_RESULT_QUEUE: [
        ACTIVITY_RESULT_EXCHANGE
    ],
    DECISION_RESULT_QUEUE: [
        DECISION_RESULT_EXCHANGE
    ],
    SCHEDULED_ACTIVITY_QUEUE: [
        SCHEDULED_ACTIVITY_EXCHANGE
    ],
    SCHEDULED_DECISION_QUEUE: [
        SCHEDULED_DECISION_EXCHANGE
    ],
    WORKFLOW_STARTER_QUEUE: [
        WORKFLOW_STARTER_EXCHANGE
    ]
}


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
    connection = pika.BlockingConnection(parameters=PARAMS)
    yield connection.channel()
    connection.close()


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
