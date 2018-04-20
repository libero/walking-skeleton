import copy
import json
import logging
from typing import Any, Dict
import time

import pika
from pika.exceptions import (
    ChannelClosed,
    ConnectionClosed,
    IncompatibleProtocolError
)
import requests

from libero_flow.conf import (
    ACTIVITY_API_URL,
    WORKFLOW_API_URL,
    SCHEDULED_ACTIVITY_EXCHANGE,
    SCHEDULED_DECISION_EXCHANGE,
    ACTIVITY_RESULT_QUEUE,
    DECISION_RESULT_QUEUE,
    SCHEDULED_ACTIVITY_QUEUE,
    SCHEDULED_DECISION_QUEUE,
    WORKFLOW_STARTER_QUEUE,
)
from libero_flow.flow_loader import FlowLoader
from libero_flow.event_utils import (
    get_base_message,
    get_channel,
    message_handler,
    setup_exchanges_and_queues,
    DELIVERY_MODE_PERSISTENT,
)
from libero_flow.session_store import get_session
from libero_flow.state_utils import (
    get_activity_state,
    send_workflow_event,
    update_activity_status,
    update_workflow_status,
    FAILED,
    FINISHED,
    WORKFLOW_ACTIVITY_SCHEDULED,
    WORKFLOW_DECISION_SCHEDULED,
)

logger = logging.getLogger(__name__)
fh = logging.FileHandler(f'{__name__}.log')
logger.addHandler(fh)


def schedule_activity(activity_id: str, workflow_id: str) -> None:
    """create and send schedule activity message.

    :param activity_id: str
    :param workflow_id: str
    :return:
    """
    with get_channel() as channel:
        message = get_base_message()
        message['aggregate']['service'] = 'flow-scheduler'
        message['aggregate']['name'] = 'schedule-workflow-activity'
        message['type'] = 'schedule-activity'
        message['data'] = {'activity_id': activity_id}

        channel.basic_publish(exchange=SCHEDULED_ACTIVITY_EXCHANGE,
                              routing_key=SCHEDULED_ACTIVITY_QUEUE,
                              body=json.dumps(message),
                              properties=pika.BasicProperties(delivery_mode=DELIVERY_MODE_PERSISTENT))
        print(f'[x] Schedule activity sent: {message}')

        update_activity_status(activity_id, status='Scheduled')

        send_workflow_event(workflow_id=workflow_id, event_type=WORKFLOW_ACTIVITY_SCHEDULED)


def schedule_decision(workflow_id: str) -> None:
    """create and send scheduled decision message.

    :param workflow_id: str
    :return:
    """
    with get_channel() as channel:
        message = get_base_message()
        message['aggregate']['service'] = 'flow-scheduler'
        message['aggregate']['name'] = 'schedule-workflow-decision'
        message['type'] = 'schedule-decision-task'
        message['data'] = {'workflow_id': workflow_id}

        channel.basic_publish(exchange=SCHEDULED_DECISION_EXCHANGE,
                              routing_key=SCHEDULED_DECISION_QUEUE,
                              body=json.dumps(message),
                              properties=pika.BasicProperties(delivery_mode=DELIVERY_MODE_PERSISTENT))
        print(f'[x] Schedule decision sent: {message}')

        # TODO send event message saying scheduled a decision
        send_workflow_event(workflow_id=workflow_id, event_type=WORKFLOW_DECISION_SCHEDULED)


def start_workflow(workflow_id: str) -> None:
    """Set workflow status to 'In Progress'.

    :param workflow_id: str
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

        # deposit input_data to session store under workflow namespace
        session = get_session()
        session.set(f'{workflow_id}_input_data', json.dumps(input_data))

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


def activity_result_handler(data: Dict[str, Any]) -> None:
    print(f'[x] Activity results received: {data}')

    result = data['data']

    activity_state = get_activity_state(result['activity_id'])
    update_activity_status(activity_id=result['activity_id'], status=result['result'])
    schedule_decision(workflow_id=activity_state['workflow'])


def decision_result_handler(data: Dict[str, Any]) -> None:
    print(f'[x] Decision results received: {data}')

    decision = data['data']

    if decision['decision'] == 'start-workflow':
        create_workflow(data['name'], data['input_data'])

    elif decision['decision'] == 'schedule-activities':
        for activity in decision['activities']:
            # TODO need to check activity does not currently have an active timeout
            schedule_activity(activity['instance_id'], decision['workflow_id'])

    elif decision['decision'] == 'workflow-finished':
        update_workflow_status(workflow_id=decision['workflow_id'], status=FINISHED)

    elif decision['decision'] == 'workflow-failure':
        update_workflow_status(workflow_id=decision['workflow_id'], status=FAILED)

    elif decision['decision'] == 'do-nothing':
        pass


def workflow_starter(data: Dict[str, Any]) -> None:
    print(f'[x] Workflow starter received: {data}')
    create_workflow(data['name'], data['input_data'])


@setup_exchanges_and_queues
def main():
    while True:
        try:
            with get_channel() as channel:
                print('Scheduler running...')
                print('[*] Waiting for Messages. To exit press CTRL+C')

                channel.basic_consume(message_handler(activity_result_handler), queue=ACTIVITY_RESULT_QUEUE, no_ack=False)
                channel.basic_consume(message_handler(decision_result_handler), queue=DECISION_RESULT_QUEUE, no_ack=False)
                channel.basic_consume(message_handler(workflow_starter), queue=WORKFLOW_STARTER_QUEUE, no_ack=False)

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
