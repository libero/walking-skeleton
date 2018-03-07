#!/bin/bash
set -e

# login as guest:guest on localhost:8080
exec docker run --hostname my-rabbit --name some-rabbit -p 8080:15672 rabbitmq:3.7.3-management
