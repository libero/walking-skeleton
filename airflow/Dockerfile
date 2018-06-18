FROM python:3.6-jessie

ARG AIRFLOW_VERSION=1.9.0
ARG AIRFLOW_HOME=/usr/local/airflow

WORKDIR ${AIRFLOW_HOME}

RUN set -ex \
    && apt-get update -yqq \
    && apt-get install -yqq --no-install-recommends \
        netcat-openbsd \
    && useradd -s /bin/bash -d ${AIRFLOW_HOME} airflow \
    && pip install -U pipenv

COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --deploy

COPY . ./

RUN chown -R airflow: .

EXPOSE 8080 5555 8793

USER airflow
ENTRYPOINT [".docker/entrypoint.sh"]
