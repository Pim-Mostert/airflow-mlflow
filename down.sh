#!/bin/bash

# Read RUN_ENVIRONMENT
if [ -f .run_environment.txt ]; then
    RUN_ENVIRONMENT=$(cat .run_environment.txt)
    echo "Read RUN_ENVIRONMENT=$RUN_ENVIRONMENT from .run_environment.txt"    
else
    echo "Mode file not found!"
    
    RUN_ENVIRONMENT=
fi

# Check if RUN_ENVIRONMENT is prod
if [ "$AIRFLOW_ENVIRONMENT" == "prod" ]; then
    docker compose \
        --env-file .env.prod \
        -f docker-compose.base.yml \
        -f docker-compose.prod.yml \
        down
else
    docker compose \
        --env-file .env.dev \
        -f docker-compose.base.yml \
        -f docker-compose.dev.yml \
        down
fi

rm .run_environment.txt
