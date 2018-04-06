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

[UI](https://airflow.apache.org/ui.html#)

On the DAGS view, you can locate a required DAG type and select `Trigger Dag` via the Links column.
