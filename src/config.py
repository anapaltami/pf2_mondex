from pathlib import Path

MONDEX_ROOT = Path(__file__).resolve().parents[1]
DATA_FOLDER = MONDEX_ROOT / 'data'
CSV_FILE = DATA_FOLDER / 'Pokemon.csv'
DB_FILE = DATA_FOLDER / 'Pokemon.db'

UI_FOLDER = MONDEX_ROOT / 'ui'
UI_EXEC_FILE = UI_FOLDER / 'main_window.py'

AI_FOLDER = MONDEX_ROOT / 'models'
MODEL_FILE = AI_FOLDER / 'pokemon_model.pkl'
