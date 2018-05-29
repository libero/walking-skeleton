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

Create an `exchange` for each data type or activity, as part of a service publishing events.

Create one `queue` as part of a service consuming events.

Bind each `queue` to as many exchanges as needed.

If an `exchange` from an upstream service is missing, wait and poll until it's present when bootstrapping a service process that wants to bind to it.

A service may have optional binds, which will only subscribe its `queue` to another service's `exchange` if enabled or dynamically configured as a plugin.

The consuming-events-from relationship between services is unidirectional and must be acyclic.

## Consequences

Service have a [partial order](https://en.wikipedia.org/wiki/Partially_ordered_set) to follow for setup.

The acyclic event consumption implies that:

- service B, consuming events from A, cannot publish events for A to consume
- service C, consuming events from B, also cannot publish events for A to consume

The consuming-events-from relationship will often be part of a stronger dependency, like relying on the APIs exposed by service A.
