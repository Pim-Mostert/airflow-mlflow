import datetime
import mlflow
import os

# Set the tracking URI to your local MLflow server
mlflow.set_tracking_uri(
    "http://127.0.0.1:9000"
)  # Replace with your server's address if different

# Test Experiment Name
experiment_name = f"Local_MLflow_Test {datetime.datetime.now()}"

# Create or get the experiment
experiment_id = mlflow.create_experiment(experiment_name)

experiment = mlflow.get_experiment_by_name(experiment_name)
print(experiment)

# Start an MLflow run
mlflow.end_run()
run = mlflow.start_run(experiment_id=experiment_id)

# Log a parameter
mlflow.log_param("param1", 5)

# Log a metric
mlflow.log_metric("metric1", 0.89)

# Create a dummy artifact
artifact_file = "test_artifact.txt"
with open(artifact_file, "w") as f:
    f.write("This is a test artifact for MLflow.")

# Log the artifact
mlflow.log_artifact(artifact_file, "output")

# Print the run info for verification
print("Run Info:")
print(f"Run ID: {run.info.run_id}")
print(f"Artifact URI: {run.info.artifact_uri}")
print(f"Experiment ID: {run.info.experiment_id}")

# Cleanup: Remove the test artifact from the local directory
if os.path.exists(artifact_file):
    os.remove(artifact_file)

print("Test completed successfully!")
