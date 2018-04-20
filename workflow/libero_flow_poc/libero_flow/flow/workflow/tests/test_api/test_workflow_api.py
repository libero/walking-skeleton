import pytest

from workflow.models import Workflow


@pytest.mark.django_db
def test_can_create_workflow_via_post(admin_client, valid_workflow_data):
    response = admin_client.post('/workflows/api/v1/workflows/', data=valid_workflow_data)
    assert response.status_code == 201
    assert Workflow.objects.count() == 1


@pytest.mark.django_db
def test_can_get_workflows(admin_client, workflow):
    response = admin_client.get('/workflows/api/v1/workflows/')
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_can_create_workflow_with_input_data(admin_client, valid_workflow_data_with_input):
    response = admin_client.post('/workflows/api/v1/workflows/', data=valid_workflow_data_with_input)
    assert response.status_code == 201
    assert Workflow.objects.count() == 1


@pytest.mark.django_db
def test_can_update_workflow_via_patch(admin_rest_client, workflow):
    payload = {"status": "In Progress"}

    response = admin_rest_client.patch(f'/workflows/api/v1/workflows/{workflow.instance_id}/', data=payload)
    assert response.status_code == 200

    workflow = Workflow.objects.get(instance_id=workflow.instance_id)
    assert workflow.status == 'In Progress'


@pytest.mark.django_db
def test_workflow_response_contains_activities(admin_client, workflow, activity):
    response = admin_client.get(f'/workflows/api/v1/workflows/{workflow.instance_id}/')
    data = response.data
    assert response.status_code == 200
    assert len(data['activities']) == 1


@pytest.mark.django_db
def test_workflow_response_contains_events(admin_client, workflow, event):
    response = admin_client.get(f'/workflows/api/v1/workflows/{workflow.instance_id}/')
    data = response.data
    assert response.status_code == 200
    assert len(data['events']) == 2
