import psutil
import time
import os
import datetime as dt
import json
import isRunning



def run():
    tracking = True
    trackGames = True
    trackApps = True

    print("[TRACKER][LOADING] Reading game-list.json")
    with open("tracker/assets/game-list.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    print("[TRACKER][OK] Read game-list.json")


    games = [g["name"] for g in data["games"]]
    print(f"Games:\n" + "\n".join(games))
    print("")


    apps = [a["name"] for a in data["apps"]]
    print(f"Apps:\n" + "\n".join(apps))
    print("")

    
    while tracking:
        
        time.sleep(3)



    
if __name__ == "__main__":
    run()
