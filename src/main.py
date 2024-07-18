"""
Iteration 2

Author: Anastasia Altamirano
Date: 2024-07-17
Class: COS349-O
Instructor: Robert Martinez

Dependencies:
    - pandas
    - scikit-learn
    - joblib
    - PyQt5
    - logging
"""
import subprocess
import sys
import sqlite3
import pandas as pd
from os import path
from config import CSV_FILE, DB_FILE, UI_EXEC_FILE
from cleaning import clean_data


def database_setup(file, file_db):
    # load data into SQLite
    df = pd.read_csv(file)
    df = clean_data(df)
    sqdb = sqlite3.connect(file_db)
    table_name = path.splitext(file.name)[0]
    df.to_sql(table_name, sqdb, if_exists='replace', index=False)
    sqdb.close()


if __name__ == '__main__':
    database_setup(CSV_FILE, DB_FILE)
    subprocess.run([sys.executable, UI_EXEC_FILE])
