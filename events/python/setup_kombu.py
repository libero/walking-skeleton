from contextlib import contextmanager
from typing import ContextManager

from kombu import Connection


ARTICLE_EXCHANGE_NAME = 'articles'
DASHBOARD_QUEUE_NAME = 'dashboard'
DELIVERY_MODE_PERSISTENT = 2

HOST = 'localhost'
PORT = 5672
PASSWORD = 'guest'
USER = 'guest'


@contextmanager
def get_connection() -> ContextManager[Connection]:
    """Handles the creation and clean up of a connection.

    :return: class: `Connection`
    """
    connection = Connection(f'amqp://{USER}:{PASSWORD}@{HOST}:{PORT}//',
                            transport_options={'confirm_publish': True})
    yield connection
    connection.release()
