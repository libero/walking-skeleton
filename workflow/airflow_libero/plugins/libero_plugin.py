from contextlib import contextmanager
from functools import wraps
import json
import os
from time import gmtime, strftime
from typing import (
    Any,
    Callable,
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
DEFAULT_EXCHANGES = [ARTICLES_EXCHANGE]
DELIVERY_MODE_PERSISTENT = 2


def create_message(msg_type: str, run_id: str, message: Optional[str] = '') -> Dict:
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


def declare_exchanges() -> None:
    """Declare all default exchanges.

    :return:
    """
    with get_channel() as channel:
        for exchange in DEFAULT_EXCHANGES:
            channel.exchange_declare(exchange=exchange, exchange_type='fanout', durable=True)


def setup_exchanges(func) -> Callable[..., None]:
    """Setup required exchanges on target broker.

    If they exist already they will be skipped.

    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        declare_exchanges()
        return func(*args, **kwargs)

    return wrapper


class EventEmittingPythonOperator(PythonOperator):

    def __init__(self, *args, **kwargs):
        super(EventEmittingPythonOperator, self).__init__(*args, **kwargs)

    def execute_callable(self):
        try:
            result = None

            self.publish_event(f'{self.python_callable.__name__}.started')
            result = self.python_callable(*self.op_args, **self.op_kwargs)
            self.publish_event(f'{self.python_callable.__name__}.completed')
        except Exception:
            self.publish_event(f'{self.python_callable.__name__}.failed')
            raise
        finally:
            return result

    def publish_event(self, msg_type: str):
        with get_channel() as channel:
            message = create_message(msg_type=msg_type, run_id='2753d3ee-63de-11e8-9add-0242ac130008')

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
