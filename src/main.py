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
import sqlite3
import pandas as pd
from config import CSV_FILE, DB_FILE
from cleaning import clean_data
import logging
from pathlib import Path

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def database_needs_refresh(csv_path: Path, db_path: Path) -> bool:
    """
    Return True if the SQLite DB is missing or older than the CSV source.
    """
    if not db_path.exists():
        return True

    try:
        return csv_path.stat().st_mtime > db_path.stat().st_mtime
    except OSError:
        # if we can't stat one of the files, be safe and rebuild
        return True


def database_setup(file, file_db):
    logging.info("Setting up the database.")
    # load data into SQLite
    df = pd.read_csv(file)
    df = clean_data(df)
    with sqlite3.connect(file_db) as sqdb:
        table_name = 'pf2_monsters'
        df.to_sql(table_name, sqdb, if_exists='replace', index=False)
    logging.info("Database setup complete.")


if __name__ == '__main__':
    try:
        logging.info("Starting the application.")
        if database_needs_refresh(CSV_FILE, DB_FILE):
            database_setup(CSV_FILE, DB_FILE)
        else:
            logging.info("Database is up-to-date; skipping rebuild.")
        logging.info("Launching the UI.")
        from ui.main_window import main
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
