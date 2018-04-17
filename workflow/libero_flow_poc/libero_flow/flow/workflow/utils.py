from typing import Any, Dict
import json

from django.conf import settings
import pika


connection = pika.BlockingConnection(parameters=settings.BROKER_PARAMS)


def start_workflow(name: str, input_data: Dict[str, Any]) -> None:
    """Send message to target broker to instruct a workflow to be started.

    :param name: str
    :param input_data: dict
    :return:
    """
    with connection.channel() as channel:
        # msg = '{"name": {0}, "input_data": {1}}'.format(name, input_data)
        msg = json.dumps({'name': name, 'input_data': input_data})

        channel.basic_publish(exchange=settings.WORKFLOW_STARTER_EXCHANGE,
                              routing_key=settings.WORKFLOW_STARTER_QUEUE,
                              body=msg,
                              properties=pika.BasicProperties(delivery_mode=2))
