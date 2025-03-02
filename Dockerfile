FROM apache/airflow:2.10.4-python3.12

WORKDIR /pip

ADD --chown=airflow:airflow packages /home/airflow/packages

RUN pip install -e /home/airflow/packages

