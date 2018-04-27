#!/usr/bin/env bash

pipenv run pytest

# now run flow api (django app) test suite
cd libero_flow/flow
pipenv run pytest
