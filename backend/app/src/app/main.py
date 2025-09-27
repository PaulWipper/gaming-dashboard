from fastapi import FastAPI, HTTPException
from db.sqlite import cursor, connection
from pydantic import BaseModel

app = FastAPI()

class Application(BaseModel):
    ID: int
    Name: str
    Nickname: str
    Process: str
    TimePlayed: float
    LastUse: str
    FirstUse: str

@app.get("/data", tags=["Database"])
async def get_data():
    sql = "SELECT * from Data"
    cursor.execute(sql)
    results = cursor.fetchall()
    return results

@app.get("/data/{application_id}", tags=["Database"])
async def get_single_data(application_id: int):
    sql = f"SELECT * from Data WHERE ID = {application_id}"
    cursor.execute(sql)
    results = cursor.fetchall()
    return results

@app.post("/data", tags=["Database"])
async def add_data(application: Application):
    sql =   f"""
            INSERT INTO Data(Name, Nickname, Process, TimePlayed, LastUse, FirstUse)
            VALUES ('{application.Name}', '{application.Nickname}', '{application.Process}', {application.TimePlayed}, '{application.LastUse}', '{application.FirstUse}')
            """
    cursor.execute(sql)
    connection.commit()
    return

@app.put("/data", tags=["Database"])
async def update_data(application: Application):
    sql =   f"""
            UPDATE Data
            SET 
                Name = '{application.Name}',
                Nickname = '{application.Nickname}', 
                Process = '{application.Process}',
                TimePlayed = {application.TimePlayed},
                LastUse = '{application.LastUse}',
                FirstUse = '{application.FirstUse}'
            WHERE ID = {application.ID}
            """
    cursor.execute(sql)
    connection.commit()
    return

@app.delete("/data/{application_id}", tags=["Database"])
async def delete_data(application_id):
    sql =   f"""
            DELETE FROM Data
            WHERE ID = {application_id}
            """
    cursor.execute(sql)
    connection.commit()
    return



@app.post("/data/empty", tags=["Database"])
async def add_data(application: Application):
    sql =   f"""
            INSERT INTO Data(Name, Nickname, Process, TimePlayed, LastUse, FirstUse)
            VALUES ('{application.Name}', '{application.Nickname}', '{application.Process}', 0, '', '')
            """
    cursor.execute(sql)
    connection.commit()
    return



@app.get("/data/columns", tags=["Database"])
async def get_data_columns():
    sql = "PRAGMA table_info(Data)"
    cursor.execute(sql)
    results = cursor.fetchall()
    return results

