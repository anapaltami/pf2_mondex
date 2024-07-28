from pathlib import Path
import sys


def resource_path(relative_path):
    try:
        base_path = Path(sys._MEIPASS)
    except Exception:
        base_path = Path(__file__).resolve().parents[1]

    return base_path / relative_path


MONDEX_ROOT = resource_path('')
DATA_FOLDER = MONDEX_ROOT / 'data'
MEDIA_FOLDER = MONDEX_ROOT / 'media'

PAIZO_LOGO = MEDIA_FOLDER / 'paizo_logo.png'
AZORA_LOGO = MEDIA_FOLDER / 'azoralaw_logo.png'

CSV_FILE = DATA_FOLDER / 'pf2_monsters.csv'
DB_FILE = DATA_FOLDER / 'PF2_Monsters.db'
GENERATED_DB_FILE = DATA_FOLDER / 'generated_monsters.db'

UI_FOLDER = MONDEX_ROOT / 'ui'
UI_EXEC_FILE = UI_FOLDER / 'main_window.py'
STYLE_SHEET = UI_FOLDER / 'styles_dark.qss'

AI_FOLDER = MONDEX_ROOT / 'models'
MODEL_FILE = AI_FOLDER / 'pf2_newmon_model.pkl'
