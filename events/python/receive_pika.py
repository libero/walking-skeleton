from setup_pika import (
    DASHBOARD_QUEUE_NAME,
    get_channel
)


def message_handler(ch, method, properties, body):
    print(f'[x] Received: {body}')


if __name__ == '__main__':
    with get_channel() as channel:
        print(' [*] Waiting for Messages. To exit press CTRL+C')

        channel.basic_consume(message_handler, queue=DASHBOARD_QUEUE_NAME, no_ack=True)

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
