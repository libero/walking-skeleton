# 2. Provide workflow integration points

Date: 2018-04-27

## Status

Proposed

## Context

A [workflow system](https://en.wikipedia.org/wiki/Workflow_management_system) to handle the creation, 
processing and orchestration of customized workflows is a required component of Libero's currently proposed design.

Users will each have their individual needs and requirements and therefore may decide to use their 
workflow solution of choice. 

It is therefore important to define clear integration points between a [workflow system](https://en.wikipedia.org/wiki/Workflow_management_system) 
and the rest of the Libero architecture.

## Decision

The workflow solution should provide:

- HTTP endpoint(s) to allow the triggering of workflows
- A queue to allow the triggering of workflows
- Publishing of workflow and activity state event messages via queues
- Adhere to the [Libero event schema](https://github.com/libero/walking-skeleton/blob/master/events/schema.md)

## Consequences

The [workflow system](https://en.wikipedia.org/wiki/Workflow_management_system) in a Libero deployment will 
be independent and swappable.

Existing systems may need a customized plugin or interface to adhere to the required integration points.

Does not force specific language choice, service provider or workflow solution.
