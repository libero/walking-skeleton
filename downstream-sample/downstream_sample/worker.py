import json
import pika

class Worker:
    def __init__(self, work):
        self._work = work

    def message_handler(self, channel: pika.channel.Channel, method: pika.spec.Basic.Deliver,
                        properties: pika.spec.BasicProperties, body: str) -> None:
        print("message_handler start")
        self._work(json.loads(body))
        channel.basic_ack(method.delivery_tag)
        print("message_handler end")
