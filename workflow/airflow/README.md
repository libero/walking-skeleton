# Airflow Example Usage

Dependencies
------------

* Python >=3.6
* [pipenv](https://docs.pipenv.org/)

Installation
------------
This will setup your virtual environment and install the required dependencies:

`pipenv --three install`

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

Browsing to [http://localhost:8080/](http://localhost:8080/) will now take you to the admin console.
