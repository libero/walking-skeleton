import json
import logging
import time
from typing import Any, Dict

import pika
from pika.exceptions import (
    ChannelClosed,
    ConnectionClosed,
    IncompatibleProtocolError
)
from libero_flow.conf import (
    DECISION_RESULT_EXCHANGE,
    DECISION_RESULT_QUEUE,
    SCHEDULED_DECISION_QUEUE,
)
from libero_flow.state_utils import (
    CANCELLED,
    FINISHED,
    IN_PROGRESS,
    PENDING,
    PERMANENT_FAILURE,
    SCHEDULED,
    SUCCEEDED,
    TEMPORARY_FAILURE,
)
from libero_flow.event_utils import (
    get_base_message,
    get_channel,
    message_handler,
    setup_exchanges_and_queues,
    DELIVERY_MODE_PERSISTENT,
)
from libero_flow.state_utils import get_workflow_state


logger = logging.getLogger(__name__)
fh = logging.FileHandler(f'{__name__}.log')
logger.addHandler(fh)


def send_decision_message(decision: Dict):
    """create and send decision task message.

    :param decision: dict
    :return:
    """
    with get_channel() as channel:
        message = get_base_message()
        message['aggregate']['service'] = 'flow-decider'
        message['aggregate']['name'] = 'workflow-decision'
        message['type'] = 'decision-task-result'
        message['data'] = decision

        channel.basic_publish(exchange=DECISION_RESULT_EXCHANGE,
                              routing_key=DECISION_RESULT_QUEUE,
                              body=json.dumps(message),
                              properties=pika.BasicProperties(delivery_mode=DELIVERY_MODE_PERSISTENT))
        print(f'[x] Schedule decision sent: {message}')


def decide(workflow: Dict) -> Dict:
    """Look at the current workflow state and decide on the next action.

    example `workflow` value:

    {
        "instance_id": "8eed4f02-4d3c-4fb2-89f8-1507374ae541",
        "name": "FooBarWorkflow",
        "status": "Pending",
        "created": "2018-04-11T12:23:34.236207Z",
        "start_timestamp": null,
        "end_timestamp": null,
        "config": {
            "timeout": 300
        },
        "input_data": {
            "timeout": 12355
        },
        "activities": [
            {
                "instance_id": "c058cd3f-93c4-4d2d-a0f4-d6eae5a3e6e2",
                "name": "PingWorker",
                "independent": false,
                "required": true,
                "status": "Pending",
                "config": {
                    "foo": "bar"
                },
                "workflow": "8eed4f02-4d3c-4fb2-89f8-1507374ae541"
            },
            {
                "instance_id": "e05678d0-20b0-4a75-8452-4be151c71461",
                "name": "SumValues",
                "independent": false,
                "required": true,
                "status": "Pending",
                "config": {
                    "foo": "bar"
                },
                "workflow": "8eed4f02-4d3c-4fb2-89f8-1507374ae541"
            }
        ]
    }

    :param workflow:
    :return: dict
    """
    decision = {
        'workflow_id': workflow['instance_id'],
        'decision': ''
    }

    # TODO replace temp logic tree with more extendable methods?
    # check current workflow state
    if workflow['status'] == FINISHED:
        decision['decision'] = 'do-nothing'

    elif workflow['status'] == CANCELLED:
        decision['decision'] = 'do-nothing'

    elif workflow['status'] == PENDING:
        decision['decision'] = 'start-workflow'

    elif workflow['status'] == IN_PROGRESS:
        # do some real work
        activities_to_schedule = []
        decision['decision'] = 'schedule-activities'

        for activity in workflow['activities']:

            if activity['status'] in [SUCCEEDED, SCHEDULED]:
                continue

            elif activity['status'] == PENDING:
                # check if pending activity should be listed to be started
                if not activity['independent'] and not len(activities_to_schedule):
                    activities_to_schedule.append(activity)
                elif activity['independent']:
                    activities_to_schedule.append(activity)

            elif activity['status'] == TEMPORARY_FAILURE:
                # TODO check max_retries
                activities_to_schedule.append(activity)

            elif activity['status'] == PERMANENT_FAILURE:
                # a required activity has failed permanently, fail the workflow
                if activity['required']:
                    decision['decision'] = 'workflow-failure'

        decision['activities'] = activities_to_schedule

        if not decision['activities'] and decision['decision'] == 'schedule-activities':
            # no activities outstanding and no failures? complete the workflow then...
            decision['decision'] = 'workflow-finished'

    return decision


def decision_handler(data: Dict[str, Any]) -> None:
    print(f'[x] scheduled decision handler received: {data}')

    try:
        workflow_id = data['data'].get('workflow_id')

        if workflow_id:
            decision = decide(workflow=get_workflow_state(workflow_id=workflow_id))
            send_decision_message(decision)
    except AttributeError as err:
        # log err and state invalid data format / type
        pass


@setup_exchanges_and_queues
def main():
    while True:
        try:
            with get_channel() as channel:
                print('Decider running...')
                print('[*] Waiting for Messages. To exit press CTRL+C')

                channel.basic_consume(message_handler(decision_handler), queue=SCHEDULED_DECISION_QUEUE, no_ack=False)

                channel.start_consuming()

        except (ChannelClosed, ConnectionClosed, IncompatibleProtocolError) as err:
            # lost connection
            logger.exception('Lost connection... waiting before retry')
            time.sleep(5)
        except KeyboardInterrupt:
            channel.stop_consuming()
            break


if __name__ == '__main__':
    pass
