from datetime import timedelta
import os
import json
from typing import Dict
import sys

import airflow
from airflow import DAG
from bs4 import BeautifulSoup
from lxml.etree import (
    Element,
    SubElement,
    fromstring,
    tostring,
)
import requests

# HACK for DAG example usage without creating a load of package structures
# would break this out, outside of example usage
sys.path.append('..')
from airflow.operators import EventEmittingPythonOperator

DIR_PATH = 'data'


def convert_to_xml(article_content: Dict):
    """
    <root>
        <content-list>
            <list-item>
            </list-item>
        </content-list>
    </root>

    :param article_content:
    :return:
    """
    root = Element('root')
    content_list = SubElement(root, 'content-list')

    for content_item in article_content['content_items']:
        list_item = SubElement(content_list, 'list-item')

        name = SubElement(list_item, 'name')
        name.text = content_item['name']

        language = SubElement(list_item, 'language')
        language.text = content_item['language']

        model = SubElement(list_item, 'model')
        model.text = content_item['model']

        content = SubElement(list_item, 'content')
        content.append(fromstring(content_item['content']))

    return tostring(root)


def store_article_data(*args, **kwargs) -> bool:
    """Store article data from input_data provided

    :return: bool
    """

    input_data = kwargs['dag_run'].conf.get('input_data')

    if input_data:
        kwargs['ti'].xcom_push('run_id', input_data.get('run_id'))
        kwargs['ti'].xcom_push('article_id', input_data.get('article_id'))
        kwargs['ti'].xcom_push('article_version', input_data.get('article_version'))
        kwargs['ti'].xcom_push('article_version_id', input_data.get('article_version_id'))
        return True

    return False


def fetch_article_content(*args, **kwargs) -> bool:
    article_version_id = kwargs['ti'].xcom_pull(task_ids=None, key='article_version_id')
    url = f'http://article-store:8000/articles/api/v1/article-versions/{article_version_id}/'

    response = requests.get(url)

    kwargs['ti'].xcom_push('article_content', response.json())
    return True


def deposit_to_article_store(*args, **kwargs) -> bool:
    run_id = kwargs['ti'].xcom_pull(task_ids=None, key='run_id')
    article_id = kwargs['ti'].xcom_pull(task_ids=None, key='article_id')
    article_version = kwargs['ti'].xcom_pull(task_ids=None, key='article_version')
    article_content = kwargs['ti'].xcom_pull(task_ids=None, key='article_content')

    url = f'http://article-store:8000/articles/{article_id}/versions/{article_version}'
    payload = convert_to_xml(article_content)

    headers = {'X-LIBERO-RUN-ID': run_id, 'Content-Type': 'application/xml'}
    response = requests.put(url, data=payload, headers=headers)
    return response.status_code == 201


default_args = {
    'owner': 'libero',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['libero@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}


dag = DAG('make_assets_public', default_args=default_args, schedule_interval=None)


_store_article_data = EventEmittingPythonOperator(task_id='store_article_data',
                                                  provide_context=True,
                                                  python_callable=store_article_data,
                                                  dag=dag)


_fetch_article_content = EventEmittingPythonOperator(task_id='fetch_article_content',
                                                     provide_context=True,
                                                     python_callable=fetch_article_content,
                                                     dag=dag)


_deposit_to_article_store = EventEmittingPythonOperator(task_id='deposit_to_article_store',
                                                        provide_context=True,
                                                        python_callable=deposit_to_article_store,
                                                        dag=dag)


_fetch_article_content.set_upstream(_store_article_data)

_deposit_to_article_store.set_upstream(_fetch_article_content)

# TODO extract uris

# TODO download assets

# TODO update uris
