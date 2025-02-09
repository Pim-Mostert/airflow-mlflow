from airflow import DAG
from airflow.operators.python import PythonOperator
from pathlib import Path
import os
import tempfile
from nbconvert import HTMLExporter
import papermill as pm
import mlflow


experiment1_dag = DAG(
    dag_id="experiment2",
    description="Experiment 2",
)


def execute_and_upload(
    experiment_name,
    notebook_path: Path,
):
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run() as run:
        os.environ["MLFLOW_RUN_ID"] = run.info.run_id

        # Execute the notebook
        executed_notebook = pm.execute_notebook(
            notebook_path,
            output_path=None,
            kernel_name="python3",
        )

        # Convert notebook to HTML
        html_exporter = HTMLExporter()
        html_body, _ = html_exporter.from_notebook_node(executed_notebook)

        # Upload the HTML to MLflow
        with tempfile.TemporaryDirectory() as tempdir:
            output_path = (
                Path(tempdir) / Path(notebook_path).stem
            ).with_suffix(".html")

            with open(output_path.as_posix(), "w") as f:
                f.write(html_body)

                mlflow.log_artifact(f.name)


PythonOperator(
    task_id="execute_and_upload",
    python_callable=execute_and_upload,
    op_kwargs={
        "experiment_name": "Experiment 2",
        "notebook_path": Path(__file__).parents[0] / "experiment1.ipynb",
    },
    dag=experiment1_dag,
)
