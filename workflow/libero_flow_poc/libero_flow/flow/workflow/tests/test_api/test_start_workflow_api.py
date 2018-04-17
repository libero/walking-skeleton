import pytest


@pytest.mark.django_db
def test_can_start_workflow_via_post(admin_client):
    payload = {"name": "FooBarWorkflow", "input_data": {"timeout": 300}}
    response = admin_client.post('/workflows/api/v1/start-workflow/', data=payload)
    assert response.status_code == 200


@pytest.mark.django_db
def test_will_receive_error_message_if_data_is_invalid(admin_client):
    payload = {"input_data": {"timeout": 300}}
    response = admin_client.post('/workflows/api/v1/start-workflow/', data=payload)
    assert response.status_code == 400
