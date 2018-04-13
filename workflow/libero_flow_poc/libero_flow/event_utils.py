from contextlib import contextmanager
from typing import ContextManager

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
WORKFLOW_STARTER_QUEUE = 'workflow_starter'

DECISION_RESULT_EXCHANGE = 'decision_result'
SCHEDULED_DECISION_EXCHANGE = 'schedule_decision'
WORKFLOW_STARTER_EXCHANGE = 'start_workflow'


DEFAULT_QUEUES = {
    ACTIVITY_RESULT_QUEUE: [],
    DECISION_RESULT_QUEUE: [
        DECISION_RESULT_EXCHANGE
    ],
    SCHEDULED_DECISION_QUEUE: [
        SCHEDULED_DECISION_EXCHANGE
    ],
    WORKFLOW_STARTER_QUEUE: [
        WORKFLOW_STARTER_EXCHANGE
    ]
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


def setup_exchanges_and_queues() -> None:
    """Setup required queues and exchanges on target broker.

    If they exist already they will be skipped.

    :return:
    """
    with get_channel() as channel:

        for queue_name in DEFAULT_QUEUES:
            channel.queue_declare(queue=queue_name, durable=True)

            for exchange in DEFAULT_QUEUES[queue_name]:
                channel.exchange_declare(exchange=exchange,
                                         exchange_type='fanout',
                                         durable=True)

                channel.queue_bind(exchange=exchange, queue=queue_name)


if __name__ == '__main__':
    pass
