# Getting started

## Development

1. Create a virtual environment at `.venv`.
2. Run:
   ```
   python -m pip install --upgrade pip
   pip install keyring artifacts-keyring
   ```
3. Copy `pip.conf` to `.venv`.
4. Run `pip install -r requirements-dev.txt`.
5. (optionally) Follow the on-screen instructions to sign in to Azure Artifacts.

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
- [ ] Default run name {datetime.now{}) - and same between Airflow and MLflow
- [ ] Separate out experiments repo from airflow/mflow repo
- [ ] Custom runner containers with `bayesian-network` installed
- [ ] Use Postgres or MySql as database for Airflow
- [ ] Do not use SequentialExecutor