from datetime import timedelta
import os
import json
from typing import Dict

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

from airflow.operators import EventEmittingPythonOperator

PUBLIC_DATA_DIR = '/usr/local/airflow/public/articles'

SUCCESS = True
FAILURE = False
STATIC_ASSETS_URL = 'http://localhost:8089'
SUPPORTED_MEDIA_TYPES = ['image/tiff', "image/jpeg"]
ASSET_ELEMENTS = ['source', 'variant']


def convert_to_xml(article_content: Dict[str, Dict]) -> str:
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
        content.append(fromstring(content_item['content'].encode('utf-8')))

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
        return SUCCESS

    return FAILURE


def fetch_article_content(*args, **kwargs) -> bool:
    article_version_id = kwargs['ti'].xcom_pull(task_ids=None, key='article_version_id')
    url = f'http://article-store:8000/articles/api/v1/article-versions/{article_version_id}/'

    response = requests.get(url)

    kwargs['ti'].xcom_push('article_content', response.json())
    return SUCCESS, response.json()


def extract_asset_uris(*args, **kwargs) -> bool:
    """Extract asset URIs from XML.

    :return: bool
    """

    article_content = kwargs['ti'].xcom_pull(task_ids=None, key='article_content')

    if article_content:
        asset_uris = []

        for content_item in article_content['content_items']:
            xml = BeautifulSoup(content_item['content'], 'lxml-xml')
            content_uris = []

            for ele in ASSET_ELEMENTS:
                for var in xml.find_all(ele):
                    if var.attrs['media-type'] in SUPPORTED_MEDIA_TYPES:
                        content_uris.append(var.contents[0])

            asset_uris += content_uris

        kwargs['ti'].xcom_push('asset_uris', json.dumps({'asset_uris': asset_uris}))
        return SUCCESS
    return FAILURE


def download_assets(*args, **kwargs) -> bool:
    """Download some static assets.

    :return: bool
    """
    article_id = kwargs['ti'].xcom_pull(task_ids=None, key='article_id')
    asset_uris = kwargs['ti'].xcom_pull(task_ids=None, key='asset_uris')

    data_dir = os.path.join(PUBLIC_DATA_DIR, article_id)
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)

    if asset_uris:
        uris = json.loads(asset_uris.replace("'", '"'))

        for uri in uris['asset_uris']:
            response = requests.get(url=uri)
            file_name = uri.split('/')[-1]

            with open(os.path.join(data_dir, file_name), 'wb') as asset_file:
                asset_file.write(response.content)


def update_asset_uris(*args, **kwargs) -> bool:
    """Update asset URIs in XML article content.

    :return: bool
    """
    article_id = kwargs['ti'].xcom_pull(task_ids=None, key='article_id')
    article_content = kwargs['ti'].xcom_pull(task_ids=None, key='article_content')

    if article_content:
        for content_item in article_content['content_items']:
            xml = BeautifulSoup(content_item['content'], 'lxml-xml')

            for ele in ASSET_ELEMENTS:
                for var in xml.find_all(ele):
                    if var.attrs['media-type'] in SUPPORTED_MEDIA_TYPES:
                        file_name = var.contents[0].split('/')[-1]
                        var.string = f'{STATIC_ASSETS_URL}/articles/{article_id}/{file_name}'

            content_item['content'] = str(xml)

        kwargs['ti'].xcom_push('article_content', article_content)
        return SUCCESS
    return FAILURE


def deposit_to_article_store(*args, **kwargs) -> bool:
    run_id = kwargs['ti'].xcom_pull(task_ids=None, key='run_id')
    article_id = kwargs['ti'].xcom_pull(task_ids=None, key='article_id')
    article_version = kwargs['ti'].xcom_pull(task_ids=None, key='article_version')
    article_content = kwargs['ti'].xcom_pull(task_ids=None, key='article_content')

    url = f'http://article-store:8000/articles/{article_id}/versions/{article_version}'
    payload = convert_to_xml(article_content)

    headers = {
        'X-LIBERO-RUN-ID': run_id,
        'X-LIBERO-AIRFLOW': 'true',
        'Content-Type': 'application/xml'
    }
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

_extract_asset_uris = EventEmittingPythonOperator(task_id='extract_asset_uris',
                                                  provide_context=True,
                                                  python_callable=extract_asset_uris,
                                                  dag=dag)

_download_assets = EventEmittingPythonOperator(task_id='download_assets',
                                               provide_context=True,
                                               python_callable=download_assets,
                                               dag=dag)

_update_asset_uris = EventEmittingPythonOperator(task_id='update_asset_uris',
                                                 provide_context=True,
                                                 python_callable=update_asset_uris,
                                                 dag=dag)

_deposit_to_article_store = EventEmittingPythonOperator(task_id='deposit_to_article_store',
                                                        provide_context=True,
                                                        python_callable=deposit_to_article_store,
                                                        dag=dag)


_fetch_article_content.set_upstream(_store_article_data)
_extract_asset_uris.set_upstream(_fetch_article_content)
_download_assets.set_upstream(_extract_asset_uris)
_update_asset_uris.set_upstream(_download_assets)
_deposit_to_article_store.set_upstream(_update_asset_uris)


# TODO deposit_assets

# TODO update_asset_uris
