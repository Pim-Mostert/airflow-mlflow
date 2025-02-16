import airflow
from pathlib import Path

from common.experiment import execute_and_upload

experiment_id = "mnist"
notebook_path = Path(__file__).parents[0] / f"{experiment_id}.py"


@airflow.decorators.dag(dag_id=experiment_id)
def dag():
    execute_and_upload(
        experiment_id=experiment_id,
        notebook_path=notebook_path,
    )


dag()
