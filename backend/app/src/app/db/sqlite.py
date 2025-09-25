import sqlite3
import os

base_path = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_path, "dash.db")

connection = sqlite3.connect(db_path)

cursor = connection.cursor()

cursor.execute

#targets = '''create table if not exists Targets(
#            ID integer primary key autoincrement,
#            Name text,
#            Process text,
#            )'''
#
#data = '''create table if not exists Data(
#            ID integer primary key autoincrement,
#            Name text,
#            Process text,
#            TimePlayed real,
#            LastUse text,
#            FirstUse text
#            )'''