from airflow.decorators import dag
from pathlib import Path

from common.experiment import execute_and_upload


@dag(dag_id="experiment1", description="Experiment 1")
def experiment1_dag():
    execute_and_upload(
        experiment_name="Experiment 1",
        notebook_path=Path(__file__).parents[0] / "experiment1.ipynb",
    )


experiment1_dag()
