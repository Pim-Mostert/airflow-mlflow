### base
FROM apache/airflow:2.10.4-python3.12 AS base


### builder
FROM base AS builder

ARG AZURE_ARTIFACTS_TOKEN

ENV PIP_EXTRA_INDEX_URL=https://${AZURE_ARTIFACTS_TOKEN}@pkgs.dev.azure.com/mostertpim/BayesianNetwork/_packaging/BayesianNetwork/pypi/simple/

COPY requirements-common.txt requirements-airflow.txt ./

RUN pip install --no-cache-dir -r requirements-airflow.txt

### runner
FROM base

COPY --from=builder /home/airflow/.local/lib/python3.12/site-packages /home/airflow/.local/lib/python3.12/site-packages
