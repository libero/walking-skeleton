import json
from time import gmtime, strftime
from typing import Dict
import uuid

import pika

from libero_flow.state_utils import (
    CANCELLED,
    FINISHED,
    IN_PROGRESS,
    PENDING,
    PERMANENT_FAILURE,
    SUCCEEDED,
    TEMPORARY_FAILURE,
)
from libero_flow.event_utils import (
    get_channel,
    setup_exchanges_and_queues,
    DELIVERY_MODE_PERSISTENT,
    DECISION_RESULT_EXCHANGE,
    DECISION_RESULT_QUEUE,
    SCHEDULED_DECISION_QUEUE,
)
from libero_flow.state_utils import get_workflow_state


def send_decision_message(decision: Dict):
    """create and send decision task message.

    :param decision: dict
    :return:
    """
    with get_channel() as channel:
        message = {
            "eventId": str(uuid.uuid1()),
            "happenedAt": strftime("%Y-%m-%dT%H:%M:%S+00:00", gmtime()),
            "aggregate": {
                "service": "flow-decider",
                "name": "workflow-decision",
                "identifier": "??",
            },
            "type": "decision-task-result",
            "data": decision
        }

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

            if activity['status'] == SUCCEEDED:
                continue

            elif activity['status'] == PENDING:
                # check if pending activity should be listed to be started
                if not activity['independent'] and not len(activities_to_schedule):
                    activities_to_schedule.append(activity)
                elif activity['independent']:
                    activities_to_schedule.append(activity)

            elif activity['status'] == TEMPORARY_FAILURE:
                # TODO check required
                pass

            elif activity['status'] == PERMANENT_FAILURE:
                # a required activity has failed permanently, fail the workflow
                if activity['required']:
                    decision['decision'] = 'workflow-failure'

        decision['activities'] = activities_to_schedule

        if not decision['activities'] and decision['decision'] == 'schedule-activities':
            # no activities outstanding and no failures, complete the workflow then
            decision['decision'] = 'workflow-finished'

    return decision


def scheduled_decision_message_handler(channel: pika.channel.Channel,
                                       method: pika.spec.Basic.Deliver,
                                       properties: pika.spec.BasicProperties, body: str) -> None:
    print(f'[x] scheduled decision handler received: {body}')

    try:
        data = json.loads(body)
        workflow_id = data['data']['workflow_id']

        decision = decide(workflow=get_workflow_state(workflow_id=workflow_id))
        send_decision_message(decision)
    except json.decoder.JSONDecodeError as err:
        print(err)

    channel.basic_ack(method.delivery_tag)


@setup_exchanges_and_queues
def main():
    with get_channel() as channel:
        print('Decider running...')
        print(' [*] Waiting for Messages. To exit press CTRL+C')

        channel.basic_consume(scheduled_decision_message_handler, queue=SCHEDULED_DECISION_QUEUE, no_ack=False)

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()


if __name__ == '__main__':
    pass
