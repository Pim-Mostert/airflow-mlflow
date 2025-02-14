# Getting started

1. Copy `.env.template` to `.env` and configure its variables:
   - **DAGS_LOCATION**: Location of the DAGs for Airflow to parse.
   - **STORAGE_LOCATION**: Location for service's persistent storage (e.g. SQlite, artifacts, etc.).
2. Run `chmod +x up.sh` and `chmod +x down.sh`
3. Run `./up.sh -d`
   - Airflow is now available at `http://localhost:8080`
   - MLflow is now available at `http://localhost:9000`
4. Run `docker exec -it airflow bash`. Within the container, run `cat standalone_admin_password.txt` to get the default admin password.
5. Go to Airflow at `http://localhost:8080`, login as `admin` and the default password. Change your password under "Your Profile".
6. Profit.

# Todo

- [ ] Sync experiments from git
- [ ] Custom runner images with `bayesian-network` installed
- [ ] Use Postgres or MySql as database for Airflow