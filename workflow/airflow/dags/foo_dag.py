"""
A simple DAG that has one operator which just prints its kwargs and return value
to it's log then completes.
"""

from datetime import timedelta
import pprint

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


# these args will get passed on to each operator
# you can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'adhoc':False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'trigger_rule': u'all_success'
}


def print_context(*args, **kwargs):
    pprint.pprint(kwargs)
    article_id = kwargs['dag_run'].conf.get('article_id')
    return 'Ran foo task with article_id {}'.format(article_id)


foo_dag = DAG(dag_id='foo_python_operator', default_args=default_args, schedule_interval=None)

foo_operator = PythonOperator(task_id='print_the_context',
                              provide_context=True,
                              python_callable=print_context,
                              dag=foo_dag)
