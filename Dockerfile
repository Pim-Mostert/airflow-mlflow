FROM apache/airflow:2.10.4-python3.12

ADD --chown=airflow:airflow packages /packages

RUN pip install -e /packages

