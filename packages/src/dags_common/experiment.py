import os
import tempfile
from typing import Dict
from airflow.decorators import task


from nbconvert import HTMLExporter
import mlflow
from pathlib import Path
import jupytext
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError
from nbparameterise.code import extract_parameter_dict
from nbparameterise import (
    replace_definitions,
    parameter_values,
)
from airflow import DAG
from airflow.models.param import Param
from airflow.configuration import conf


@task(task_id="read_git_hash")
def read_git_hash(file_path: Path):
    with open(file_path, "r") as file:
        git_hash = file.read().strip()

    print(f"Git commit hash: {git_hash}")

    # Push to XCom by returning
    return git_hash


@task(task_id="execute_and_upload")
def execute_and_upload(
    experiment_id,
    notebook_path: Path,
    **kwargs,
):
    params = kwargs["params"]
    print(f"Supplied DAG parameters: {params}")

    ti = kwargs["ti"]
    run_id = kwargs["dag_run"].run_id

    mlflow.set_experiment(experiment_id)

    run_name = params["run_name"]
    if not run_name:
        print("No 'run_name' specified. Using Airflow's Run ID.")

        run_name = run_id

    with mlflow.start_run(run_name=run_name) as run:
        # Set environment variable to setup run within notebook
        os.environ["MLFLOW_RUN_ID"] = run.info.run_id

        # Set git_hash tag
        git_hash = ti.xcom_pull(task_ids="read_git_hash")
        mlflow.set_tag("git_hash", git_hash)

        # Read notebook from disk
        notebook = jupytext.read(notebook_path, fmt="py:percent")

        # Inject arguments
        notebook_args = extract_parameter_dict(notebook)

        print(f"Detected notebook arguments: {notebook_args}")

        for notebook_arg in notebook_args:
            assert notebook_arg in params, (
                f"Notebook parameter '{notebook_arg}' not passed into DAG"
            )

        notebook_args = parameter_values(notebook_args, **params)
        notebook = replace_definitions(notebook, notebook_args)

        # Define hooks and notebook client
        def on_cell_start(cell, cell_index):
            print(f"--- Starting cell #{cell_index}")

        def on_cell_executed(cell, cell_index, execute_reply=None):
            print(f"--- Executed cell #{cell_index}")
            print(f"'execute_reply': {execute_reply}")

            for output in cell.get("outputs", []):
                print(output.get("text", ""), end="")

        client = NotebookClient(
            notebook,
            on_cell_start=on_cell_start,
            on_cell_executed=on_cell_executed,
        )

        # Run notebook
        try:
            client.execute()
        except CellExecutionError:
            print(f"Error executing notebook {notebook_path}, experiment id: {experiment_id}.")

            raise
        finally:
            # Convert notebook to HTML
            html_exporter = HTMLExporter()
            html_body, _ = html_exporter.from_notebook_node(notebook)

            # Upload the HTML to MLflow
            with tempfile.TemporaryDirectory() as tempdir:
                output_path = (Path(tempdir) / notebook_path.stem).with_suffix(".html")

                with open(f"{output_path}", "w") as f:
                    f.write(html_body)

                    mlflow.log_artifact(f.name)


def create_experiment_dag(
    experiment_id: str,
    notebook_path: Path,
    experiment_params: Dict[str, Param],
) -> DAG:
    params = {
        "run_name": Param(
            default=None,
            type=["null", "string"],
            description=("Optional: run name (default: Airflow's Run ID)."),
        ),
    }

    # Add parameters if not exist in default parameters
    params.update({k: v for k, v in experiment_params.items() if k not in params})

    # Create and return the DAG object
    with DAG(
        dag_id=experiment_id,
        params=params,
    ) as dag:
        # read_git_hash
        dags_folder = conf.get("core", "dags_folder")
        git_hash_file_name = os.environ["GIT_HASH_FILE_NAME"]

        ti_read_git_hash = read_git_hash(Path(dags_folder) / git_hash_file_name)

        # ti_execute_and_upload
        ti_execute_and_upload = execute_and_upload(
            experiment_id=experiment_id,
            notebook_path=notebook_path,
        )

        # task order
        ti_read_git_hash >> ti_execute_and_upload

    return dag
