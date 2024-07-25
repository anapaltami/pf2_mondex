"""
Iteration 3

Author: Anastasia Altamirano
Date: 2024-07-24
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
from config import CSV_FILE, DB_FILE, UI_EXEC_FILE
from cleaning import clean_data
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def database_setup(file, file_db):
    logging.info("Setting up the database.")
    # load data into SQLite
    df = pd.read_csv(file)
    df = clean_data(df)
    sqdb = sqlite3.connect(file_db)
    table_name = 'pf2_monsters'
    df.to_sql(table_name, sqdb, if_exists='replace', index=False)
    sqdb.close()
    logging.info("Database setup complete.")


if __name__ == '__main__':
    try:
        logging.info("Starting the application.")
        database_setup(CSV_FILE, DB_FILE)
        logging.info("Launching the UI.")
        from ui.main_window import main
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
