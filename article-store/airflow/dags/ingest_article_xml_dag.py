from datetime import timedelta
import os
import json
import sys

import airflow
from airflow import DAG
from bs4 import BeautifulSoup
import requests

# HACK for DAG example usage without creating a load of package structures
# would break this out, outside of example usage
sys.path.append('..')
from airflow.operators import EventEmittingPythonOperator

DIR_PATH = 'data'
ARTICLES_EXCHANGE = 'articles'


def download_article_xml(*args, **kwargs):
    """Download some article xml and store in a public location

    :return: str
    """

    input_data = kwargs['dag_run'].conf.get('input_data')

    if input_data:
        data_dir = input_data.get('data_dir')
        file_urls = input_data.get('urls')

        if not os.path.isdir(data_dir):
            os.mkdir(data_dir)

        if file_urls:
            for url in file_urls:
                response = requests.get(url=url)

                file_name = url.split('/')[-1]

                with open(os.path.join(data_dir, file_name), 'w') as xml_file:
                    xml_file.write(response.text)


def extract_asset_uris(*args, **kwargs):
    """Download some article xml and extract asset URIs from XML.

    :return: str
    """

    input_data = kwargs['dag_run'].conf.get('input_data')

    if input_data:
        file_urls = input_data.get('urls')

        uris = []

        if file_urls:
            for url in file_urls:
                response = requests.get(url=url)
                xml = BeautifulSoup(response.text, 'lxml-xml')
                uris += [var.contents[0] for var in xml.find_all('source')
                         if var.attrs['media-type'] == 'image/tiff']

        print(uris)

        kwargs['ti'].xcom_push('uris', json.dumps({'uris': uris}))


def download_assets(*args, **kwargs):
    """Download some static assets.

    :return: str
    """

    input_data = kwargs['dag_run'].conf.get('input_data')
    uris = kwargs['ti'].xcom_pull(task_ids=None, key='uris')

    if input_data and uris:
        data_dir = input_data.get('data_dir')

        uris = json.loads(uris.replace("'", '"'))

        for uri in uris['uris']:
            response = requests.get(url=uri)

            file_name = uri.split('/')[-1]

            with open(os.path.join(data_dir, file_name), 'wb') as asset_file:
                asset_file.write(response.content)


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


dag = DAG('ingest_article_xml', default_args=default_args, schedule_interval=None)


_download_article_xml = EventEmittingPythonOperator(exchange=ARTICLES_EXCHANGE,
                                                    task_id='article.version.download_article_xml',
                                                    provide_context=True,
                                                    python_callable=download_article_xml,
                                                    dag=dag)

_extract_asset_uris = EventEmittingPythonOperator(exchange=ARTICLES_EXCHANGE,
                                                  task_id='article.version.extract_asset_uris',
                                                  provide_context=True,
                                                  python_callable=extract_asset_uris,
                                                  dag=dag)

_download_assets = EventEmittingPythonOperator(exchange=ARTICLES_EXCHANGE,
                                               task_id='article.version.download_assets',
                                               provide_context=True,
                                               python_callable=download_assets,
                                               dag=dag)


_extract_asset_uris.set_upstream(_download_article_xml)
_download_assets.set_upstream(_extract_asset_uris)
