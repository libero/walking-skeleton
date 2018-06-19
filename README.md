# Libero walking skeleton

This repo contains experiments that will comprise a walking skeleton of the Libero publishing system.

Execute `./example.sh` in your terminal to follow a demo. This shows:

1. Creating an article
2. Adding a new version
3. Updating a version
4. Deleting an article

## Applications

These can be run using `docker-compose up -V`.

### `api-doc`

Can be viewed through the `api-gateway` at http://localhost:8085/.

Contains an example RAML definition of a Libero API: shows running two article stores (with different content schemas), including adding custom extensions to article store endpoints.

### `api-gateway`

Contains a simple Nginx API gateway.

* http://localhost:8085/ proxies `api-doc`
* http://localhost:8085/articles proxies `article-store`

### `article-store`

Can be viewed through the `api-gateway` at http://localhost:8085/articles.

A basic implementation of the article store in Django, that stores and serves articles through the API. It uses the `article-store-airflow` to run a workflow when creating/updating an article version.

### `article-store-airflow`

Can be viewed at http://localhost:8086/.

Contains an Airflow for the article store, and a DAG that is run when an article version is created/updated. This DAG copies images to `static-assets-store` and rewrites the content to be served by it (representing the source images being stored somewhere private, and need to be made public).

### `dashboard`

Can be viewed at http://localhost:8082/.

A basic implementation of the dashboard in Symfony, that lists all events passed on the event bus (grouped by run ID) in multiple languages. 

### `event-bus`

This is http://localhost:8083/ (using `guest`/`guest`).

It is a standard RabbitMQ (ie no code here), where require exchanges and queue are run.

### `journal`

Can be viewed at http://localhost:8080/.

A basic implementation of the public-facing site in Symfony, that lists and displays articles from an API implementation in multiple languages. 

### `schemas`

Can be viewed at http://localhost:8087/.

Contains the base Libero API (in RAML) and content (in RELAX NG) schemas.

This represents files that are immutable and publicly hosted by Libero.

### `static-assets-store`

Can be viewed at http://localhost:8089/.

This represents a publicly-available asset store (eg an S3 bucket). `article-store-airflow` places images here.

## Extra

### `airflow`

This represents a base install of Airflow with basic Libero integration. Applications can then extend this by adding in DAGs (eg `article-store-airflow`).

### `api-dummy`

A dummy implementation of the API, containing sample XML content in multiple languages from eLife, Hindawi, SciELO, International Journal of Microsimulation and Wikipedia, and corresponding RELAX NG schemas for each source. Can be viewed at http://localhost:8081/articles.
  - XML content is stored in `data`
  - Schemas are stored in `public/schemas`
