import os
import tempfile
from airflow import DAG
from airflow.operators.python import PythonOperator
import nbformat
from nbconvert import HTMLExporter
import papermill as pm

INPUT_DIR = os.path.realpath(__file__)
OUTPUT_DIR = "/tmp"
FILE_NAME = "notebook.ipynb"


def execute_notebook_and_convert(**kwargs):
    # Read the input notebook
    INPUT_FILE = os.path.join(os.path.dirname(INPUT_DIR), FILE_NAME)

    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fp:
        pm.execute_notebook(
            INPUT_FILE,
            fp.name,
        )

        # Read notebook
        executed_notebook = nbformat.read(fp, as_version=4)

    # Convert notebook to HTML
    html_exporter = HTMLExporter()
    (html_body, _) = html_exporter.from_notebook_node(executed_notebook)

    # Save the final HTML to disk
    with open(os.path.join(OUTPUT_DIR, "output.html"), "w") as f:
        f.write(html_body)


with DAG(
    dag_id="run_notebook",
    description="Run notebook and export HTML",
) as dag:
    run_and_convert = PythonOperator(
        task_id="run_and_convert",
        python_callable=execute_notebook_and_convert,
    )
