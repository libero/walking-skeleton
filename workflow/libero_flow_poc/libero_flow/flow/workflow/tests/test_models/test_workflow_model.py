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


@pytest.mark.django_db
def test_will_add_start_timestamp_to_in_progress_workflow(workflow):
    assert not workflow.start_timestamp

    workflow.status = 'In Progress'
    workflow.save()

    assert workflow.start_timestamp


@pytest.mark.django_db
def test_will_add_end_timestamp_to_in_progress_workflow(workflow):
    assert not workflow.end_timestamp

    workflow.status = 'Finished'
    workflow.save()

    assert workflow.end_timestamp
