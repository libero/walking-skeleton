# Events schema

Events published to the bus have a standard schema that allows SDKs and services to consume them homogeneously.

The schema is based on JSON (and can be modelled with JSON Schema if necessary).

```
{
    "eventId": "448278c4-22d6-11e8-b467-0ed5f89f718b",
    "date": "2018-03-08T12:00:00+00:00",
    "aggregate": {
        "service": "bot",
        "name": "article-run",
        "identifier": "6551f09a-bd23-4f12-a039-f8fa78ef776a",
    },
    "type": "deposit-assets-started",
    "data": {
        ... 
    },
    #"correlationId": {
    #    "service": "journal",
    #    "name": "page",
    #    "identifier": "e4c1829b8249fee0e201bec4589b2aa1b394960f",
    #},
}
```

- `eventId` is unique for all events. It is a UUID version 1 generated with time and a node identifier.
- `date` identifies when the event has happened (then it can get published, consumed, etc).
- `aggregate` identifies the unit of consistency that has produced the event: article run in the bot, article version in the articles, store podcast episode in journal-cms, an article's set of metrics in metrics, a single profile in profiles. All three information are required to uniquely identify it: `service`, `name`, `identifier`.
- `type` describes what the event is about so that they can be grouped or recognized.
- `data` is opaque here, and can contain anything as long as it follows naming conventions. Events with the same `type` should usually follow the same schema.
- `correlationId` can be used to track events across services, grouping them by the kind of session that originated them. Could be an article run during ingestion, or a journal page creating a profile. It is optional at this time.
