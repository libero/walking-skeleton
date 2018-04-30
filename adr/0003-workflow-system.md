# 3. Provide a workflow system

Date: 2018-04-27

## Status

Proposed

## Context

In order to maintain portability and avoid dependency on any one service provider we wanted to explore 
[workflow systems](https://en.wikipedia.org/wiki/Workflow_management_system) that did not depend on a specific platform.

Although a Libero deployment should be workflow system agnostic, we want to provide a tried and tested solution as an option.

There are many off the shelf solutions which offer vastly different levels of features and functionality.

Each have their pros and cons, the key factors considered where:

Usage:
- Workflow and activity creation
- Triggering workflows
- Tracking workflow state

Developer experience:
- API complexity overhead
- Minimal required system configuration
- System deployment
- System extension

Integration:
- How other services will communicate with it

Libraries and frameworks that were considered:

- [SpiffWorkflow](http://spiffworkflow.readthedocs.io/en/latest/)
- [Toil](https://toil.readthedocs.io/en/3.15.0/)
- [Luigi](http://luigi.readthedocs.io/en/stable/index.html)
- [Conductor](https://netflix.github.io/conductor/)
- [Airflow](https://airflow.incubator.apache.org/project.html)

We also explored using a custom implementation consisting of the minimal components required to make up a lightweight 
workflow system written in pure Python.

## Decision

Our proposed solution is to use [Airflow](https://airflow.incubator.apache.org/project.html) with a Libero wrapper to fulfil the required workflow integration points and manage the custom workflow and activities.

## Consequences

Only have to manage the code base for the wrapper and custom workflows and activities, not the overall system.

Access to many pre made integrations and plubins with common services managed by the project. 

Must track progress of the [Airflow](https://airflow.incubator.apache.org/project.html) project and keep up to date.

Handle the larger deployment requirements (when compared with other solutions).


