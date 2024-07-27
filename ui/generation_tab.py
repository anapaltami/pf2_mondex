import sqlite3
import logging
import pandas as pd
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QSpinBox, QComboBox, QPushButton, QLabel
from models.pf2_newmon_model import NewMonsterModel
from src.config import DB_FILE


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
        self.level_input = QSpinBox()
        self.level_input.setRange(-1, 25)
        self.trait_input = QComboBox()
        self.trait_input.addItems(self.get_monster_traits())
        self.generate_button = QPushButton('Generate Monster')
        self.generate_button.clicked.connect(self.generate_monster)
        self.form_layout.addRow(QLabel('Level'), self.level_input)
        self.form_layout.addRow(QLabel('Trait'), self.trait_input)
        self.form_layout.addWidget(self.generate_button)
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
