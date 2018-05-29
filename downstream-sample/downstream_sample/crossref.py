class FakeCrossref:
    # TODO: add type hints
    def __init__(self, events):
        self._events = events

    def push(self, article_event):
        # TODO: consider runId mandatory
        runId = article_event.get('runId', None)
        self._events.publish({
            "runId": runId,
            "type": "downstream-crossref-started",
            "message": "We are happy to receive this paper and have put it into a queue",
        })
