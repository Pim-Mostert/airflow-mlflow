#!/bin/bash

# Check if the first argument is -d
if [ "$1" == "-d" ]; then
    DETACH="-d"
else
    DETACH=""
fi

docker compose up --build $DETACH