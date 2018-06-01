import json

from django.conf import settings
import requests


DAG_NAME = 'make_assets_public'
AIRFLOW_DAGS_URL = f'{settings.AIRFLOW_URL}/api/experimental/dags'
TRIGGER_DAG_URL = f'{AIRFLOW_DAGS_URL}/{DAG_NAME}/dag_runs'


def start_article_dag(run_id: str, article_id: str, article_version_id: str, article_version: str) -> bool:
    """Trigger `DAG_NAME` dag using target airflow instance.

    :param run_id: str
    :param article_id: str
    :param article_version_id: str
    :param article_version: str
    :return: bool
    """

    payload = {
        "schedule": "None",
        "conf": "{\"input_data\": "
                "{ \"run_id\": \"%s\", "
                "\"article_id\": \"%s\","
                "\"article_version\": \"%s\","
                "\"article_version_id\": \"%s\""
                "}}" % (run_id, article_id, article_version, article_version_id)
    }

    response = requests.post(TRIGGER_DAG_URL, data=json.dumps(payload))
    return response.status_code == 200
