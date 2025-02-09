import os
import tempfile
from airflow.decorators import task, dag
from nbconvert import HTMLExporter
import papermill as pm
import mlflow


@task(task_id="run_and_convert")
def execute_notebook_and_convert(
    mlflow_experiment_name,
    notebook_file,
):
    mlflow.set_experiment(mlflow_experiment_name)

    with mlflow.start_run() as run:
        os.environ["MLFLOW_RUN_ID"] = run.info.run_id

        # Execute the notebook
        executed_notebook = pm.execute_notebook(
            notebook_file,
            output_path=None,
            kernel_name="python3",
        )

        # Convert notebook to HTML
        html_exporter = HTMLExporter()
        html_body, _ = html_exporter.from_notebook_node(executed_notebook)

        # Upload the HTML to MLflow
        with tempfile.TemporaryDirectory() as tempdir:
            with open(os.path.join(tempdir, "output.html"), "w") as f:
                f.write(html_body)

                mlflow.log_artifact(f.name)


@dag(dag_id="experiment1", description="Experiment 1")
def experiment1_dag():
    execute_notebook_and_convert(
        mlflow_experiment_name="Experiment 1",
        notebook_file=os.path.join(
            os.path.dirname(__file__), "experiment1.ipynb"
        ),
    )


experiment1_dag()
