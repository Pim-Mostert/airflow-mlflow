FROM apache/airflow:2.10.4-python3.12

WORKDIR /startup

COPY --chown=airflow:airflow startup.sh .

RUN chmod +x startup.sh

ENTRYPOINT /startup/startup.sh