import csv
import os
import pandas as pd

base_path = os.path.dirname(os.path.abspath(__file__))
target_path = os.path.join(base_path, "../", "db", "targets.csv")
data_path = os.path.join(base_path, "../", "db", "data.csv")

df = pd.read_csv(data_path)

print(base_path)