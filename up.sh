#!/bin/bash

# Check if the first argument is -a (attach)
if [ "$1" == "-a" ]; then
    DETACH=""
else
    DETACH="-d"
fi

docker compose up --build $DETACH