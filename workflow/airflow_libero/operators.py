import json
from typing import Any, Dict

from airflow.operators.python_operator import PythonOperator

from .event_utils import (
    get_channel,
    get_base_message,
    TASK_EVENT_EXCHANGE,
)


class EventEmittingPythonOperator(PythonOperator):

    def __init__(self, *args, **kwargs):
        super(EventEmittingPythonOperator, self).__init__(*args, **kwargs)

    def execute_callable(self):
        try:
            result = None

            self.publish_event({'message': f'Starting {self.python_callable.__name__}'})
            result = self.python_callable(*self.op_args, **self.op_kwargs)
            self.publish_event({'message': f'Finished {self.python_callable.__name__}'})
        except Exception:
            self.publish_event({'message': f'Failed {self.python_callable.__name__}'})
        finally:
            return result

    def publish_event(self, data: Dict[str, Any]):
        with get_channel() as channel:
            message = get_base_message()
            message['aggregate']['service'] = 'airflow'
            message['aggregate']['name'] = f'{self.python_callable.__name__}'
            message['type'] = 'event-emitting-python-operator'
            message['data'] = data

            channel.basic_publish(exchange=TASK_EVENT_EXCHANGE,
                                  routing_key=message['type'],
                                  body=json.dumps(message))
