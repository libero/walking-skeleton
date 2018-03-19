import time

from kombu import (
    Exchange, Queue, Producer
)

from setup_kombu import (
    ARTICLE_EXCHANGE_NAME,
    DASHBOARD_QUEUE_NAME,
    DELIVERY_MODE_PERSISTENT,
    get_connection
)


if __name__ == '__main__':

    with get_connection() as connection:
        # create an exchange of type `fanout`, will skip if already exists
        # is durable by default
        exchange = Exchange(name=ARTICLE_EXCHANGE_NAME, type='fanout')

        # create queue, will skip if exists
        # is durable by default
        # bind queue to exchange
        queue = Queue(name=DASHBOARD_QUEUE_NAME, exchange=exchange)

        with connection.channel() as channel:
            producer = Producer(channel)

            while True:
                msg = f'Test message: {time.time()}'
                print(f'Publishing: {msg}')

                producer.publish(
                    body=msg,
                    delivery_mode=DELIVERY_MODE_PERSISTENT,
                    retry=True,
                    retry_policy={
                        'interval_start': 0,  # First retry immediately,
                        'interval_step': 2,   # then increase by 2s for every retry.
                        'interval_max': 30,   # but don't exceed 30s between retries.
                        'max_retries': 30,    # give up after 30 tries.
                    },
                )

                time.sleep(1)
