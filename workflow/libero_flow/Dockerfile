FROM python:3.6.4-stretch

RUN pip install pipenv

ADD . /srv/app/
WORKDIR /srv/app/flow

RUN pipenv install --system

RUN adduser elife
USER elife

#RUN python manage.py migrate
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
