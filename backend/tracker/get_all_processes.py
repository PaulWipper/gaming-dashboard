import psutil
import os

for i in psutil.process_iter(attrs=["name", "create_time", "cpu_times"]):
    print(i.info["name"])

base_path = os.path.dirname(os.path.abspath(__file__))
target_path = os.path.join(base_path, "../", "db", "targets.csv")
temp_data_path = os.path.join(base_path, "../", "db", "data.csv")
print(base_path, target_path, temp_data_path)