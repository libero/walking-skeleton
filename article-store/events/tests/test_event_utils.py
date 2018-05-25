from unittest.mock import MagicMock, patch

from events.utils import (
    create_message,
    get_channel,
    send_article_message,
    setup_exchanges,
)


def test_can_get_base_message():
    base_msg = create_message(msg_type='foo.test', identifier='someId', data={})
    assert base_msg
    assert len(base_msg['eventId'])
    assert base_msg['happenedAt']
    assert base_msg['type'] == 'foo.test'
    assert base_msg['data'] == {}
    assert base_msg['aggregate']['service'] == 'article-store'
    assert base_msg['aggregate']['name'] == 'article-version'
    assert base_msg['aggregate']['identifier'] == 'someId'


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
                         article_id='12345',
                         article_version=1)

    assert mock_get_channel.call_count == 2
    assert channel.__enter__().basic_publish.called
