import pika

from setup_pika import (
    DASHBOARD_QUEUE_NAME,
    get_channel
)


def message_handler(channel: pika.channel.Channel, method: pika.spec.Basic.Deliver,
                    properties: pika.spec.BasicProperties, body: str) -> None:
    print(f'[x] Received: {body}')
    channel.basic_ack(method.delivery_tag)


if __name__ == '__main__':
    with get_channel() as channel:
        print(' [*] Waiting for Messages. To exit press CTRL+C')

        channel.basic_consume(message_handler, queue=DASHBOARD_QUEUE_NAME, no_ack=False)

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
