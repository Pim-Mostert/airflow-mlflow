#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "postgres" <<-EOSQL
    CREATE USER airflow WITH PASSWORD '$POSTGRES_AIRFLOW_PASSWORD';
    CREATE DATABASE airflow;
    ALTER DATABASE airflow OWNER TO airflow;
EOSQL
