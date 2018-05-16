#from downstream_sample import settings, worker, crossref
#from downstream_sample.settings import (
#    DOWNSTREAM_QUEUE_NAME,
#    get_channel,
#    get_queue
#)

# only one command supported
if __name__ == '__main__':
    print('Get channel')
    print('Should definitely be logger immediately')
    #crossref = crossref.FakeCrossref()
    #worker = worker.Worker(crossref.push)
    import time
    time.sleep(10)
    # move into worker.py
    #with get_channel() as channel:
    #    print('Get queue')
    #    get_queue()
    #    print('Basic consume')
    #    import time
    #    time.sleep(20)
    #    #channel.basic_consume(worker.message_handler, queue=DOWNSTREAM_QUEUE_NAME, no_ack=False)
#
    #    try:
    #        print('Start consuming...')
    #        channel.start_consuming()
    #    except KeyboardInterrupt:
    #        channel.stop_consuming()
