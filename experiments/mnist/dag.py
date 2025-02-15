import airflow
from pathlib import Path

from common.experiment import execute_and_upload

experiment_id = "mnist"


@airflow.decorators.dag(dag_id=experiment_id)
def dag():
    execute_and_upload(
        experiment_name=experiment_id,
        notebook_path=Path(__file__).parents[0] / f"{experiment_id}.ipynb",
    )


dag()
