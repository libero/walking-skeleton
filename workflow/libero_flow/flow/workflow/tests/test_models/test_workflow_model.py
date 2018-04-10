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


