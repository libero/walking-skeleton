import configparser
import os

import pika

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CFG_PATH = os.path.join(BASE_DIR)
CFG_NAME = 'app.cfg'
CONF = configparser.ConfigParser()
CONF.read(os.path.join(CFG_PATH, CFG_NAME))


# API
API_HOST = CONF.get('api', 'host')
API_PORT = CONF.get('api', 'port')

ACTIVITY_API_ENDPOINT = CONF.get('api', 'activity_api_url')
WORKFLOW_API_ENDPOINT = CONF.get('api', 'workflow_api_url')

ACTIVITY_API_URL = f'http://{API_HOST}:{API_PORT}/{ACTIVITY_API_ENDPOINT}/'
WORKFLOW_API_URL = f'http://{API_HOST}:{API_PORT}/{WORKFLOW_API_ENDPOINT}/'


# Message Broker
BROKER_HOST = CONF.get('broker', 'host')
BROKER_PORT = CONF.get('broker', 'port')
BROKER_PASSWORD = CONF.get('broker', 'password')
BROKER_USER = CONF.get('broker', 'user')

BROKER_CREDENTIALS = pika.PlainCredentials(BROKER_USER, BROKER_PASSWORD)
BROKER_PARAMS = pika.ConnectionParameters(host=BROKER_HOST, credentials=BROKER_CREDENTIALS)
