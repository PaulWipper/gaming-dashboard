from datetime import datetime as dt
from db.sqlite import *
import psutil
import asyncio
import time

DATA = None
DB_LOCK = asyncio.Lock()

def initialize():
    global DATA
    sql =   f"""
            SELECT * from Data
            """
    cursor.execute(sql)
    DATA = cursor.fetchall()
    return

async def track_application(application):
    print(application)
    while True:

        async with DB_LOCK:
            refresh =   f"""
                        SELECT * from Data
                        WHERE ID = {application[0]}
                        """
            cursor.execute(refresh)
            application = cursor.fetchall()[0]

        def _find_process():
            for proc in psutil.process_iter(attrs=["name"]):
                if proc.info.get("name") == application[1]:
                    return True
            return False
        
        found = await asyncio.to_thread(_find_process)

        if found:
            print(f"[OK] Application {application[1]} found.")

            await asyncio.sleep(10)

            async with DB_LOCK:
                save =  f"""
                        UPDATE Data
                        SET
                            TimePlayed = {application[4] + 10}
                        WHERE ID = {application[0]}
                        """
                cursor.execute(save)
                connection.commit()

            print(f"[OK] Application {application[1]} saved.")
        else:
            await asyncio.sleep(5)

async def run():
    initialize()
    tasks = [asyncio.create_task(track_application(game)) for game in DATA]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(run())

