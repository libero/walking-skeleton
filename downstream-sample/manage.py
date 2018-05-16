from downstream_sample import settings, worker, crossref
from downstream_sample.settings import (
    DOWNSTREAM_QUEUE_NAME,
    get_channel,
    get_queue
)


# only one command supported
if __name__ == '__main__':
    print('Starting worker...')
    crossref = crossref.FakeCrossref()
    worker = worker.Worker(crossref.push)
    # move into worker.py
    with get_channel() as channel:
        get_queue()
        channel.basic_consume(worker.message_handler, queue=DOWNSTREAM_QUEUE_NAME, no_ack=False)
#
        try:
            print('Consuming...')
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
