import json

import pytest
from rest_framework.test import APIClient

from workflow.models import (
    Activity,
    Event,
    Workflow,
)


@pytest.fixture
@pytest.mark.django_db
def admin_rest_client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
@pytest.mark.django_db
def workflow():
    return Workflow.objects.create(name='FooWorkflow', config={"foo": "bar"})


@pytest.fixture
@pytest.mark.django_db
def event(workflow):
    return Event.objects.create(type='TestEvent', workflow=workflow)


@pytest.fixture
@pytest.mark.django_db
def workflow_with_input():
    return Workflow.objects.create(name='FooWorkflow', config={"foo": "bar"},
                                   input_data={"some": "data"})


@pytest.fixture
@pytest.mark.django_db
def activity(workflow):
    return Activity.objects.create(name='FooActivity', config={"foo": "bar"},
                                   workflow=workflow)


@pytest.fixture
def valid_activity_data(workflow):
    return {
        "name": "TestActivity",
        "workflow": workflow.instance_id
    }


@pytest.fixture
def valid_event_data(workflow):
    return {
        "type": "TestEvent",
        "workflow": workflow.instance_id
    }


@pytest.fixture
def valid_workflow_data():
    return {
        "name": "TestWorkflow",
        "config": json.dumps({"foo": "bar"})
    }


@pytest.fixture
def valid_workflow_data_with_input():
    return {
        "name": "TestWorkflow",
        "input_data": json.dumps({"article_id": "12345678"}),
        "config": json.dumps({"foo": "bar"})
    }

