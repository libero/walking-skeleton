import pytest

from workflow.models import Event


@pytest.mark.django_db
def test_can_create_event_via_post(admin_client, valid_event_data):
    response = admin_client.post('/workflows/api/v1/events/', data=valid_event_data)
    assert response.status_code == 201
    assert Event.objects.count() == 2


@pytest.mark.django_db
def test_can_get_events(admin_client, event):
    response = admin_client.get('/workflows/api/v1/events/')
    assert response.status_code == 200
    assert len(response.data) == 2
