#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "postgres" <<-EOSQL
    CREATE USER mlflow WITH PASSWORD '$POSTGRES_MLFLOW_PASSWORD';
    CREATE DATABASE mlflow;
    ALTER DATABASE mlflow OWNER TO mlflow;
EOSQL

    # GRANT ALL PRIVILEGES ON DATABASE mlflow TO mlflow;
    # GRANT ALL ON SCHEMA public TO mlflow;
