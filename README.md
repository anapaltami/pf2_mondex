## PF2 Monster Dex

**PF2 Monster Dex** is a desktop companion app for Pathfinder 2e built with Python and PyQt5. It lets you:

- **Browse and search** official PF2 monsters
- **Generate new monsters** using a simple machine‑learning model
- **Save generated monsters** into your own SQLite database so they appear in search results alongside the originals

### Roadmap to v1.0.0 (MVP)

#### v0.1.0 - Foundation (Current)
- [x] Basic project structure and SQLite integration
- [x] Data cleaning and loading from CSV
- [x] Search functionality for official monsters
- [x] Linear Regression model for Ability Scores (Str, Dex, Con, Int, Wis, Cha)
- [x] Simple UI to generate and save monsters (ability scores only)
- [x] Dark/Light mode support

#### v0.2.0 - Defensive Stats & Basic Predictions
- [ ] Expand model to predict AC, HP, and Saving Throws (Fort, Ref, Will)
- [ ] Update UI to display these defensive stats
- [ ] Save defensive stats to `generated_monsters.db`
- [ ] Implement prediction for Perception and Speed

#### v0.3.0 - Data Enrichment & Trait-based Scaling
- [ ] Incorporate Traits into the ML model more effectively (e.g., One-Hot Encoding)
- [ ] Add support for Alignment and Size generation
- [ ] Expand dataset to include offensive capabilities (Attacks, Damage)

#### v0.4.0 - Offensive Stats Generation
- [ ] Generate Melee and Ranged attack bonuses based on Level and Type
- [ ] Generate Damage dice/bonuses appropriate for level
- [ ] UI update: Add "Offense" section to the generated monster view

#### v0.5.0 - Resistances, Weaknesses, and Immunities
- [ ] ML model to suggest common Resistances, Weaknesses, and Immunities based on Traits
- [ ] UI toggle for suggested resistances/weaknesses

#### v0.6.0 - Advanced Feature Extraction & Abilities
- [ ] Extract "Common Abilities" (e.g., Grab, Knockdown, Fly) from existing data
- [ ] System to suggest level-appropriate special abilities or actions
- [ ] Template-based ability description generator

#### v0.7.0 - UI/UX Overhaul & Monster Sheet View
- [ ] "Stat Block" view mimicking official PF2e books
- [ ] Edit functionality for generated monsters
- [ ] Export options: JSON and PDF/Image

#### v0.8.0 - Balancing & Validation
- [ ] Compare generated stats against Gamemastery Guide creation tables
- [ ] Add "Balance Check" indicator (e.g., "High AC", "Low HP")
- [ ] Elite/Weak templates

#### v0.9.0 - Beta & Refinement
- [ ] Performance optimizations and bug fixes
- [ ] Finalize Legal/ORC documentation

#### v1.0.0 - Release MVP
- [ ] Fully functional monster generator (Level -1 to 24)
- [ ] Complete Stat Block generation (Stats, Attacks, Abilities)
- [ ] Search, Save, Edit, and Export features

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
