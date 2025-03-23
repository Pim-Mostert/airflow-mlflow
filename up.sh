#!/bin/bash

if [ "$1" == "" ]; then
    RUN_ENVIRONMENT="dev"
else
    RUN_ENVIRONMENT=$1
fi

echo "Writing RUN_ENVIRONMENT=$RUN_ENVIRONMENT to .run_environment.txt"
echo "$RUN_ENVIRONMENT" > .run_environment.txt

if [ "$RUN_ENVIRONMENT" == "prod" ]; then
    echo "Starting up in production mode..."

    docker compose \
        --env-file .env.prod \
        -f docker-compose.base.yml \
        -f docker-compose.prod.yml \
        pull
    
    docker compose \
        --env-file .env.prod \
        -f docker-compose.base.yml \
        -f docker-compose.prod.yml \
        up \
        --detach
else
    echo "Starting up in development mode..."

    docker compose \
        --env-file .env.dev \
        -f docker-compose.base.yml \
        -f docker-compose.dev.yml \
        pull
    
    docker compose \
        --env-file .env.dev \
        -f docker-compose.base.yml \
        -f docker-compose.dev.yml \
        up \
        --detach \
        --build
fi
