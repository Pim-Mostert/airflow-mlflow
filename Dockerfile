FROM apache/airflow:2.10.4-python3.12

COPY requirements-common.txt requirements-airflow.txt ./

RUN pip install --no-cache-dir -r requirements-airflow.txt