import psutil
import time
import os
import datetime as dt
import json
from Process import Process

base_path = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_path, 'assets', 'game-list.json')



def run():
    tracking = True
    track_games = True
    track_apps = True

    print("[TRACKER][LOADING] Reading game-list.json")
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    print("[TRACKER][OK] Read game-list.json")


    games = [g["name"] for g in data["games"]]
    print(f"Games:\n" + "\n".join(games))
    print("")


    apps = [a["name"] for a in data["apps"]]
    print(f"Apps:\n" + "\n".join(apps))
    print("")

    processes = psutil.process_iter(attrs=["name", "create_time", "cpu_times"])
    
    user_processes = [Process("Discord"), Process("Valheim")]

    while tracking:
        for up in user_processes:
            up.get_is_running(processes)
        print("-----")
        processes = psutil.process_iter(attrs=["name", "create_time", "cpu_times"])
        time.sleep(5)



    
if __name__ == "__main__":
    run()
