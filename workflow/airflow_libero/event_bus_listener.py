import time
from typing import Any, Dict

from pika.exceptions import (
    ChannelClosed,
    ConnectionClosed,
    IncompatibleProtocolError
)

from event_utils import (
    get_channel, message_handler,
    setup_exchanges_and_queues,
    TASK_EVENT_QUEUE,
)


def task_event_handler(data: Dict[str, Any]) -> None:
    print(f'[x] Task event handler received: {data}')


@setup_exchanges_and_queues
def main():
    while True:
        try:
            with get_channel() as channel:
                print('Event Listener running...')
                print('[*] Waiting for Messages. To exit press CTRL+C')

                channel.basic_consume(message_handler(task_event_handler), queue=TASK_EVENT_QUEUE, no_ack=False)
                channel.start_consuming()

        except (ChannelClosed, ConnectionClosed, IncompatibleProtocolError):
            # lost connection
            print('Lost connection... waiting before retry')
            time.sleep(5)
        except KeyboardInterrupt:
            channel.stop_consuming()
            break


if __name__ == '__main__':
    pass
