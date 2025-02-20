### base
FROM apache/airflow:2.10.4-python3.12 AS base


### builder
FROM base AS builder

ARG AZURE_ARTIFACTS_TOKEN

ENV PIP_EXTRA_INDEX_URL=https://${AZURE_ARTIFACTS_TOKEN}@pkgs.dev.azure.com/mostertpim/BayesianNetwork/_packaging/BayesianNetwork/pypi/simple/

COPY requirements.txt ./
RUN pip install -r requirements.txt


### runner
FROM base

# Copy Python environment from builder
COPY --from=builder /home/airflow/.local /home/airflow/.local

