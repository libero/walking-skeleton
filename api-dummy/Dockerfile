FROM php:7.1-fpm

RUN mkdir -p /var/www && \
    chown www-data:www-data /var/www

RUN apt-get update && apt-get install -y \
    git-core \
    zip

RUN docker-php-ext-configure opcache --enable-opcache \
    && docker-php-ext-install opcache

COPY --from=composer:1.6 /usr/bin/composer /usr/bin/composer

RUN mkdir -p /srv/app && \
    chown www-data:www-data /srv/app

USER www-data
WORKDIR /srv/app

COPY --chown=www-data:www-data composer.json composer.lock ./
RUN composer --no-interaction install --no-autoloader --no-scripts --no-suggest

COPY --chown=www-data:www-data . ./

ARG APP_ENV
ARG APP_SECRET
ENV APP_ENV="$APP_ENV"
ENV APP_SECRET="$APP_SECRET"

RUN composer dump-autoload
RUN composer run-script post-install-cmd
