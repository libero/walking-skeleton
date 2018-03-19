#!/bin/bash
set -e

# login as guest:guest on localhost:8080

# detach from container
# hostname: used by RabbitMQ as configuration
# name: Docker container name for `docker start|stop`
# port 8080: management UI
# port 5672: AMQP 0.9 port
# rabbitmq_data: anonymous volume for persistence
# image: pinned, with management UI
docker run \
    -d \
    --hostname my-rabbit \
    --name some-rabbit \
    -p 8080:15672 \
    -p 5672:5672 \
    -v rabbitmq_data:/var/lib/rabbitmq \
    rabbitmq:3.7.3-management
