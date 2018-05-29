# Downstream delivery sample

This service is an example of listening to `article` events to deliver new articles to downstream services such as [Crossref](https://www.crossref.org/).

## Features

Being a sample, this service does not interact with the real crossref service.

Implemented:

- emit a `downstream.crossref.started` event upon successful receival of the `article` event
- add `runId` correlation data to emitted `downstream.crossref.*` events to link them to the article

Planned:

- retrieve an `article` from the Libero API for further processing
- add delayed `downstream.crossref.completed` events representing an asynchronous process coming to an end
- add random and realistic `downstream.crossref.failed` events

## Configuration

Provide access to RabbitMQ using the environment variable:

- `RABBITMQ_URL` (example: `amqp://username:password@localhost:5672`)
