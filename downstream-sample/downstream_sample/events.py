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
            # TODO add:
            # "happenedAt": "2018-03-08T12:00:00+00:00",
            event['eventId'] = str(uuid.uuid1())
            print("Publishing: %s" % event)
            channel.basic_publish(exchange=self._exchange_name,
                                  routing_key='*',
                                  body=json.dumps(event),
                                  properties=pika.BasicProperties(delivery_mode=DELIVERY_MODE_PERSISTENT))
