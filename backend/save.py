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