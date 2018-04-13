import pytest


@pytest.fixture
def base_workflow_state():
    return {
        "instance_id": "8eed4f02-4d3c-4fb2-89f8-1507374ae541",
        "name": "FooBarWorkflow",
        "status": "Pending",
        "created": "2018-04-11T12:23:34.236207Z",
        "start_timestamp": None,
        "end_timestamp": None,
        "config": {
            "timeout": 300
        },
        "input_data": {
            "timeout": 12355
        },
        "activities": [
            {
                "instance_id": "c058cd3f-93c4-4d2d-a0f4-d6eae5a3e6e2",
                "name": "PingWorker",
                "independent": False,
                "required": True,
                "status": "Pending",
                "config": {
                    "foo": "bar"
                },
                "workflow": "8eed4f02-4d3c-4fb2-89f8-1507374ae541"
            },
            {
                "instance_id": "e05678d0-20b0-4a75-8452-4be151c71461",
                "name": "SumValues",
                "independent": False,
                "required": True,
                "status": "Pending",
                "config": {
                    "foo": "bar"
                },
                "workflow": "8eed4f02-4d3c-4fb2-89f8-1507374ae541"
            }
        ]
    }


@pytest.fixture(name='wf_with_multi_independent_acts')
def base_workflow_state_with_multi_independent_activities():
    return {
        "instance_id": "8eed4f02-4d3c-4fb2-89f8-1507374ae541",
        "name": "FooBarWorkflow",
        "status": "In Progress",
        "created": "2018-04-11T12:23:34.236207Z",
        "start_timestamp": None,
        "end_timestamp": None,
        "config": {
            "timeout": 300
        },
        "input_data": {
            "timeout": 12355
        },
        "activities": [
            {
                "instance_id": "c058cd3f-93c4-4d2d-a0f4-d6eae5a3e6e2",
                "name": "CloneXML",
                "independent": True,
                "required": True,
                "status": "Pending",
                "config": {
                    "foo": "bar"
                },
                "workflow": "8eed4f02-4d3c-4fb2-89f8-1507374ae541"
            },
            {
                "instance_id": "e05678d0-20b0-4a75-8452-4be151c71461",
                "name": "GeneratePDF",
                "independent": True,
                "required": True,
                "status": "Pending",
                "config": {
                    "foo": "bar"
                },
                "workflow": "8eed4f02-4d3c-4fb2-89f8-1507374ae541"
            },
            {
                "instance_id": "e05678d0-20b0-4a75-8452-4be151c71461",
                "name": "ArchiveXML",
                "independent": False,
                "required": True,
                "status": "Pending",
                "config": {
                    "foo": "bar"
                },
                "workflow": "8eed4f02-4d3c-4fb2-89f8-1507374ae541"
            }
        ]
    }


@pytest.fixture
def workflow_with_pending_state(base_workflow_state):
    return base_workflow_state


@pytest.fixture
def workflow_with_finished_state(base_workflow_state):
    base_workflow_state['status'] = 'Finished'
    return base_workflow_state


@pytest.fixture
def workflow_with_cancelled_state(base_workflow_state):
    base_workflow_state['status'] = 'Cancelled'
    return base_workflow_state


@pytest.fixture
def workflow_with_in_progress_state(base_workflow_state):
    base_workflow_state['status'] = 'In Progress'
    return base_workflow_state


@pytest.fixture
def workflow_with_perma_failed_required_activity(base_workflow_state):
    base_workflow_state['status'] = 'In Progress'
    base_workflow_state['activities'][0]['status'] = 'Permanent Failure'
    return base_workflow_state
