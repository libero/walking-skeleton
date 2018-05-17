# 4. Own event bus exchanges and queues in services

Date: 2018-05-17

## Status

Proposed

## Context

In a service-based architecture, infrastructure needs to be owned by a service so that it is provisioned and maintained as a first class citizen.

The [event system](0001-events-system.md) based on RabbitMQ requires the setup of `exchanges` and `queues` that `bind` to them.

Practical experience developing eLife lead to no mutual dependencies between services, with e.g. service B strictly being downstream from service A with no events feeding back into service A.

Some services may require a generic binding to many other exchanges in the interest of observability, e.g. a dashboard aggregating events from many different services.

## Decision

Create an `exchange` for each data type, as part of a service publishing events.

Create one `queue` as part of a service consuming events.

Create more than one `queue` in a service if specialized behavior is required, in opposition to a generic type of consumer process.

A service may have optional binds, which will only subscribe its `queue` to another service's `exchange` if enabled or dynamically configured as a plugin.

## Consequences

Service have a [partial order](https://en.wikipedia.org/wiki/Partially_ordered_set) to follow for setup.

The consuming-events-from relationship between services is unidirectional and must be acyclic:

- service B, consuming events from A, cannot publish events for A to consume
- service C, consuming events from B, also cannot publish events for A to consume

The consuming-events-from relationship will often be part of a stronger dependency, like relying on the APIs exposed by service A.
