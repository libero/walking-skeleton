class FakeCrossref:
    # TODO: add type hints
    def __init__(self, events):
        self._events = events

    def push(self, article):
        self._events.publish({
            "aggregate": {
                "service": "downstream-sample",
                "name": "article-delivery",
                # TODO: make article id dynamic
                "identifier": "10627-crossref-1",
            },
            "type": "downstream-crossref-started",
            "data": {
                "crossref_output": "We are happy to receive this paper and have put it into a queue",
            },
            # TODO: insert article id for correlation
        })
