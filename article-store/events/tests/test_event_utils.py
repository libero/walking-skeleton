from unittest.mock import MagicMock, patch

from events.utils import (
    create_message,
    get_channel,
    send_article_message,
    setup_exchanges,
)


def test_can_get_base_message():
    run_id = '2753d3ee-63de-11e8-9add-0242ac130008'
    base_msg = create_message(msg_type='foo.test', run_id=run_id)

    assert base_msg
    assert len(base_msg['eventId'])
    assert base_msg['happenedAt']
    assert base_msg['type'] == 'foo.test'
    assert base_msg['runId'] == run_id


def test_can_get_channel():
    assert get_channel()


@patch('events.utils.get_channel')
def test_setup_exchanges_and_queues(mock_get_channel: MagicMock):
    wrapped = setup_exchanges(MagicMock())
    wrapped()

    assert mock_get_channel.call_count == 1


@patch('events.utils.get_channel')
def test_can_send_article_message(mock_get_channel: MagicMock):
    channel = MagicMock(name='channel')
    mock_get_channel.return_value = channel
    send_article_message(msg_type='test-msg',
                         run_id='12345')

    assert mock_get_channel.call_count == 2
    assert channel.__enter__().basic_publish.called
