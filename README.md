# Libero walking skeleton

This repo contains experiments that will comprise a walking skeleton of the Libero publishing system.

It contains:

## Applications

These can be run using `docker-compose up`.

- `api-dummy`: A dummy implementation of the API, containing sample XML content in multiple languages from eLife, Hindawi, SciELO, International Journal of Microsimulation and Wikipedia, and corresponding RELAX NG schemas for each source. Can be viewed at http://localhost:8081/articles.
  - XML content is stored in `data`
  - Schemas are stored in `public/schemas`
- `journal`: A basic implementation of the public-facing site, that lists and displays articles from an API implementation in multiple languages. Can be viewed at http://localhost:8080/.

## Experiments

- `events`: Experiments into PHP and Python implementations of a RabbitMQ-based event bus.
- `workflow`: An experiment into using Airflow as a workflow.
