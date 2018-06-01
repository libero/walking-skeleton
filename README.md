# Libero walking skeleton

This repo contains experiments that will comprise a walking skeleton of the Libero publishing system.

Execute `./example.sh` in your terminal to follow a demo.

It contains:

## Applications

These can be run using `docker-compose up -V`.

- `api-dummy`: A dummy implementation of the API, containing sample XML content in multiple languages from eLife, Hindawi, SciELO, International Journal of Microsimulation and Wikipedia, and corresponding RELAX NG schemas for each source. Can be viewed at http://localhost:8081/articles.
  - XML content is stored in `data`
  - Schemas are stored in `public/schemas`
- `dashboard`: A basic implementation of the dashboard, that lists all events passed on the event bus in multiple languages. Can be viewed at http://localhost:8082/.
- `journal`: A basic implementation of the public-facing site, that lists and displays articles from an API implementation in multiple languages. Can be viewed at http://localhost:8080/.

## Experiments

- `api-dummy/public/schemas`: An experiment to create an extensible data model using RELAX NG. `libero` contains base schemas (eg an article has an ID and a title), and extensions to represent common requirements (eg abstracts, MathML). `elife`, `hindawi`, `ijm`, `scielo` and `wikipedia` contain example schemas using the base Libero schemas, including Libero extensions, and custom schemas where necessary. Sample content is available in `api-dummy/data`.
- `events`: Experiments into PHP and Python implementations of a RabbitMQ-based event bus.
- `workflow`: An experiment into using Airflow as a workflow.
