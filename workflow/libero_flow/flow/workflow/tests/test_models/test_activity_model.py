import pytest


@pytest.mark.django_db
def test_can_create_activity(activity):
    assert activity
    assert activity.instance_id
    assert activity.name == 'FooActivity'
    assert activity.status == 'Pending'
    assert activity.config['foo'] == 'bar'
    assert activity.workflow
