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
        "name": Param("Pim", type="string"),
        "age": Param(35, type="integer"),
    },
)
def dag():
    execute_and_upload(
        experiment_id=experiment_id,
        notebook_path=notebook_path,
    )


dag()
