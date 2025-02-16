import os
import tempfile
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


@task(task_id="execute_and_upload")
def execute_and_upload(
    experiment_id,
    notebook_path: Path,
    **kwargs,
):
    params = kwargs["params"]
    print(f"Supplied DAG parameters: {params}")

    mlflow.set_experiment(experiment_id)

    with mlflow.start_run() as run:
        # Set environment variable to setup run within notebook
        os.environ["MLFLOW_RUN_ID"] = run.info.run_id

        # Read notebook from disk
        notebook = jupytext.read(notebook_path, fmt="py:percent")

        # Inject arguments
        notebook_args = extract_parameter_dict(notebook)

        print(f"Detected notebook arguments: {notebook_args}")

        for notebook_arg in notebook_args:
            assert (
                notebook_arg in params
            ), f"Notebook parameter '{k}' not passed into DAG"

        notebook_args = parameter_values(notebook_args, **params)
        notebook = replace_definitions(notebook, notebook_args)

        # Define hooks and notebook client
        def on_cell_start(cell, cell_index):
            print(f"--- Starting cell #{cell_index}")

        def on_cell_executed(cell, cell_index, execute_reply=None):
            print(f"--- Executed cell #{cell_index}")
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
            print(
                f"Error executing notebook {notebook_path},"
                f" experiment id: {experiment_id}."
            )

            raise
        finally:
            # Convert notebook to HTML
            html_exporter = HTMLExporter()
            html_body, _ = html_exporter.from_notebook_node(notebook)

            # Upload the HTML to MLflow
            with tempfile.TemporaryDirectory() as tempdir:
                output_path = (Path(tempdir) / notebook_path.stem).with_suffix(
                    ".html"
                )

                with open(f"{output_path}", "w") as f:
                    f.write(html_body)

                    mlflow.log_artifact(f.name)
