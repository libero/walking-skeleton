from contextlib import contextmanager
from functools import partial
import json
import os
from time import gmtime, strftime
from typing import (
    ContextManager,
    Dict,
    Optional,
)
import uuid

from airflow.plugins_manager import AirflowPlugin
from airflow.operators.python_operator import PythonOperator
import pika
from pika.exceptions import ConnectionClosed
from pika.adapters.blocking_connection import BlockingChannel


RABBITMQ_URL = os.environ.get('RABBITMQ_URL', '')
BROKER_PARAMS = pika.connection.URLParameters(RABBITMQ_URL)
ARTICLES_EXCHANGE = 'articles'


def create_message(msg_type: str, run_id: str, message: Optional[str] = None) -> Dict:
    """Create a message `dict` based on a standard schema.
    :return: Dict
    """
    return {
        "eventId": str(uuid.uuid1()),
        "runId": run_id,
        "happenedAt": strftime("%Y-%m-%dT%H:%M:%S+00:00", gmtime()),
        "type": f'article.version.{msg_type}',
        "message": message
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


class EventEmittingPythonOperator(PythonOperator):

    def __init__(self, *args, **kwargs):
        super(EventEmittingPythonOperator, self).__init__(*args, **kwargs)

    def execute_callable(self):
        try:
            result = None
            run_id = self.op_kwargs['dag_run'].conf.get('input_data')['run_id']
            send_message = partial(self.send_message, run_id=run_id)

            send_message(f'{self.task_id}.started')
            result = self.python_callable(*self.op_args, **self.op_kwargs)
            send_message(f'{self.task_id}.completed')
        except Exception as exception:
            send_message(f'{self.task_id}.failed', message=str(exception))
            raise
        finally:
            return result

    @staticmethod
    def send_message(msg_type: str, run_id: str, message: Optional[str] = None) -> None:
        with get_channel() as channel:
            message = create_message(msg_type=msg_type, run_id=run_id, message=message)

            channel.basic_publish(exchange=ARTICLES_EXCHANGE,
                                  routing_key="",
                                  body=json.dumps(message))


class LiberoPlugin(AirflowPlugin):
    name = "libero_plugin"
    operators = [EventEmittingPythonOperator]
    hooks = []
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []
