from pathlib import Path
from airflow import DAG
from airflow.models.param import Param
from common.experiment import execute_and_upload

experiment_id = Path(__file__).parents[0].stem
notebook_path = Path(__file__).parents[0] / f"{experiment_id}.py"

# Create the DAG object using the context manager
with DAG(
    dag_id=experiment_id,
    params={
        "run_name": Param(None, type=["null", "string"]),
        "name": Param("Pim", type="string"),
        "age": Param(35, type="integer"),
    },
) as dag:
    execute_and_upload(
        experiment_id=experiment_id,
        notebook_path=notebook_path,
    )
