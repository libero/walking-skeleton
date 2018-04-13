from libero_flow.event_utils import get_base_message


def test_can_get_base_message():
    base_msg = get_base_message()
    assert base_msg
    assert len(base_msg['eventId'])
    assert base_msg['happenedAt']
    assert len(base_msg['aggregate']) == 3
    assert base_msg['type'] == ''
    assert base_msg['data'] == {}
