import psutil
import os
from datetime import datetime as dt
import json
import asyncio

base_path = os.path.dirname(os.path.abspath(__file__))
target_path = os.path.join(base_path, "data", "targets.json")
temp_data_path = os.path.join(base_path, "data", "temp_data.json")

tracking_data = {"games": []}

def initialize():
    global tracking_data
    with open(target_path, "r", encoding="utf-8") as f:
        target_data = json.load(f)
    targets = target_data.get("games", [])
    try:
        with open(temp_data_path, "r", encoding="utf-8") as f:
            tracking_data = json.load(f)
    except FileNotFoundError:
        tracking_data = {"games": []}
    return {"targets": targets}

async def track_target(target, lock: asyncio.Lock):
    global tracking_data
    proc_name = (target.get("name") or "").strip()
    proc_proc = (target.get("process") or "").strip()

    while True:
        found_proc = None
        for proc in psutil.process_iter(attrs=["pid", "name"]):
            try:
                name = proc.info["name"] or ""
                if name == proc_name or name == proc_proc:
                    found_proc = proc
                    print(f"[OK] Process found: {name} (PID: {proc.info['pid']})")
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if not found_proc:
            await asyncio.sleep(5)
            continue

        today_iso = dt.today().date().isoformat()

        # Eintrag sicherstellen (anlegen falls fehlt)
        async with lock:
            games_list = tracking_data.setdefault("games", [])
            exists = False
            for game in games_list:
                if (game.get("name") or "").lower() == proc_name.lower():
                    game["last_use"] = today_iso
                    exists = True
                    break
            if not exists:
                games_list.append({
                    "name": proc_name or proc_proc,
                    "process": proc_proc or proc_name,
                    "time_played": 0.0,
                    "last_use": today_iso
                })
                print(f"[ADD] New entry for {proc_name or proc_proc}")

        # Laufzeit inkrementell addieren, solange der Prozess läuft
        last_tick = dt.now()
        while True:
            try:
                if not found_proc.is_running():
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                break

            await asyncio.sleep(1)
            now = dt.now()
            delta = (now - last_tick).total_seconds()
            last_tick = now

            async with lock:
                for game in tracking_data.get("games", []):
                    if (game.get("name") or "").lower() == proc_name.lower():
                        game["time_played"] = float(game.get("time_played", 0)) + delta
                        game["last_use"] = today_iso
                        break

        print(f"[END] {proc_name or proc_proc} stopped")

async def periodic_save(lock: asyncio.Lock):
    global tracking_data
    while True:
        await asyncio.sleep(30)
        async with lock:
            with open(temp_data_path, "w", encoding="utf-8") as f:
                json.dump(tracking_data, f, indent=2, ensure_ascii=False)
            print("[SYSTEM] Autosave completed")

async def run():
    data = initialize()
    write_lock = asyncio.Lock()
    tasks = [asyncio.create_task(track_target(game, write_lock)) for game in data["targets"]]
    tasks.append(asyncio.create_task(periodic_save(write_lock)))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(run())
