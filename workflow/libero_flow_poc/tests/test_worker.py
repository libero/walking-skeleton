from unittest.mock import patch, MagicMock

from libero_flow.worker import (
    activity_handler,
    run_activity,
    send_result_message,
)


@patch('libero_flow.worker.get_channel')
def test_can_send_result_message(mock_get_channel):
    mock_channel = MagicMock()
    mock_get_channel.return_value = mock_channel

    result = {
        'activity_id': 'c580c481-ee0b-490f-887d-e03bfc9d4d18',
        'result': 'Succeeded'
    }
    send_result_message(result)
    assert mock_channel.__enter__.call_count == 1
    assert mock_channel.__enter__().basic_publish.call_count == 1


@patch('libero_flow.worker.run_activity')
@patch('libero_flow.worker.send_result_message')
def test_can_handle_activity(mock_send_result_message, mock_run_activity):
    data = {
        "data": {"activity_id": "1b53d475-3704-46d3-9763-6a60c161362d"}
    }
    result = {
        'activity_id': 'c580c481-ee0b-490f-887d-e03bfc9d4d18',
        'result': 'Succeeded'
    }
    mock_run_activity.return_value = result
    activity_handler(data)
    assert mock_run_activity.call_count == 1
    assert mock_send_result_message.call_count == 1
