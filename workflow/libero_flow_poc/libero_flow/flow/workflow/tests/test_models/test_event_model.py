import pytest


@pytest.mark.django_db
def test_can_create_event(event):
    assert event.id
    assert event.created
    assert event.type == 'TestEvent'
    assert event.workflow
