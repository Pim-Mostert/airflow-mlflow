# Getting started

## Setup Airflow and MLflow

1. Copy `.env.template` to `.env` and configure its variables
2. Run `chmod +x up.sh` and `chmod +x down.sh`
3. Run `./up.sh`
   - Airflow is now available at `http://localhost:8080`
   - MLflow is now available at `http://localhost:9000`

# Todo

- [x] Install private `bayesian-network` package in Airflow container
- [x] Use normal Python file (and interactive in VS) instead of .ipynb
- [x] Handle Exceptions in notebooks
- [x] Parameterize runs
- [x] Custom run names
- [x] Sync experiments from git
- [x] Remove Airflow login
- [ ] WARN: SecretsUsedInArgOrEnv: Do not use ARG or ENV instructions for sensitive data (ARG "AZURE_ARTIFACTS_TOKEN") (line 8) 
  - See: https://docs.docker.com/compose/how-tos/use-secrets/#examples
- [ ] Add git commit hash to run
- [ ] Default run name {datetime.now{}) - and same between Airflow and MLflow
- [x] Publish dags_common package
- [ ] Separate out experiments repo from airflow/mflow repo
- [ ] Custom runner containers with `bayesian-network` installed
- [ ] Use Postgres or MySql as database for Airflow
- [ ] Do not use SequentialExecutor