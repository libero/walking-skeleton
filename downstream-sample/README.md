# Downstream delivery sample

This service is an example of listening to `article` events to deliver new articles to downstream services such as [Crossref](https://www.crossref.org/).

## Features

Being a sample, this service does not interact with the real crossref service.

Implemented:

- emit an `article-delivery` event upon successful receival of the `article` event

Planned:

- retrieve an `article` from the Libero API for further processing
- add correlation data to emitted `article-delivery` events to link them to the article
- add delayed `article-delivery` events representing an asynchronous process coming to an end
- add random and realistic `article-delivery` failure events

## Configuration

Provide access to RabbitMQ using the environment variables:

- `RABBITMQ_HOST` (default: `localhost`)
- `RABBITMQ_PORT` (default: `5672`)
- `RABBITMQ_USER` (default: `guest`)
- `RABBITMQ_PASSWORD` (default: `guest`)
