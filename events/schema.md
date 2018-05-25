# Events schema

Events published to the bus have a standard schema that allows SDKs and services to consume them homogeneously.

The schema is based on JSON (and can be modelled with JSON Schema if necessary).

## Examples

For clarity, the example data is included with JS syntax (e.g. allowing comments) rather than JSON syntax.

### Example: article ingestion from the article store

```
{
    "eventId": "448278c4-22d6-11e8-b467-0ed5f89f718b",
    "runId": "0509e8c3-4dee-4a3a-800a-3fa9fb43f2e8",
    "happenedAt": "2018-03-08T12:00:00+00:00",
    "type": "deposit-assets-started",
    "message": "Article 10627 figure archival completed",
}
```

### Example: downstream search service indexing an article

```
{
    "runId": "0509e8c3-4dee-4a3a-800a-3fa9fb43f2e8",
    "eventId": "448278c4-22d6-11e8-b467-0ed5f89f718b",
    "happenedAt": "2018-03-08T12:00:00+00:00",
    "type": "search-indexing-started",
    "message": "Article keywords parsing started",
}
```

### Example: downstream deposit service pushing an article to Crossref

```
{
    "runId": "0509e8c3-4dee-4a3a-800a-3fa9fb43f2e8",
    "eventId": "448278c4-22d6-11e8-b467-0ed5f89f718b",
    "happenedAt": "2018-03-08T12:00:00+00:00",
    "type": "downstream-crossref-started",
    "message": "Article being pushed to crossref.org",
}
```

## Fields

### `runId`

Ties together a single ingestion of an article or other content type across multiple systems. It's an implementation of a correlation id for events across multiple services.

### `eventId`

Unique for all events. It is a UUID version 1 generated with time and a node identifier.

### `happenedAt` 

Identifies when the event has happened (then it can get published, consumed, etc). It follows the `yyyy-mm-ddTHH:MM:SS+00:00` ISO 8601 format, and is expressed in UTC.

### `type`

Describes what the event is about so that they can be grouped or recognized. It follows the `[a-z\-\.]+` regular expression, with `.` separating hierarchical levels and `-` separating words in a single level (if there are multiple words).

A consistent pattern for types describing a transaction is

- `...-started` 
- `...-completed` 
- `...-failed` 

### `message`

A string containing useful information to log about the event, or diagnostic information to help make sense of errors.

For the time being, contains also identifiers that can map a run to a particular content item, such as an article id and version.
