import pytest

from workflow.models import Workflow


@pytest.mark.django_db
def test_can_create_workflow_via_post(admin_client, valid_workflow_data):
    response = admin_client.post('/workflows/api/v1/workflows/', data=valid_workflow_data)
    assert response.status_code == 201
    assert Workflow.objects.count() == 1


@pytest.mark.django_db
def test_can_get_workflow(admin_client, workflow):
    response = admin_client.get('/workflows/api/v1/workflows/')
    assert response.status_code == 200
    assert len(response.data) == 1
