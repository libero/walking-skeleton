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
