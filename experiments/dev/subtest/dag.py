from pathlib import Path

from dags_common import create_experiment_dag

experiment_id = Path(__file__).parents[0].stem
notebook_path = Path(__file__).parents[0] / f"{experiment_id}.py"

dag = create_experiment_dag(
    experiment_id,
    notebook_path,
)
