import copy
import json
import sys
from time import gmtime, strftime
from typing import Any, Dict
import uuid

import pika
import requests

from libero_flow.conf import ACTIVITY_API_URL, WORKFLOW_API_URL
from libero_flow.flow_loader import FlowLoader
from libero_flow.event_utils import (
    get_channel,
    setup_exchanges_and_queues,
    DELIVERY_MODE_PERSISTENT,
    SCHEDULED_ACTIVITY_EXCHANGE,
    SCHEDULED_DECISION_EXCHANGE,
    ACTIVITY_RESULT_QUEUE,
    DECISION_RESULT_QUEUE,
    SCHEDULED_ACTIVITY_QUEUE,
    SCHEDULED_DECISION_QUEUE,
    WORKFLOW_STARTER_QUEUE,
)
from libero_flow.state_utils import (
    get_activity_state,
    update_activity_status,
    update_workflow_status,
    FINISHED,
)

# Will watch queue for WorkflowStart, DecisionResult and ActivityResult
"""
DecisionResult:
    - handle_decision()
        - Will update workflow state
        - May Schedule an Activity
        - May Complete a workflow
"""


# Receive a `success` state back from activity worker --------

# get workflow_id from result and get workflow state

# update activity state to success

# Receive a `success` state back from activity worker --------


def schedule_activity(activity_id: str) -> None:
    """create and send schedule activity message.

    :param activity_id: str
    :return:
    """
    with get_channel() as channel:
        message = {
            "eventId": str(uuid.uuid1()),
            "happenedAt": strftime("%Y-%m-%dT%H:%M:%S+00:00", gmtime()),
            "aggregate": {
                "service": "flow-scheduler",
                "name": "schedule-workflow-activity",
                "identifier": "??",
            },
            "type": "schedule-activity",
            "data": {
                "activity_id": activity_id
            }
        }

        channel.basic_publish(exchange=SCHEDULED_ACTIVITY_EXCHANGE,
                              routing_key=SCHEDULED_ACTIVITY_QUEUE,
                              body=json.dumps(message),
                              properties=pika.BasicProperties(delivery_mode=DELIVERY_MODE_PERSISTENT))
        print(f'[x] Schedule activity sent: {message}')

        # TODO send event message saying scheduled a decision task


def schedule_decision(workflow_id: str) -> None:
    """create and send scheduled decision message.

    :param workflow_id: str
    :return:
    """
    with get_channel() as channel:
        message = {
            "eventId": str(uuid.uuid1()),
            "happenedAt": strftime("%Y-%m-%dT%H:%M:%S+00:00", gmtime()),
            "aggregate": {
                "service": "flow-scheduler",
                "name": "schedule-workflow-decision",
                "identifier": "??",
            },
            "type": "schedule-decision-task",
            "data": {
                "workflow_id": workflow_id
            }
        }

        channel.basic_publish(exchange=SCHEDULED_DECISION_EXCHANGE,
                              routing_key=SCHEDULED_DECISION_QUEUE,
                              body=json.dumps(message),
                              properties=pika.BasicProperties(delivery_mode=DELIVERY_MODE_PERSISTENT))
        print(f'[x] Schedule decision sent: {message}')

        # TODO send event message saying scheduled a decision task


def start_workflow(workflow_id: str) -> None:
    """Set workflow status to 'In Progress'.

    :param workflow_id:
    :return:
    """
    data = {'status': 'In Progress'}
    requests.patch(f'{WORKFLOW_API_URL}{workflow_id}/', data=data)


def create_workflow(name: str, input_data: Dict[str, Any]) -> None:
    """Create workflow instance via workflow API.

    :param name: str
    :param input_data: Dict
    :return:
    """
    # get workflow definition
    loader = FlowLoader()
    workflow_def = loader.get_workflow(name)

    if workflow_def:
        workflow_payload = {
            "name": workflow_def.get('name'),
            "input_data": json.dumps(input_data),
            "config": json.dumps(workflow_def.get('config'))
        }

        # create workflow
        response = requests.post(WORKFLOW_API_URL, data=workflow_payload)
        workflow_id = response.json().get('instance_id')

        if workflow_id:
            # create activities
            for activity in workflow_def.get('activities', []):
                activity_payload = copy.deepcopy(activity)
                activity_payload['config'] = json.dumps(activity_payload['config'])
                activity_payload['workflow'] = workflow_id

                requests.post(ACTIVITY_API_URL, data=activity_payload)

        update_workflow_status(workflow_id=workflow_id, status='In Progress')

        schedule_decision(workflow_id=workflow_id)

        # TODO if successful then send workflow created event

    else:
        # TODO if unsuccessful then send workflow creation failed event
        print(f'No Workflow definition found for {name}')


def activity_result_message_handler(channel: pika.channel.Channel,
                                    method: pika.spec.Basic.Deliver,
                                    properties: pika.spec.BasicProperties, body: str) -> None:
    print(f'[x] Activity results received: {body}')

    try:
        data = json.loads(body)
        result = data['data']

        activity_state = get_activity_state(result['activity_id'])

        update_activity_status(activity_id=result['activity_id'], status=result['result'])

        schedule_decision(workflow_id=activity_state['workflow'])
    except json.decoder.JSONDecodeError:
        pass

    channel.basic_ack(method.delivery_tag)


def decision_result_message_handler(channel: pika.channel.Channel,
                                    method: pika.spec.Basic.Deliver,
                                    properties: pika.spec.BasicProperties, body: str) -> None:
    print(f'[x] Decision results received: {body}')

    try:
        data = json.loads(body)
        decision = data['data']

        if decision['decision'] == 'start-workflow':
            create_workflow(data['name'], data['input_data'])

        elif decision['decision'] == 'schedule-activities':
            for activity in decision['activities']:
                schedule_activity(activity['instance_id'])

        elif decision['decision'] == 'workflow-finished':
            update_workflow_status(workflow_id=decision['workflow_id'], status=FINISHED)

        elif decision['decision'] == 'workflow-failure':
            update_workflow_status(workflow_id=decision['workflow_id'], status=FINISHED)

        elif decision['decision'] == 'do-nothing':
            pass

    except json.decoder.JSONDecodeError:
        pass

    channel.basic_ack(method.delivery_tag)


def workflow_starter_message_handler(channel: pika.channel.Channel,
                                     method: pika.spec.Basic.Deliver,
                                     properties: pika.spec.BasicProperties, body: str) -> None:
    print(f'[x] Workflow starter received: {body}')

    try:
        data = json.loads(body)
        create_workflow(data['name'], data['input_data'])
    except json.decoder.JSONDecodeError:
        pass

    channel.basic_ack(method.delivery_tag)


@setup_exchanges_and_queues
def main():
    with get_channel() as channel:
        print('Scheduler running...')
        print(' [*] Waiting for Messages. To exit press CTRL+C')

        channel.basic_consume(activity_result_message_handler, queue=ACTIVITY_RESULT_QUEUE, no_ack=False)
        channel.basic_consume(decision_result_message_handler, queue=DECISION_RESULT_QUEUE, no_ack=False)
        channel.basic_consume(workflow_starter_message_handler, queue=WORKFLOW_STARTER_QUEUE, no_ack=False)

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()


if __name__ == '__main__':
    pass











