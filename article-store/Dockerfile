FROM python:3.6.4-jessie

RUN mkdir -p /var/www && \
    chown www-data:www-data /var/www

RUN pip install pipenv

RUN mkdir -p /srv/app && \
    chown www-data:www-data /srv/app

USER www-data
WORKDIR /srv/app

COPY --chown=www-data:www-data Pipfile Pipfile.lock ./
RUN pipenv install --deploy

COPY --chown=www-data:www-data . ./

EXPOSE 8000

CMD pipenv run python -u manage.py runserver 0.0.0.0:8000
