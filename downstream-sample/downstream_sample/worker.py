import json
import pika

from downstream_sample.settings import (
    get_channel,
    ensure_queue()
)

class Worker:
    def __init__(self, queue_name, work):
        """work will be passed a dictionary containing the message
        
        Possible results:
            - return None
            - raise an exception"""
        self._work = work
        self._queue_name = queue_name

    def start(self):
        with get_channel() as channel:
            ensure_queue()
            channel.basic_consume(self._message_handler, queue=self._queue_name, no_ack=False)

            try:
                print('Consuming...')
                channel.start_consuming()
            except KeyboardInterrupt:
                channel.stop_consuming()

    def _message_handler(self, channel: pika.channel.Channel, method: pika.spec.Basic.Deliver,
                        properties: pika.spec.BasicProperties, body: str) -> None:
        message = json.loads(body)
        print("Receiving: %s" % message)
        self._work(message)
        channel.basic_ack(method.delivery_tag)
