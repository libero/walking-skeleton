from datetime import timedelta
import pprint
import time

import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
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


dag = DAG(dag_id='foo_python_operator', default_args=default_args, schedule_interval=None)


# # t1, t2 and t3 are examples of tasks created by instantiating operators
# t1 = BashOperator(
#     task_id='print_date',
#     bash_command='date',
#     dag=dag)
#
# t1.doc_md = """\
# #### Task Documentation
# You can document your task using the attributes `doc_md` (markdown),
# `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
# rendered in the UI's Task Instance Details page.
# ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
# """
#
# dag.doc_md = __doc__


def my_sleeping_function(random_base):
    """This is a function that will run within the DAG execution"""
    time.sleep(random_base)


def print_context(ds, **kwargs):
    pprint.pprint(kwargs)
    # print(ds)
    # print(kwargs['params']['article_id'])
    article_id = kwargs['dag_run'].conf.get('article_id')
    return 'Ran foo task with article_id {}'.format(article_id)


run_this = PythonOperator(task_id='print_the_context',
                          provide_context=True,
                          python_callable=print_context,
                          # params={'article_id': article_id},
                          dag=dag)

# # Generate 10 sleeping tasks, sleeping from 0 to 9 seconds respectively
# for i in range(10):
#     task = PythonOperator(
#         task_id='sleep_for_' + str(i),
#         python_callable=my_sleeping_function,
#         op_kwargs={'random_base': float(i) / 10},
#         dag=dag)
#
#     task.set_upstream(run_this)
