#!/bin/bash

# Check if the first argument is -a (attach)
# if [ "$1" == "-a" ]; then
#     DETACH=""
# else
#     DETACH="-d"
# fi

docker compose \
    --env-file .env.dev \
    -f docker-compose.base.yml \
    -f docker-compose.dev.yml \
    up \
    --detach \
    --build