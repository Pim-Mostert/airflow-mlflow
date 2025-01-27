import os
from airflow import DAG
from airflow.providers.papermill.operators.papermill import PapermillOperator
from airflow.operators.bash import BashOperator

INPUT_DIR = os.path.realpath(__file__)
OUTPUT_DIR = "/tmp"
FILE_NAME = "notebook.ipynb"

with DAG(
    dag_id="run_notebook",
    description="Run notebook and export HTML",
) as dag:
    run_notebook = PapermillOperator(
        task_id="run_notebook",
        input_nb=os.path.join(os.path.dirname(INPUT_DIR), FILE_NAME),
        output_nb=os.path.join(OUTPUT_DIR, FILE_NAME),
    )

    convert_to_html = BashOperator(
        task_id="convert_to_html",
        bash_command=f"jupyter nbconvert {os.path.join(OUTPUT_DIR, FILE_NAME)} --to html",
    )

    clean_up = BashOperator(
        task_id="clean_up",
        bash_command=f"rm {os.path.join(OUTPUT_DIR, FILE_NAME)}",
    )

    run_notebook >> convert_to_html >> clean_up
