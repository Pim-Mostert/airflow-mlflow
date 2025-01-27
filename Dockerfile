FROM apache/airflow

COPY requirements-dockerfile.txt .

RUN pip install --no-cache-dir -r requirements-dockerfile.txt