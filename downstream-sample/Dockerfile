FROM python:3.6.4-jessie

WORKDIR /srv/app/

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy

COPY downstream_sample/ /srv/app/downstream_sample/
COPY manage.py /srv/app/

CMD pipenv run python manage.py

