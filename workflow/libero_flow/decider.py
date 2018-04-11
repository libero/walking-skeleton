import json
import sys
from time import gmtime, strftime
from typing import Dict
import uuid

import pika
import requests

from event_utils import get_channel, DELIVERY_MODE_PERSISTENT


WORKFLOW_API_URL = 'http://localhost:8000/workflows/api/v1/workflows/'


DECISION_RESULT_EXCHANGE_NAME = 'decision_result'
DECISION_RESULT_QUEUE_NAME = 'decision_results'
SCHEDULED_DECISION_QUEUE_NAME = 'scheduled_decisions'


def get_workflow_state(workflow_id: str) -> Dict:
    """Get workflow state via workflow API.

    :param workflow_id:
    :return:
    """
    response = requests.get(f'{WORKFLOW_API_URL}{workflow_id}/')
    return response.json()


def send_decision_message():
    """create and send decision task message.

    :param workflow_id: str
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
            "data": {
                "decision": ""
            }
        }

        channel.basic_publish(exchange=DECISION_RESULT_EXCHANGE_NAME,
                              routing_key=DECISION_RESULT_QUEUE_NAME,
                              body=json.dumps(message),
                              properties=pika.BasicProperties(delivery_mode=DELIVERY_MODE_PERSISTENT))
        print(f'[x] Schedule decision sent: {message}')


def make_decision(workflow: Dict) -> None:
    """

    :param workflow:
    :return:
    """
    print(f'decider received {workflow}')

    # TODO send decision to DECISION_RESULT_EXCHANGE_NAME
    send_decision_message()


def scheduled_decision_message_handler(channel: pika.channel.Channel,
                                       method: pika.spec.Basic.Deliver,
                                       properties: pika.spec.BasicProperties, body: str) -> None:
    print(f'[x] scheduled decision handler received: {body}')

    try:
        data = json.loads(body)
        workflow_id = data['data']['workflow_id']

        make_decision(workflow=get_workflow_state(workflow_id=workflow_id))
    except json.decoder.JSONDecodeError as err:
        print(err)

    channel.basic_ack(method.delivery_tag)


def main():
    with get_channel() as channel:
        print('Decider running...')
        print(' [*] Waiting for Messages. To exit press CTRL+C')

        channel.basic_consume(scheduled_decision_message_handler, queue=SCHEDULED_DECISION_QUEUE_NAME, no_ack=False)

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()


if __name__ == '__main__':
    sys.exit(main())