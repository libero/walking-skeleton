from libero_flow.conf import SESSION_HOST, SESSION_PORT
from libero_flow.session_store.session import BaseSession, RedisSession


DEFAULT_SESSION_TYPE = 'redis'

SESSION_TYPES = {
    'redis': RedisSession
}


def get_session(session_type=DEFAULT_SESSION_TYPE) -> BaseSession:
    """Return initiated `BaseSession` object to caller.

    :param session_type: str
    :return: class: BaseSession
    """
    return SESSION_TYPES[session_type](SESSION_HOST, SESSION_PORT)
