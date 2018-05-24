# Events schema

Events published to the bus have a standard schema that allows SDKs and services to consume them homogeneously.

The schema is based on JSON (and can be modelled with JSON Schema if necessary).

## Examples

For clarity, the example data is included with JS syntax (e.g. allowing comments) rather than JSON syntax.

### Example: article ingestion from the article store

```
{
    "eventId": "448278c4-22d6-11e8-b467-0ed5f89f718b",
    "happenedAt": "2018-03-08T12:00:00+00:00",
    "entity": {
        "service": "article-store",
        "name": "article-run",
        "identifier": "6551f09a-bd23-4f12-a039-f8fa78ef776a",
    },
    "type": "deposit-assets-started",
    "data": {
        ... 
    },
    "correlationIds": [
        {
            "service": "article-store",
            "name": "article",
            "identifier": "10627",
        },
        {
            "service": "article-store",
            "name": "article-version",
            "identifier": "1",
        },
        {
            "service": "article-store",
            "name": "article-run",
            "identifier": "6551f09a-bd23-4f12-a039-f8fa78ef776a",
        },
    ],
}
```

### Example: downstream search service indexing an article

```
{
    "eventId": "448278c4-22d6-11e8-b467-0ed5f89f718b",
    "happenedAt": "2018-03-08T12:00:00+00:00",
    "entity": {
        "service": "search",
        "name": "indexing",
        "identifier": "18b21fea-5a87-11e8-9c2d-fa7ae01bbebc",
    },
    "type": "search-indexing-started",
    "data": {
        ... 
    },
    "correlationIds": [
        {
            "service": "article-store",
            "name": "article",
            "identifier": "10627",
        },
        {
            "service": "article-store",
            "name": "article-version",
            "identifier": "1",
        },
        {
            "service": "article-store",
            "name": "article-run",
            "identifier": "6551f09a-bd23-4f12-a039-f8fa78ef776a",
        },
        {
            "service": "search",
            "name": "indexing",
            "identifier": "18b21fea-5a87-11e8-9c2d-fa7ae01bbebc",
        },
    ],
}
```

### Example: downstream deposit service pushing an article to Crossref

```
{
    "eventId": "448278c4-22d6-11e8-b467-0ed5f89f718b",
    "happenedAt": "2018-03-08T12:00:00+00:00",
    "entity": {
        "service": "downstream-sample",
        "name": "deposit",
        "identifier": "2018-03-08/1", # daily attempts
    },
    "type": "downstream-crossref-started",
    "data": {
        ... 
    },
    "correlationIds": [
        {
            "service": "article-store",
            "name": "article",
            "identifier": "10627",
        },
        {
            "service": "article-store",
            "name": "article-version",
            "identifier": "1",
        },
        {
            "service": "article-store",
            "name": "article-run",
            "identifier": "6551f09a-bd23-4f12-a039-f8fa78ef776a",
        },
        {
            "service": "downstream-sample",
            "name": "deposit",
            "identifier": "2018-03-08/1",
        },
    ],
}
```

## Fields

### `eventId`

Unique for all events. It is a UUID version 1 generated with time and a node identifier.

### `happenedAt` 

Identifies when the event has happened (then it can get published, consumed, etc). It follows the `yyyy-mm-ddTHH:MM:SS+00:00` ISO 8601 format, and is expressed in UTC.

### `entity`

Identifies the unit of consistency that has produced the event: article run in the bot, article version in the articles store, podcast episode in journal-cms, an article's set of metrics in metrics, a single profile in profiles.

All three information are required to uniquely identify it:

- `service`: `[a-z\-]+`
- `name`: `[a-z\-]+`
- `identifier`: `.+` (possibly URL-friendly)

This identifier may or may not correspond to a REST resource accessible through the API of the originating service.

### `type`

Describes what the event is about so that they can be grouped or recognized. It follows the `[a-z\-\.]+` regular expression, with `.` separating hierarchical levels and `-` separating words in a single level (if there are multiple words).

### `data` (optional)

Is opaque here, and can contain anything as long as it follows naming conventions. Events with the same `type` should usually follow the same schema.

### `correlationIds` (optional)

Can be used to track events across services, linking them to:

- the service and transaction that originated them (`article-run` or `search-indexing` or `deposit`)
- a real world entity they refer to (`article` or `article-version`)

Modelled as an array of dictionaries, each following the format of `entity`. Order is not important.

Services may add correlation ids from events they have triggered them to the new events being produced.
