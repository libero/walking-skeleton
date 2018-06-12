import json
from typing import Any, Dict

from airflow.plugins_manager import AirflowPlugin
from airflow.operators.python_operator import PythonOperator


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
        pass
        # with get_channel() as channel:
        #     message = get_base_message()
        #     message['aggregate']['service'] = 'airflow'
        #     message['aggregate']['name'] = f'{self.python_callable.__name__}'
        #     message['type'] = 'event-emitting-python-operator'
        #     message['data'] = data
        #
        #     channel.basic_publish(exchange=TASK_EVENT_EXCHANGE,
        #                           routing_key=message['type'],
        #                           body=json.dumps(message))


class LiberoPlugin(AirflowPlugin):
    # The name of your plugin (str)
    name = "libero_plugin"
    # A list of class(es) derived from BaseOperator
    operators = [EventEmittingPythonOperator]
    # A list of class(es) derived from BaseHook
    hooks = []
    # A list of class(es) derived from BaseExecutor
    executors = []
    # A list of references to inject into the macros namespace
    macros = []
    # A list of objects created from a class derived
    # from flask_admin.BaseView
    admin_views = []
    # A list of Blueprint object created from flask.Blueprint
    flask_blueprints = []
    # A list of menu links (flask_admin.base.MenuLink)
    menu_links = []
