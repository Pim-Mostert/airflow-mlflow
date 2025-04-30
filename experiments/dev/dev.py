# %% tags=["parameters"]


name = ["a", "b", "c"]
age = [0.1, 0.5]


# %%

print(f"Name: {name} - end")
print(f"Age: {age} - end")

# %%

import os

from experiments.dev.common import get_name

os.getcwd()

print(get_name())
