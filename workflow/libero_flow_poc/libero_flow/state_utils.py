from typing import Dict

import requests

from libero_flow.conf import ACTIVITY_API_URL, WORKFLOW_API_URL


CANCELLED = 'Cancelled'
FAILED = 'Failed'
FINISHED = 'Finished'
IN_PROGRESS = 'In Progress'
PENDING = 'Pending'
PERMANENT_FAILURE = 'Permanent Failure'
SCHEDULED = 'Scheduled'
SUCCEEDED = 'Succeeded'
TEMPORARY_FAILURE = 'Temporary Failure'


def get_activity_state(activity_id: str) -> Dict:
    """Get activity state via workflow API.

    :param activity_id: str
    :return: dict
    """
    response = requests.get(f'{ACTIVITY_API_URL}{activity_id}/')
    return response.json()


def get_workflow_state(workflow_id: str) -> Dict:
    """Get workflow state via workflow API.

    :param workflow_id: str
    :return: dict
    """
    response = requests.get(f'{WORKFLOW_API_URL}{workflow_id}/')
    return response.json()


def update_activity_status(activity_id: str, status: str) -> Dict:
    """Update activity status field via workflow API.

    :param activity_id: str
    :param status: str
    :return: dict
    """
    data = {'status': status}
    response = requests.patch(f'{ACTIVITY_API_URL}{activity_id}/', data=data)
    return response.json()


def update_workflow_status(workflow_id: str, status: str) -> Dict:
    """Update workflow status field via workflow API.

    :param workflow_id:
    :return:
    """
    data = {'status': status}
    response = requests.patch(f'{WORKFLOW_API_URL}{workflow_id}/', data=data)
    return response.json()
