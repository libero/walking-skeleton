from abc import ABC, abstractmethod
from typing import Dict


class Activity(ABC):
    @abstractmethod
    def do_activity(self, data=None) -> str:
        raise NotImplementedError


class BaseActivity(Activity):
    """
    **complete**
    """

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
        """

        :return:
        """
        return self.PERMANENT_FAILURE

    def session_get(self, key: str) -> None:
        """Get a value by key on the activities workflow session

        :param key: str
        :param value: str
        :return: bool
        """
        return self.session.get(f'{self.workflow_id}_{key}')

    def session_set(self, key: str, value: str) -> None:
        """Set a value by key on the activities workflow session

        :param key: str
        :param value: str
        :return: bool
        """
        self.session.set(f'{self.workflow_id}_{key}', value)
