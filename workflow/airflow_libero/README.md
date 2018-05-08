# Airflow Example Usage

Dependencies
------------

* Python >=3.6
* [pipenv](https://docs.pipenv.org/)

Installation
------------

Depends on:
* [docker](https://www.docker.com/)
* [docker-compose](https://github.com/docker/compose)

Celery Executor

`docker-compose -f docker-compose-celery-executor.yml up --build`

Local Executor

`docker-compose -f docker-compose-local-executor.yml up --build`

Run Airflow CLI Commands
--------------------

To run any of Airflow's [CLI commands](https://airflow.apache.org/cli.html) you need to execute them from inside a running
Airflow container. 

For example to execute the [`airflow version`](https://airflow.apache.org/cli.html#version) command:

`docker-compose -f docker-compose-celery-executor.yml exec scheduler airflow version`


Usage
-----

Start the event listener:

`pipenv run python run_event_bus_listener.py`

Browsing to [http://localhost:8080/](http://localhost:8080/) will now take you to the [admin console](https://airflow.apache.org/ui.html).


Trigger a DAG
-----------

There are multiple ways to trigger a DAG manually.

[CLI](https://airflow.apache.org/cli.html#trigger_dag)

`airflow trigger_dag foo_python_operator`

To trigger a DAG with addtional data you can pass it a JSON string:

`airflow trigger_dag foo_python_operator --conf '{"input_data": {"foo": "bar"}}'`

[UI](https://airflow.apache.org/ui.html#)

On the DAGS view, you can locate a required DAG type and select `Trigger Dag` via the Links column.

[API (experimental)](https://airflow.apache.org/api.html)

Send a POST request to `/api/experimental/dags/<DAG_ID>/dag_runs` .

This creates a `dag_run` for a given dag id (POST).

Scheduled string format: https://airflow.apache.org/scheduler.html#dag-runs

The below example would schedule the dag `example_bash_operator` to be scheduled immediately:

POST: `http://localhost:8080/api/experimental/dags/example_bash_operator/dag_runs`

PAYLOAD:
```json
{
	"schedule": "None"
}
```

For additional REST functionality there is also a 3rd party [REST API Plugin](https://github.com/teamclairvoyant/airflow-rest-api-plugin) .

To trigger a dag with some initial value(s) you can use the following format:

note: "Support for passing such arguments will be dropped in Airflow 2.0."

Trigger Ingest Article XML DAG
------------------------------

- Follow `Usage` section steps to setup your environment.

To DAG execute via the CLI:

`pipenv run airflow trigger_dag ingest_article_xml --conf '{"input_data": {"data_dir": "article-data-public", "urls": ["https://s3.amazonaws.com/libero-workflow-test/00666/00666-body.xml", "https://s3.amazonaws.com/libero-workflow-test/00666/00666-front.xml"]}}'
`

or to DAG execute via http:

POST: `http://localhost:8080/api/experimental/dags/ingest_article_xml/dag_runs`
PAYLOAD:
```json
{
	"schedule": "None",
	"conf": "{\"input_data\": {\"data_dir\": \"article-data-public\", \"urls\": [\"https://s3.amazonaws.com/libero-workflow-test/00666/00666-body.xml\", \"https://s3.amazonaws.com/libero-workflow-test/00666/00666-front.xml\"]}}"
}
```


- You should be able to see the DAG and task state(s) via the web UI on [http://localhost:8080/](http://localhost:8080/).
- You should see emitted events for each task in your event listener console that you started.