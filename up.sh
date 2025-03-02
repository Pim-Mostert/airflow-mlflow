#!/bin/bash

RUN_ENVIRONMENT=$1

echo "Writing RUN_ENVIRONMENT=$RUN_ENVIRONMENT to .run_environment.txt"
echo "$RUN_ENVIRONMENT" > .run_environment.txt

# Check if the first argument is prod
if [ "$RUN_ENVIRONMENT" == "prod" ]; then
    docker compose \
        --env-file .env.prod \
        -f docker-compose.base.yml \
        -f docker-compose.prod.yml \
        up \
        --detach
else
    docker compose \
        --env-file .env.dev \
        -f docker-compose.base.yml \
        -f docker-compose.dev.yml \
        up \
        --detach \
        --build
fi
