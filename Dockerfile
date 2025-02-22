# syntax=docker/dockerfile:1

### base
FROM apache/airflow:2.10.4-python3.12 AS base


### builder
FROM base AS builder

ARG AZURE_ARTIFACTS_TOKEN

ENV PIP_EXTRA_INDEX_URL=https://${AZURE_ARTIFACTS_TOKEN}@pkgs.dev.azure.com/mostertpim/BayesianNetwork/_packaging/BayesianNetwork/pypi/simple/

WORKDIR /pip

# Copy local packages
ADD --chown=airflow:airflow packages packages

# Check that the correct version of Airflow is installed
RUN pip install --no-deps --no-index -r ./packages/requirements-airflow.txt

# Install dependencies
COPY requirements.txt .

# RUN --mount=type=cache,target=/home/airflow/.cache/pip pip install -r ./requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install -r ./requirements.txt


### runner
FROM base

# Copy Python environment from builder
COPY --from=builder /home/airflow/.local /home/airflow/.local

