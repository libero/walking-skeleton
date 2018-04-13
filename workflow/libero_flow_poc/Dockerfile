FROM python:3.6.4-stretch

RUN pip install pipenv

ADD . /srv/app/
WORKDIR /srv/app/

RUN pipenv install --system

#RUN adduser elife
#USER elife

WORKDIR /srv/app/libero_flow/flow

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
