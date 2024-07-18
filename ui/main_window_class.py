import sqlite3
import pandas as pd
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QWidget, QPushButton, QTableWidgetItem, QTableWidget, QFormLayout, \
    QSpinBox, QComboBox, QLabel
from src.config import DB_FILE
from models.pf2_newmon_model import NewMonsterModel
import logging

logging.basicConfig(level=logging.DEBUG)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.model = NewMonsterModel()
        self.model.ensure_model_exists(level=0)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText('Search')
        self.layout.addWidget(self.search_bar)

        # search button
        self.search_button = QPushButton('Search', self)
        self.search_button.clicked.connect(self.search)
        self.layout.addWidget(self.search_button)

        # data display table
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

        # PF2 monster generation elements
        self.form_layout = QFormLayout()
        self.level_input = QSpinBox()
        self.level_input.setRange(-1, 25)
        self.trait_input = QComboBox()
        self.trait_input.addItems(self.get_monster_traits())
        self.generate_button = QPushButton('Generate')
        self.generate_button.clicked.connect(self.generate_monster)
        self.form_layout.addRow(QLabel('Level'), self.level_input)
        self.form_layout.addRow(QLabel('Trait'), self.trait_input)
        self.form_layout.addWidget(self.generate_button)
        self.layout.addLayout(self.form_layout)

        # set layout
        self.setLayout(self.layout)
        self.setWindowTitle('PF2 Monster Dex')
        self.table.setSortingEnabled(True)
        self.load_data()

    def load_data(self, query=""):
        conn = sqlite3.connect(DB_FILE)
        if query:
            sql_query = f"SELECT * FROM pf2_monsters WHERE Name LIKE '%{query}%'"
        else:
            sql_query = f"SELECT * FROM pf2_monsters"
        df = pd.read_sql_query(sql_query, conn)
        conn.close()

        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)

        for row_index, row in df.iterrows():
            for col_index, col in enumerate(df.columns):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(row[col])))

    def search(self):
        query = self.search_bar.text()
        self.load_data(query)

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
        message = f'Level {level} {monster_trait} Monster:\n'
        for stat, value in new_monster_block.items():
            message += f'{stat}: {value}\n'
        self.show_message(message)

    def show_message(self, message):
        msg = QLabel(message)
        msg.setWordWrap(True)
        self.layout.addWidget(msg)
