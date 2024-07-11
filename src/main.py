"""
Assignment 2

Author: Anastasia Altamirano
Date: 2024-07-10
Class: COS349-O
Instructor: Robert Martinez

Dependencies:
    - sqlite3
    - pandas
"""
import subprocess
import sys
from os import path
from config import CSV_FILE, DB_FILE, UI_EXEC_FILE
import sqlite3
import pandas as pd


def database_setup(file, file_db):
    # load data into SQLite
    df = pd.read_csv(file)
    sqdb = sqlite3.connect(file_db)
    table_name = path.splitext(file.name)[0]
    df.to_sql(table_name, sqdb, if_exists='replace', index=False)
    sqdb.close()


if __name__ == '__main__':
    database_setup(CSV_FILE, DB_FILE)
    subprocess.run([sys.executable, UI_EXEC_FILE])
