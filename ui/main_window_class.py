import sqlite3
import pandas as pd
from PyQt5.QtWidgets import (
    QVBoxLayout, QLineEdit, QWidget, QPushButton, QTableWidgetItem, QTableWidget, QFormLayout, QSpinBox, QComboBox,
    QLabel, QTabWidget, QTextEdit
)
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

        # init tab widget
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # add tabs
        self.tabs.addTab(self.search_tab(), "Search Monsters")
        self.tabs.addTab(self.generation_tab(), "Generate Monsters")
        self.tabs.addTab(self.legality_tab(), "Legal License Notes")

        # set layout
        self.setLayout(self.layout)
        self.setWindowTitle('PF2 Monster Dex')
        self.setGeometry(100, 100, 800, 600)

        # load data table on startup
        self.load_data()

    def search_tab(self):
        search_tab = QWidget()
        layout = QVBoxLayout()

        # search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText('Search')
        self.search_bar.textChanged.connect(self.search) # dynamic searching
        layout.addWidget(self.search_bar)

        # search button
        self.search_button = QPushButton('Search', self)
        self.search_button.clicked.connect(self.search)
        layout.addWidget(self.search_button)

        # data display table
        self.table = QTableWidget(self)
        layout.addWidget(self.table)

        search_tab.setLayout(layout)
        return search_tab

    def generation_tab(self):
        generate_tab = QWidget()
        layout = QVBoxLayout()

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
        layout.addLayout(self.form_layout)

        generate_tab.setLayout(layout)
        return generate_tab

    def legality_tab(self):
        legal_tab = QWidget()
        layout = QVBoxLayout()

        # legal license notes
        self.license_text = QTextEdit(self)
        self.license_text.setReadOnly(True)
        self.license_text.setText(
            "Legal License Notes:\n\n"  # TODO Replace this with actual license text
            "This work includes material taken from the System Reference Document 5.1 (SRD 5.1) by Wizards of the "
            "Coast and licensed under the Open Game License (OGL).\n\n"
            "For further details, please refer to the OGL available at www.wizards.com/d20.")

        layout.addWidget(self.license_text)
        legal_tab.setLayout(layout)
        return legal_tab

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
