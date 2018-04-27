from libero_flow.activities.base_activity import BaseActivity


def test_can_create_activity():
    activity = BaseActivity('12345678', {}, None)
    assert activity


def test_can_set_value_on_session_using_workflow_namespace(mock_session):
    session = mock_session()
    activity = BaseActivity('12345678', {}, session)
    activity.session_set('foo', 'bar')
    assert session['12345678_foo'] == 'bar'


def test_can_get_value_from_session_using_workflow_namespace(mock_session):
    session = mock_session()
    activity = BaseActivity('12345678', {}, session)
    activity.session_set('result', 'some_value')
    assert activity.session_get('result') == 'some_value'
