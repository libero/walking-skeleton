import json
import pika

from downstream_sample.settings import (
    get_channel,
    get_queue
)

class Worker:
    def __init__(self, queue_name, work):
        self._work = work
        self._queue_name = queue_name

    def start(self):
        with get_channel() as channel:
            get_queue()
            channel.basic_consume(self._message_handler, queue=DOWNSTREAM_QUEUE_NAME, no_ack=False)

            try:
                print('Consuming...')
                channel.start_consuming()
            except KeyboardInterrupt:
                channel.stop_consuming()

    def _message_handler(self, channel: pika.channel.Channel, method: pika.spec.Basic.Deliver,
                        properties: pika.spec.BasicProperties, body: str) -> None:
        print("message_handler start")
        self._work(json.loads(body))
        channel.basic_ack(method.delivery_tag)
        print("message_handler end")
