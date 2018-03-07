from kombu import Consumer, Exchange, Queue, Message

from setup_kombu import (
    ARTICLE_EXCHANGE_NAME,
    DASHBOARD_QUEUE_NAME,
    get_connection
)


def message_handler(body: str, message: Message) -> None:
    print(f'[x] Received: {body}')
    message.ack()


if __name__ == '__main__':
    with get_connection() as connection:

        with connection.channel() as channel:

            queue = Queue(name=DASHBOARD_QUEUE_NAME,
                          exchange=Exchange(name=ARTICLE_EXCHANGE_NAME, type='fanout'))

            consumer = Consumer(channel=channel,
                                queues=queue,
                                callbacks=[message_handler],
                                no_ack=False)

            print(' [*] Waiting for Messages. To exit press CTRL+C')
            consumer.consume()

            while True:
                try:
                    connection.drain_events()
                except KeyboardInterrupt:
                    break
