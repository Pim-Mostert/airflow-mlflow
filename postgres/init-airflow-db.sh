#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "postgres" <<-EOSQL
    CREATE USER airflow WITH PASSWORD '$POSTGRES_AIRFLOW_PASSWORD';
    CREATE DATABASE airflow;
    GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;
    GRANT ALL ON SCHEMA public TO airflow;
    ALTER DATABASE airflow OWNER TO airflow;
EOSQL
