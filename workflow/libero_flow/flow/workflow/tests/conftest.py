import json

import pytest

from workflow.models import Activity, Workflow


@pytest.fixture
@pytest.mark.django_db
def workflow():
    return Workflow.objects.create(name='FooWorkflow', config={"foo": "bar"})


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

