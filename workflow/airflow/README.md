# Airflow Example Usage

Dependencies
------------

* Python >=3.6
* [pipenv](https://docs.pipenv.org/)

Installation
------------
This will setup your virtual environment and install the required dependencies:

`pipenv --python 3.6.3 install`

Set the `AIRFLOW_HOME` environment variable in the `.env` file to your absolute path:

e.g. `AIRFLOW_HOME=~/...../walking-skeleton/workflow/airflow`

Activate your virtual environment:

`pipenv shell`

Initialize the database:

`airflow initdb`

This step will setup an `airflow.db` `sqlite` file, your `airflow.cfg` file and your `unittests.cfg` file.
 
Usage
-----

Activate your virtual environment:

`pipenv shell`

Start a scheduler instance in it's own process:

`airflow scheduler`

Start a webserver instance in it's own process: (not required but provides a nice UI)

`airflow webserver -p 8080`

Browsing to [http://localhost:8080/](http://localhost:8080/) will now take you to the [admin console](https://airflow.apache.org/ui.html)foo_dag.py.


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
