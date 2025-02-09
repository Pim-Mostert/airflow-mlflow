import os
import tempfile
from airflow.decorators import task, dag
from nbconvert import HTMLExporter
import papermill as pm
import mlflow
from pathlib import Path


@task(task_id="execute_and_upload")
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


@dag(dag_id="experiment1", description="Experiment 1")
def experiment1_dag():
    execute_and_upload(
        experiment_name="Experiment 1",
        notebook_path=Path(__file__).parents[0] / "experiment1.ipynb",
    )


experiment1_dag()
