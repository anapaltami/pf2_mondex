from pathlib import Path
import sys


def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller. """
    try:
        base_path = Path(sys._MEIPASS)  # PyInstaller creates a temp folder and stores path in _MEIPASS
    except Exception:
        base_path = Path(__file__).resolve().parents[1]

    return base_path / relative_path


MONDEX_ROOT = resource_path('')
DATA_FOLDER = MONDEX_ROOT / 'data'
CSV_FILE = DATA_FOLDER / 'pf2_monsters.csv'
DB_FILE = DATA_FOLDER / 'PF2_Monsters.db'

UI_FOLDER = MONDEX_ROOT / 'ui'
UI_EXEC_FILE = UI_FOLDER / 'main_window.py'

AI_FOLDER = MONDEX_ROOT / 'models'
MODEL_FILE = AI_FOLDER / 'pf2_newmon_model.pkl'
