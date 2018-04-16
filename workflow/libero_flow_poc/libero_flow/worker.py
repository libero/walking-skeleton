import json
from typing import Any, Dict

import pika

from libero_flow.flow_loader import FlowLoader
from libero_flow.event_utils import (
    get_base_message,
    get_channel,
    message_handler,
    setup_exchanges_and_queues,
    ACTIVITY_RESULT_EXCHANGE,
    ACTIVITY_RESULT_QUEUE,
    DELIVERY_MODE_PERSISTENT,
    SCHEDULED_ACTIVITY_QUEUE,
)
from libero_flow.state_utils import (
    get_activity_state,
    update_activity_status,
)


def run_activity(activity_id: str) -> Dict:
    """

    :param activity_id: str
    :return: dict
    """

    update_activity_status(activity_id, status='In Progress')

    result = {
        'activity_id': activity_id,
        'result': ''
    }

    loader = FlowLoader()
    activity_state = get_activity_state(activity_id=activity_id)

    print('activity state: ', activity_state)
    activity_class = loader.get_activity(activity_state['name'])
    print('activity class: ', activity_class)

    if activity_class:
        # get session
        # TODO session interface
        session = None

        activity = activity_class(workflow_id=activity_state['workflow'],
                                  config=activity_state['config'],
                                  session=session)
        result['result'] = activity.do_activity()
    else:
        result['result'] = 'no-activity-found'

    return result


def send_result_message(result: Dict):
    """create and send decision task message.

    :param result: dict
    :return:
    """
    with get_channel() as channel:
        message = get_base_message()
        message['aggregate']['service'] = 'flow-worker'
        message['aggregate']['name'] = 'flow-worker'
        message['type'] = 'activity-worker-result'
        message['data'] = result

        channel.basic_publish(exchange=ACTIVITY_RESULT_EXCHANGE,
                              routing_key=ACTIVITY_RESULT_QUEUE,
                              body=json.dumps(message),
                              properties=pika.BasicProperties(delivery_mode=DELIVERY_MODE_PERSISTENT))
        print(f'[x] Schedule activity result sent: {message}\n')


def activity_handler(data: Dict[str, Any]) -> None:
    print(f'[x] scheduled activity handler received: {data}')

    """
    '{"eventId": "9052435a-3f06-11e8-95ff-8c85905818e6", "happenedAt": "2018-04-13T10:36:45+00:00", "aggregate": {"service": "flow-scheduler", "name": "schedule-workflow-activity", "identifier": "??"}, "type": "schedule-activity", "data": {"activity_id": "1b53d475-3704-46d3-9763-6a60c161362d"}}'

    """
    # TODO needs to be passed to celery here or launch thread/process
    result = run_activity(data['data']['activity_id'])
    send_result_message(result)


@setup_exchanges_and_queues
def main():
    with get_channel() as channel:
        print('Worker running...')
        print(' [*] Waiting for Messages. To exit press CTRL+C')

        channel.basic_consume(message_handler(activity_handler), queue=SCHEDULED_ACTIVITY_QUEUE, no_ack=False)

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()


if __name__ == '__main__':
    pass
