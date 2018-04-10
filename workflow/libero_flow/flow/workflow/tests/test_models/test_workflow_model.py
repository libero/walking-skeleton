import pytest


@pytest.mark.django_db
def test_can_create_workflow(workflow):
    assert workflow
    assert workflow.config['foo'] == 'bar'
    assert workflow.created
    assert not workflow.end_timestamp
    assert workflow.instance_id
    assert workflow.name == 'FooWorkflow'
    assert not workflow.start_timestamp
    assert workflow.status == 'Pending'


@pytest.mark.django_db
def test_can_create_workflow_with_input_data(workflow_with_input):
    assert workflow_with_input
    assert workflow_with_input.config['foo'] == 'bar'
    assert workflow_with_input.created
    assert not workflow_with_input.end_timestamp
    assert workflow_with_input.instance_id
    assert workflow_with_input.name == 'FooWorkflow'
    assert not workflow_with_input.start_timestamp
    assert workflow_with_input.status == 'Pending'
