import time

import pika

from setup_pika import (
    ARTICLE_EXCHANGE_NAME,
    DASHBOARD_QUEUE_NAME,
    PERSISTENT,
    get_channel
)


if __name__ == '__main__':

    with get_channel() as channel:
        # create an exchange of type `fanout`, will skip if already exists
        channel.exchange_declare(exchange=ARTICLE_EXCHANGE_NAME,
                                 exchange_type='fanout',
                                 durable=True)

        # create queue, will skip if exists
        channel.queue_declare(queue=DASHBOARD_QUEUE_NAME, durable=True)

        # bind queue to exchange, will skip if already bound
        channel.queue_bind(exchange=ARTICLE_EXCHANGE_NAME, queue=DASHBOARD_QUEUE_NAME)
        channel.confirm_delivery()

        while True:
            msg = f'Test message: {time.time()}'
            print(f'Publishing: {msg}')

            # send a message
            channel.basic_publish(exchange=ARTICLE_EXCHANGE_NAME,
                                  routing_key=DASHBOARD_QUEUE_NAME,
                                  body=msg,
                                  properties=pika.BasicProperties(delivery_mode=PERSISTENT))
            time.sleep(1)
