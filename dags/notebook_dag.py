import os
from airflow import DAG
from airflow.providers.papermill.operators.papermill import PapermillOperator



with DAG(
    dag_id='notebook_Dag',
    description='Notebook DAG',
) as dag:
    run_this = PapermillOperator(
        task_id="run_example_notebook",
        input_nb=os.path.join(os.path.dirname(os.path.realpath(__file__)), "notebook.ipynb"),
        output_nb="/opt/airflow/database/out-{{ logical_date }}.ipynb",
        parameters={"msgs": "Ran from Airflow at {{ logical_date }}!"},
    )
