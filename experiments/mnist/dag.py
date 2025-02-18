import airflow
from pathlib import Path
from airflow.models.param import Param

from common.experiment import execute_and_upload

experiment_id = Path(__file__).parents[0].stem
notebook_path = Path(__file__).parents[0] / f"{experiment_id}.py"


@airflow.decorators.dag(
    dag_id=experiment_id,
    params={
        "run_name": Param(None, type=["null", "string"]),
        "device": Param("cpu", type="string"),
        "selected_num_observations": Param(1000, type="integer"),
        "num_iterations": Param(10, type="integer"),
        "gamma": Param(0.00001, type="number"),
    },
)
def dag():
    execute_and_upload(
        experiment_id=experiment_id,
        notebook_path=notebook_path,
    )


dag()
