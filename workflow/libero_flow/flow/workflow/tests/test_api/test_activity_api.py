import pytest

from workflow.models import Activity


@pytest.mark.django_db
def test_can_create_activity_via_post(admin_client, valid_activity_data):
    response = admin_client.post('/workflows/api/v1/activities/', data=valid_activity_data)
    assert response.status_code == 201
    assert Activity.objects.count() == 1


@pytest.mark.django_db
def test_can_get_workflow(admin_client, activity):
    response = admin_client.get('/workflows/api/v1/activities/')
    assert response.status_code == 200
    assert len(response.data) == 1
