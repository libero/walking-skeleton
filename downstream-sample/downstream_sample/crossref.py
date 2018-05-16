class FakeCrossref:
    # TODO: add type hints
    def __init__(self, events):
        self._events = events

    def push(self, article):
        self._events.publish({
            "aggregate": {
                "service": "downstream-sample",
                # TODO: rename into how "getting an article into Crossref" is called, delivery?
                "name": "article-push",
                # TODO: should probably be an internal identifier
                # e.g. article id plus an incremental number or UUID to identify the attempt
                "identifier": "10627-1",
            },
            "type": "downstream-crossref-started",
            "data": {
                "crossref_output": "We are happy to receive this paper and have put it into a queue",
            },
            # TODO: insert article id for correlation
        })
