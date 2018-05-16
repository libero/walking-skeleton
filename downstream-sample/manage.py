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
    worker = worker.Worker(DOWNSTREAM_QUEUE_NAME, crossref.push)
    worker.start()
