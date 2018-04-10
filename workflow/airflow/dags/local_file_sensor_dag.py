import os

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.sensors import BaseSensorOperator
from datetime import timedelta


class FileWatcherOperator(BaseSensorOperator):
    """
    Triggers a file system check.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize a FileWatcherOperator which should wait for a file to be present in a target directory.

        :param args:
        :param kwargs:
        """
        self.directory_path = kwargs.get('directory_path')
        super(FileWatcherOperator, self).__init__(*args, **kwargs)

    def poke(self, context, *args, **kwargs):
        """
        See if a file is present in a given directory.

        :param context: Context dictionary forwarded from the DAG;
        expects to contain context.dag and context.task
        :type context: dict
        :param args: not expected
        :param kwargs: not expected
        :return: whether the poke method has succeeded or not, 0 or 1
        :rtype: int
        """
        path = os.path.join(os.getcwd(), self.directory_path)
        dir_listing = os.listdir(path)

        if len(dir_listing) > 0:
            context['ti'].xcom_push(key='file_path', value=os.path.join(path, dir_listing[0]))
            return True

        return False


DIR_PATH = 'data'


def parse_file(*args, **kwargs):
    """Simply parse the first file in a directory and return it's contents.

    :param args:
    :param kwargs:
    :return:
    """
    # get file path value from passed in context
    file_path = kwargs['ti'].xcom_pull(task_ids='file_watcher', key='file_path')

    with open(file_path) as f:
        return f.read()


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}

# create your DAG
dag = DAG('local_file_sensor', default_args=default_args, schedule_interval=None)

# the first task is going to be a file watcher
watcher = FileWatcherOperator(task_id='file_watcher',
                              poke_interval=2,
                              timeout=10,
                              provide_context=True,
                              directory_path=DIR_PATH,
                              dag=dag)

# the second task is going to wait for the watcher to return true before starting
file_parser = PythonOperator(task_id='file_parser',
                             provide_context=True,
                             python_callable=parse_file,
                             dag=dag)


# set the file_parser to come after the watcher
file_parser.set_upstream(watcher)
