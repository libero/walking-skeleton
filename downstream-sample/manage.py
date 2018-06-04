from downstream_sample import settings, worker, events, crossref
from downstream_sample.settings import (
    DOWNSTREAM_QUEUE_NAME,
    DOWNSTREAM_EXCHANGE_NAME,
    ensure_exchange
)


# only one command supported
if __name__ == '__main__':
    print('Starting worker...')
    ensure_exchange(DOWNSTREAM_EXCHANGE_NAME)
    crossref = crossref.FakeCrossref(events.Events(DOWNSTREAM_EXCHANGE_NAME))
    worker = worker.Worker(DOWNSTREAM_QUEUE_NAME, crossref.push)
    worker.start()
