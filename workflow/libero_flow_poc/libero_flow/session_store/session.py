from abc import ABC, abstractmethod

import redis


class BaseSession(ABC):
    @abstractmethod
    def get(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def set(self, key: str, value: str) -> None:
        raise NotImplementedError


class RedisSession(BaseSession):

    def __init__(self, host: str, port: int, db: int = 0):
        """Initiate target redis connection and bind to `self.session`.

        :param host: str
        :param port: int
        :param db: int
        """
        self.host = host
        self.port = port
        self.db = db
        self.session = redis.StrictRedis(host=self.host, port=self.port, db=self.db)

    def get(self, key: str) -> str:
        """Retrieve value by key from session.

        :param key:
        :return: str
        """
        return self.session.get(key)

    def set(self, key: str, value: str) -> None:
        """Set value by key on session.

        :param key:
        :param value:
        :return:
        """
        self.session.set(key, value)

    # TODO rpush

    # TODO rllen

    # TODO rlindex

    # TODO lrem

    # TODO lset
