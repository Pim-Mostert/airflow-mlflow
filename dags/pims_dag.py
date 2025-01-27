from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

# Define the DAG
with DAG(
    dag_id='pims_dag',
    default_args=default_args,
    description='A simple example DAG',
) as dag:
    task1 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    task2 = BashOperator(
        task_id='say_hello',
        bash_command='echo "Hello, Airflow!"',
    )

    task1 >> task2
