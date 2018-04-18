from abc import ABC, abstractmethod
from typing import Dict


class Activity(ABC):
    @abstractmethod
    def do_activity(self, data=None) -> str:
        raise NotImplementedError


class BaseActivity(Activity):

    IN_PROGRESS = 'In Progress'
    PENDING = 'Pending'
    PERMANENT_FAILURE = "Permanent Failure"
    SCHEDULED = 'Scheduled'
    SUCCEEDED = 'Succeeded'
    TEMPORARY_FAILURE = "Temporary Failure"

    def __init__(self, workflow_id: str, config: Dict, session=None):
        self.config = config
        self.session = session
        self.workflow_id = workflow_id

    def do_activity(self) -> str:
        """Perform actions.

        :return: str
        """
        return self.PERMANENT_FAILURE

    def session_get(self, key: str) -> str:
        """Get a value by key on the activities workflow session

        :param key: str
        :return:
        """
        value = self.session.get(f'{self.workflow_id}_{key}')
        if value:
            return value.decode("utf-8")

    def session_set(self, key: str, value: str) -> None:
        """Set a value by key on the activities workflow session

        :param key: str
        :param value: str
        :return:
        """
        self.session.set(f'{self.workflow_id}_{key}', value)
