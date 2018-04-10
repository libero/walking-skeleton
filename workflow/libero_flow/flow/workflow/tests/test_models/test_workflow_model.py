import pytest


@pytest.mark.django_db
def test_can_create_workflow(workflow):
    assert workflow
    assert workflow.instance_id
    assert workflow.name == 'FooWorkflow'
    assert workflow.status == 'Pending'
    assert workflow.start_timestamp
    assert workflow.config['foo'] == 'bar'


