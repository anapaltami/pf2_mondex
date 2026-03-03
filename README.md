## PF2 Monster Dex

**PF2 Monster Dex** is a desktop companion app for Pathfinder 2e built with Python and PyQt5. It lets you:

- **Browse and search** official PF2 monsters
- **Generate new monsters** using a simple machine‑learning model
- **Save generated monsters** into your own SQLite database so they appear in search results alongside the originals

### Project layout

- `src/`
  - `main.py` – entrypoint; ensures the SQLite database is built from `data/pf2_monsters.csv` and launches the UI
  - `config.py` – paths for data, media, UI, and model files (supports PyInstaller via `resource_path`)
  - `cleaning.py` – data cleanup utilities used when building the `pf2_monsters` table
- `ui/`
  - `main_window.py` / `main_window_class.py` – PyQt5 main window and tab wiring
  - `search_tab.py` – search monsters (official + generated) and view basic details
  - `generation_tab.py` – generate and save new monsters
  - `legal_tab.py` – ORC license and attribution text, plus optional logo images
  - `styles_dark.qss` / `styles_light.qss` – dark and light themes
- `models/`
  - `pf2_newmon_model.py` – trains a linear regression model to estimate ability scores given a level and trait
- `data/`
  - `pf2_monsters.csv` – source monster dataset
  - `PF2_Monsters.db` – auto‑generated SQLite DB for official monsters
  - `generated_monsters.db` – SQLite DB for monsters you save from the generation tab

### Requirements

- Python 3.10+ is recommended
- See `requirements.txt` for Python dependencies

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Running the app

From the project root:

```bash
python -m src.main
```

On first run, this will:

1. Read `data/pf2_monsters.csv`
2. Clean and normalize the data
3. Build or refresh `data/PF2_Monsters.db`
4. Launch the PyQt5 GUI

Subsequent runs will only rebuild the database if the CSV is newer than the SQLite DB.

### Notes

- The legal tab optionally shows Paizo and Azora Law logos; place `paizo_logo.png` and `azoralaw_logo.png` in a `media/` folder alongside `data/`, `ui/`, and `models/` if you want those images to appear.
- Generated monsters are stored in `data/generated_monsters.db` and are searchable from the Search tab.

