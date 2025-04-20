from importlib.metadata import PackageNotFoundError, version
from .experiment import create_experiment_dag

try:
    __version__ = version("bayesian_network")
except PackageNotFoundError:
    __version__ = "noinstall"

__all__ = [
    "create_experiment_dag",
]
