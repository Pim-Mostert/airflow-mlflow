import os
import tempfile
from airflow.decorators import task


from nbconvert import HTMLExporter
import mlflow
from pathlib import Path
import jupytext
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError


@task(task_id="execute_and_upload")
def execute_and_upload(
    experiment_id,
    notebook_path: Path,
):
    mlflow.set_experiment(experiment_id)

    with mlflow.start_run() as run:
        os.environ["MLFLOW_RUN_ID"] = run.info.run_id

        with open(notebook_path, "r") as f:
            py_content = f.read()

        notebook = jupytext.reads(py_content, fmt="py:percent")

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

        try:
            client.execute()
        except CellExecutionError:
            print(
                f"Error executing notebook {notebook_path},"
                f" experiment id: {experiment_id}."
            )

            raise
        finally:
            html_exporter = HTMLExporter()
            html_body, _ = html_exporter.from_notebook_node(notebook)

            # Upload the HTML to MLflow
            with tempfile.TemporaryDirectory() as tempdir:
                output_path = (
                    Path(tempdir) / Path(notebook_path).stem
                ).with_suffix(".html")

                with open(output_path.as_posix(), "w") as f:
                    f.write(html_body)

                    mlflow.log_artifact(f.name)
