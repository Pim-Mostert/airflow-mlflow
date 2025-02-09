import os
import tempfile
from airflow import DAG, task
from airflow.decorators import task
import nbformat
from nbconvert import HTMLExporter
import papermill as pm
import mlflow

INPUT_DIR = os.path.realpath(__file__)
OUTPUT_DIR = "/tmp"
FILE_NAME = "notebook.ipynb"


@task(task_id="run_and_convert")
def execute_notebook_and_convert(
    mlflow_experiment_name,
):
    mlflow.set_experiment(mlflow_experiment_name)

    with mlflow.start_run() as run:
        # Read the input notebook
        INPUT_FILE = os.path.join(os.path.dirname(INPUT_DIR), FILE_NAME)

        with tempfile.NamedTemporaryFile(suffix=".ipynb") as fp:
            executed_notebook = pm.execute_notebook(
                INPUT_FILE,
                fp.name,
            )

            # Read notebook
            # executed_notebook = nbformat.read(fp, as_version=4)

        # Convert notebook to HTML
        html_exporter = HTMLExporter()
        html_body, _ = html_exporter.from_notebook_node(executed_notebook)

        # Upload the final HTML to MLflow
        with tempfile.TemporaryDirectory() as tempdir:
            with open(os.path.join(tempdir, "output.html"), "w") as f:
                f.write(html_body)

                mlflow.log_artifact(f.name)


with DAG(
    dag_id="run_notebook",
    description="Run notebook and export HTML",
) as dag:
    run_and_convert = execute_notebook_and_convert(
        mlflow_experiment_name="run_notebook",
    )
