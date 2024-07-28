import sqlite3
import logging
import pandas as pd
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QSpinBox, QComboBox, QPushButton, QLabel, \
    QLineEdit
from models.pf2_newmon_model import NewMonsterModel
from src.config import DB_FILE, GENERATED_DB_FILE


class GenerationTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.model = NewMonsterModel()
        self.model.ensure_model_exists(level=0)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        # left panel for generation elements
        left_panel = QVBoxLayout()

        # PF2 monster generation elements
        self.form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Monster Name')
        self.level_input = QSpinBox()
        self.level_input.setRange(-1, 25)
        self.trait_input = QComboBox()
        self.trait_input.addItems(self.get_monster_traits())
        self.generate_button = QPushButton('Generate Monster')
        self.generate_button.clicked.connect(self.generate_monster)
        self.save_button = QPushButton('Save Monster')
        self.save_button.clicked.connect(self.save_monster)
        self.form_layout.addRow(QLabel('Name'), self.name_input)
        self.form_layout.addRow(QLabel('Level'), self.level_input)
        self.form_layout.addRow(QLabel('Trait'), self.trait_input)
        self.form_layout.addWidget(self.generate_button)
        self.form_layout.addWidget(self.save_button)
        left_panel.addLayout(self.form_layout)

        # right panel for generated monster details
        self.generated_details_panel = QVBoxLayout()
        self.generated_details_label = QLabel("Generate a monster to see its details.")
        self.generated_details_panel.addWidget(self.generated_details_label)

        layout.addLayout(left_panel)
        layout.addLayout(self.generated_details_panel)
        self.setLayout(layout)

    def get_monster_traits(self):
        conn = sqlite3.connect(DB_FILE)
        query = f"SELECT DISTINCT `Traits` FROM pf2_monsters"
        df = pd.read_sql_query(query, conn)
        conn.close()
        all_traits = df['Traits'].str.split(',').explode().str.strip().unique()
        return sorted(all_traits.tolist())

    def generate_monster(self):
        level = self.level_input.value()
        monster_trait = self.trait_input.currentText()
        logging.debug(f"Generating monster with level: {level} and trait: {monster_trait}")
        new_monster_block = self.model.predict(level, trait=monster_trait)
        if new_monster_block is not None:
            self.display_generated_monster(new_monster_block)
        else:
            self.show_message(f"No data available for trait: {monster_trait}")

    def display_generated_monster(self, new_monster_block):
        level = self.level_input.value()
        monster_trait = self.trait_input.currentText()
        details = f'Level {level} {monster_trait} Monster:\n'
        for stat, value in new_monster_block.items():
            details += f'{stat}: {value}\n'
        self.generated_details_label.setText(details)
        self.generated_monster_data = new_monster_block

    def get_next_id(self):
        try:
            conn = sqlite3.connect(DB_FILE)
            query = f"SELECT MAX(CAST(ID AS INTEGER)) FROM pf2_monsters"
            max_id_main = pd.read_sql_query(query, conn).iloc[0, 0]
            conn.close()

            conn = sqlite3.connect(GENERATED_DB_FILE)
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS generated_monsters ("
                "ID INTEGER, "
                "Name TEXT, "
                "Level INTEGER, "
                "Alignment TEXT, "
                "Size TEXT, "
                "Traits TEXT, "
                "Perception INTEGER, "
                "Languages TEXT, "
                "Skills TEXT, "
                "Str INTEGER, "
                "Dex INTEGER, "
                "Con INTEGER, "
                "Int INTEGER, "
                "Wis INTEGER, "
                "Cha INTEGER, "
                "AC INTEGER, "
                "Fort INTEGER, "
                "Ref INTEGER, "
                "Will INTEGER, "
                "HP INTEGER, "
                "Resistances TEXT, "
                "Speed TEXT, "
                "Source TEXT)")
            cursor.execute("SELECT MAX(CAST(ID AS INTEGER)) FROM generated_monsters")
            max_id_generated = cursor.fetchone()[0]
            conn.close()

            max_id_main = int(max_id_main) if max_id_main is not None else 0
            max_id_generated = int(max_id_generated) if max_id_generated is not None else 0

            return max(max_id_main, max_id_generated) + 1
        except Exception as e:
            logging.error(f"Error getting next ID: {e}", exc_info=True)
            return 1

    def save_monster(self):
        try:
            name = self.name_input.text()
            if not name:
                self.show_message("Please enter a name for the monster.")
                return

            if not hasattr(self, 'generated_monster_data'):
                self.show_message("No monster generated to save.")
                return

            next_id = self.get_next_id()

            monster_data = {
                'ID': next_id,
                'Name': name,
                'Level': self.level_input.value(),
                'Alignment': None,
                'Size': None,
                'Traits': self.trait_input.currentText(),
                'Perception': None,
                'Languages': None,
                'Skills': None,
                'Str': int(self.generated_monster_data['Str']),
                'Dex': int(self.generated_monster_data['Dex']),
                'Con': int(self.generated_monster_data['Con']),
                'Int': int(self.generated_monster_data['Int']),
                'Wis': int(self.generated_monster_data['Wis']),
                'Cha': int(self.generated_monster_data['Cha']),
                'AC': None,
                'Fort': None,
                'Ref': None,
                'Will': None,
                'HP': None,
                'Resistances': None,
                'Speed': None,
                'Source': 'PF2MONDEX'
            }

            conn = sqlite3.connect(GENERATED_DB_FILE)
            cursor = conn.cursor()
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS generated_monsters (
                ID INTEGER,
                Name TEXT,
                Level INTEGER,
                Alignment TEXT,
                Size TEXT,
                Traits TEXT,
                Perception INTEGER,
                Languages TEXT,
                Skills TEXT,
                Str INTEGER,
                Dex INTEGER,
                Con INTEGER,
                Int INTEGER,
                Wis INTEGER,
                Cha INTEGER,
                AC INTEGER,
                Fort INTEGER,
                Ref INTEGER,
                Will INTEGER,
                HP INTEGER,
                Resistances TEXT,
                Speed TEXT,
                Source TEXT
                )'''
            )
            cursor.execute(
                '''INSERT INTO generated_monsters 
                (ID, Name, Level, Alignment, Size, Traits, Perception, Languages, Skills, Str, Dex, Con, Int, Wis, Cha, 
                AC, Fort, Ref, Will, HP, Resistances, Speed, Source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (
                    monster_data['ID'],
                    monster_data['Name'],
                    monster_data['Level'],
                    monster_data['Alignment'],
                    monster_data['Size'],
                    monster_data['Traits'],
                    monster_data['Perception'],
                    monster_data['Languages'],
                    monster_data['Skills'],
                    monster_data['Str'],
                    monster_data['Dex'],
                    monster_data['Con'],
                    monster_data['Int'],
                    monster_data['Wis'],
                    monster_data['Cha'],
                    monster_data['AC'],
                    monster_data['Fort'],
                    monster_data['Ref'],
                    monster_data['Will'],
                    monster_data['HP'],
                    monster_data['Resistances'],
                    monster_data['Speed'],
                    monster_data['Source']
                )
            )
            conn.commit()
            conn.close()

            self.show_message(f"Monster '{name}' has been saved!")
        except Exception as e:
            logging.error(f"Error saving monster: {e}", exc_info=True)

    def show_message(self, message):
        msg = QLabel(message)
        msg.setWordWrap(True)
        self.generated_details_panel.addWidget(msg)
