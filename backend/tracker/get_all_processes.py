import psutil

for i in psutil.process_iter(attrs=["name", "create_time", "cpu_times"]):
    print(i.info["name"])