# %%


import mlflow

# %% tags=["parameters"]


name = "Truus"
age = 21


# %%

print(f"Name: {name} - end")
print(f"Age: {age} - end")

# %%

with mlflow.start_run():
    for true_age in range(20, 23):
        with mlflow.start_run(
            nested=True,
            run_name=f"Age: {true_age}",
        ) as run:
            mlflow.log_param("name", name)
            mlflow.log_metric("age", age + true_age)

            print(f"Age: {age + true_age}")
