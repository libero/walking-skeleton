FROM python:3.6.4-jessie

RUN pip install pipenv

ADD . /srv/app/
WORKDIR /srv/app/

RUN pipenv install --deploy

WORKDIR /srv/app/

CMD pipenv run python manage.py migrate && pipenv run python manage.py runserver 0.0.0.0:8000
