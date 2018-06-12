from datetime import datetime
import json
import pika
import uuid

from downstream_sample.settings import get_channel, ensure_exchange, DELIVERY_MODE_PERSISTENT

class Events():
    def __init__(self, exchange_name):
        self._exchange_name = exchange_name

    def publish(self, event):
        ensure_exchange(self._exchange_name)
        with get_channel() as channel:
            event['eventId'] = str(uuid.uuid1())
            event['happenedAt'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")
            print("Publishing: %s" % event)
            channel.basic_publish(exchange=self._exchange_name,
                                  routing_key=event['type'],
                                  body=json.dumps(event),
                                  properties=pika.BasicProperties(delivery_mode=DELIVERY_MODE_PERSISTENT))
