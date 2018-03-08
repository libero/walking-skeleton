# 1. Provide an internal bus with RabbitMQ

Date: 2018-03-08

## Status

Proposed

## Context

In a service-based architecture, each service needs to update its data by importing it from another service.

A many-to-many mesh of remote calls can quickly create a tight network of dependencies between services.

Portability across cloud providers and hosting services, and easy of deployment, are key concerns for any middleware used by services to communicate.

Standards like the AMQP 0.9.1 specification or abstraction layer libraries do not fully provide reliable delivery from the producer to the consumer.

## Decision

Setup a bus delivering events produced by a service A to any other interested service B, C.

Use RabbitMQ and the following features:

- durable exchanges and queues (AMQP 0.9.1)
- persistent messages (AMQP 0.9.1)
- consumer acknowledgements (AMQP 0.9.1)
- producer confirms (RabbitMQ extension to the protocol)

Use the following libraries for the supported programming languages:

- PHP: [amqplib](https://github.com/php-amqplib/php-amqplib)
- Python: [pika](https://github.com/pika/pika)

## Consequences

RabbitMQ is a dependency for most of the projects to produce or consume events, but it can be provided as a Docker container.

Event bus SDKs wrapping the libraries should be provided to services for each supported programming language, to make integration easy.

High-availability of the events middleware is an operational issue that requires RabbitMQ clustering.
