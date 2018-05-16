import json
import pika

from downstream_sample.settings import get_channel, ensure_exchange, DELIVERY_MODE_PERSISTENT

class Events():
    def __init__(self, exchange_name):
        self._exchange_name = exchange_name

    def publish(self, event):
        ensure_exchange(self._exchange_name)
        with get_channel() as channel:
            # TODO add:
            # "eventId": "448278c4-22d6-11e8-b467-0ed5f89f718b",
            # "happenedAt": "2018-03-08T12:00:00+00:00",
            print("Publishing: %s" % event)
            channel.basic_publish(exchange=self._exchange_name,
                                  routing_key='*',
                                  body=json.dumps(event),
                                  properties=pika.BasicProperties(delivery_mode=DELIVERY_MODE_PERSISTENT))
